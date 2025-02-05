# Copyright (C) 2024 Nice Zombies
"""JSON decoder."""
# TODO(Nice Zombies): Fix end_offset in JSONSyntaxError
from __future__ import annotations

__all__: list[str] = ["Decoder", "JSONSyntaxError", "detect_encoding"]

import re
import sys
from codecs import (
    BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE,
)
from decimal import Decimal, InvalidOperation
from math import isinf
from os import PathLike, fspath
from os.path import realpath
from pathlib import Path
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from shutil import get_terminal_size
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container

    _T_co = TypeVar("_T_co", covariant=True)

    # pylint: disable-next=R0903
    class _SupportsRead(Protocol[_T_co]):
        def read(self, length: int = ..., /) -> _T_co:  # type: ignore
            """Read string."""

    _MatchFunc = Callable[[str, int], Match[str] | None]
    _Scanner = Callable[[str, str], Any]
    _StrPath = PathLike[str] | str
    _Hook = Callable[[Any], Any]


_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL
_UNESCAPE: dict[str, str] = {
    '"': '"',
    "\\": "\\",
    "/": "/",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
}

_match_chunk: _MatchFunc = re.compile(r'[^"\\\x00-\x1f]+', _FLAGS).match
_match_hex_digits: _MatchFunc = re.compile(r"[0-9A-Fa-f]{4}", _FLAGS).match
_match_line_end: _MatchFunc = re.compile(r"[^\n\r]+", _FLAGS).match
_match_number: _MatchFunc = re.compile(
    r"""
    (-?0|-?[1-9][0-9]*) # integer
    (\.[0-9]+)?         # [frac]
    ([eE][-+]?[0-9]+)?  # [exp]
    """, _FLAGS,
).match
_match_unquoted_key: _MatchFunc = re.compile(
    r"(?:\w+|[^\x00-\x7f]+)+", _FLAGS,
).match
_match_whitespace: _MatchFunc = re.compile(r"[ \t\n\r]+", _FLAGS).match


def _get_err_context(doc: str, start: int, end: int) -> tuple[int, str, int]:
    line_start: int = max(
        doc.rfind("\n", 0, start), doc.rfind("\r", 0, start),
    ) + 1
    if match := _match_whitespace(doc, line_start):
        line_start = min(match.end(), start)

    if match := _match_line_end(doc, start):
        line_end: int = match.end()
    else:
        line_end = start

    end = min(line_end, end)
    if match := _match_whitespace(doc[::-1], len(doc) - line_end):
        line_end = max(end, len(doc) - match.end())

    if end == start:
        end += 1

    max_chars: int = get_terminal_size().columns - 4  # leading spaces
    if end == line_end + 1:  # newline
        max_chars -= 1

    text_start: int = max(min(
        line_end - max_chars, end - 1 - max_chars // 2,
        start - (max_chars + 2) // 3,
    ), line_start)
    text_end: int = min(max(
        line_start + max_chars, start + (max_chars + 1) // 2,
        end + max_chars // 3,
    ), line_end)
    text: str = doc[text_start:text_end].expandtabs(1)
    if text_start > line_start:
        text = "..." + text[3:]

    if len(text) > max_chars:
        end -= len(text) - max_chars
        text = (
            text[:max_chars // 2 - 1] + "..." + text[2 - (max_chars + 1) // 2:]
        )

    if text_end < line_end:
        text = text[:-3] + "..."

    return start - text_start + 1, text, end - text_start + 1


def _unescape_unicode(filename: str, s: str, end: int) -> int:
    if match := _match_hex_digits(s, end):
        try:
            return int(match.group(), 16)
        except ValueError:
            pass

    msg: str = "Expecting 4 hex digits"
    raise _errmsg(msg, filename, s, end, -4)


class JSONSyntaxError(SyntaxError):
    """Invalid JSON (query) syntax.

    :param msg: an error message
    :param filename: the path to the JSON file
    :param doc: a JSON string
    :param start: the start position
    :param end: the end position or negative offset

    Example:
        >>> import jsonyx as json
        >>> raise json.JSONSyntaxError("Expecting value", "<string>", "[,]", 1)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "<string>", line 1
            [,]
             ^
        jsonyx.JSONSyntaxError: Expecting value

    .. seealso:: :func:`jsonyx.format_syntax_error` for formatting the
        exception.

    """

    def __init__(
        self, msg: str, filename: str, doc: str, start: int = 0, end: int = 0,
    ) -> None:
        """Create a new JSON syntax error."""
        lineno: int = (
            doc.count("\n", 0, start)
            + doc.count("\r", 0, start)
            - doc.count("\r\n", 0, start)
            + 1
        )
        colno: int = start - max(
            doc.rfind("\n", 0, start), doc.rfind("\r", 0, start),
        )
        if end <= 0:  # offset
            if match := _match_line_end(doc, start):
                end = min(match.end(), start - end)
            else:
                end = start

        end_lineno: int = (
            doc.count("\n", 0, end)
            + doc.count("\r", 0, end)
            - doc.count("\r\n", 0, end)
            + 1
        )
        end_colno: int = end - max(
            doc.rfind("\n", 0, end), doc.rfind("\r", 0, end),
        )
        offset, text, end_offset = _get_err_context(doc, start, end)
        if sys.version_info >= (3, 10):
            super().__init__(
                msg, (filename, lineno, offset, text, end_lineno, end_offset),
            )
        else:
            self.end_lineno: int = end_lineno
            self.end_offset: int = end_offset
            super().__init__(msg, (filename, lineno, offset, text))

        self.colno: int = colno
        self.end_colno: int = end_colno

    def __str__(self) -> str:
        """Convert to string."""
        if self.end_lineno == self.lineno:
            line_range: str = f"{self.lineno:d}"
        else:
            line_range = f"{self.lineno:d}-{self.end_lineno:d}"

        if self.end_colno == self.colno:
            column_range: str = f"{self.colno:d}"
        else:
            column_range = f"{self.colno:d}-{self.end_colno:d}"

        return (
            f"{self.msg} ({self.filename}, line {line_range}, column "
            f"{column_range})"
        )


JSONSyntaxError.__module__ = "jsonyx"
_errmsg: type[JSONSyntaxError] = JSONSyntaxError


def detect_encoding(b: bytearray | bytes) -> str:
    r"""Detect the JSON encoding.

    :param b: a JSON string
    :return: the detected encoding

    Example:
        >>> import jsonyx as json
        >>> b = b'\x00"\x00f\x00o\x00o\x00"'
        >>> b.decode(json.detect_encoding(b))
        '"foo"'

    .. note:: Supports only ``"utf_8"``, ``"utf_8-sig"``, ``"utf_16"``,
        ``"utf_16_be"``, ``"utf_16_le"``, ``"utf_32"``, ``"utf_32_be"`` and
        ``"utf_32_le"``.

    """
    # JSON must start with ASCII character (not NULL)
    # Strings can't contain control characters (including NULL)
    encoding: str = "utf_8"
    startswith: Callable[[bytes | tuple[bytes, ...]], bool] = b.startswith
    if startswith((BOM_UTF32_BE, BOM_UTF32_LE)):
        encoding = "utf_32"
    elif startswith((BOM_UTF16_BE, BOM_UTF16_LE)):
        encoding = "utf_16"
    elif startswith(BOM_UTF8):
        encoding = "utf_8_sig"
    elif len(b) >= 4:
        if not b[0]:
            # 00 00 -- -- - utf_32_be
            # 00 XX -- -- - utf_16_be
            encoding = "utf_16_be" if b[1] else "utf_32_be"
        elif not b[1]:
            # XX 00 00 00 - utf_32_le
            # XX 00 00 XX - utf_16_le
            # XX 00 XX -- - utf_16_le
            encoding = "utf_16_le" if b[2] or b[3] else "utf_32_le"
    elif len(b) == 2:
        if not b[0]:
            # 00 -- - utf_16_be
            encoding = "utf_16_be"
        elif not b[1]:
            # XX 00 - utf_16_le
            encoding = "utf_16_le"

    return encoding


detect_encoding.__module__ = "jsonyx"

try:
    if not TYPE_CHECKING:
        from _jsonyx import make_scanner
except ImportError:
    def make_scanner(
        bool_hook: _Hook,
        float_hook: _Hook,
        int_hook: _Hook,
        mapping_hook: _Hook,
        sequence_hook: _Hook,
        str_hook: _Hook,
        allow_comments: bool,  # noqa: FBT001
        allow_missing_commas: bool,  # noqa: FBT001
        allow_nan_and_infinity: bool,  # noqa: FBT001
        allow_surrogates: bool,  # noqa: FBT001
        allow_trailing_comma: bool,  # noqa: FBT001
        allow_unquoted_keys: bool,  # noqa: FBT001
        use_decimal: bool,  # noqa: FBT001
    ) -> _Scanner:
        """Make JSON scanner."""
        memo: dict[Any, Any] = {}
        memoize: Callable[[Any, Any], Any] = memo.setdefault
        parse_float: Callable[
            [str], Decimal | float,
        ] = Decimal if use_decimal else float
        if use_decimal:
            float_hook = Decimal

        def skip_comments(filename: str, s: str, end: int) -> int:
            find: Callable[[str, int], int] = s.find
            while True:
                if match := _match_whitespace(s, end):
                    end = match.end()

                comment_idx: int = end
                if (comment_prefix := s[end:end + 2]) == "//":
                    end += 2
                    if match := _match_line_end(s, end):
                        end = match.end()
                elif comment_prefix == "/*":
                    if (end := find("*/", end + 2)) == -1:
                        if allow_comments:
                            msg: str = "Unterminated comment"
                        else:
                            msg = "Comments are not allowed"

                        raise _errmsg(msg, filename, s, comment_idx, len(s))

                    end += 2
                else:
                    return end

                if not allow_comments:
                    msg = "Comments are not allowed"
                    raise _errmsg(msg, filename, s, comment_idx, end)

        def scan_string(filename: str, s: str, end: int) -> tuple[Any, int]:
            chunks: list[str] = []
            append_chunk: Callable[[str], None] = chunks.append
            str_idx: int = end - 1
            while True:
                # Match one or more unescaped string characters
                if match := _match_chunk(s, end):
                    end = match.end()
                    append_chunk(match.group())

                # Terminator is the end of string, a literal control character,
                # or a backslash denoting that an escape sequence follows
                try:
                    terminator: str = s[end]
                except IndexError:
                    msg: str = "Unterminated string"
                    raise _errmsg(msg, filename, s, str_idx, end) from None

                if terminator == '"':
                    return str_hook("".join(chunks)), end + 1

                if terminator != "\\":
                    if terminator in {"\n", "\r"}:
                        msg = "Unterminated string"
                        raise _errmsg(msg, filename, s, str_idx, end)

                    msg = "Unescaped control character"
                    raise _errmsg(msg, filename, s, end, end + 1)

                end += 1
                try:
                    esc = s[end]
                except IndexError:
                    msg = "Expecting escaped character"
                    raise _errmsg(msg, filename, s, end) from None

                # If not a unicode escape sequence, must be in the lookup table
                if esc != "u":
                    try:
                        char = _UNESCAPE[esc]
                    except KeyError:
                        if esc in {"\n", "\r"}:
                            msg = "Expecting escaped character"
                            raise _errmsg(msg, filename, s, end) from None

                        msg = "Invalid backslash escape"
                        raise _errmsg(
                            msg, filename, s, end - 1, end + 1,
                        ) from None

                    end += 1
                else:
                    uni: int = _unescape_unicode(filename, s, end + 1)
                    end += 5
                    if 0xd800 <= uni <= 0xdbff:
                        if s[end:end + 2] == r"\u":
                            uni2: int = _unescape_unicode(filename, s, end + 2)
                            if 0xdc00 <= uni2 <= 0xdfff:
                                uni = ((uni - 0xd800) << 10) | (uni2 - 0xdc00)
                                uni += 0x10000
                                end += 6
                            elif not allow_surrogates:
                                msg = "Surrogates are not allowed"
                                raise _errmsg(msg, filename, s, end - 6, end)
                        elif not allow_surrogates:
                            msg = "Surrogates are not allowed"
                            raise _errmsg(msg, filename, s, end - 6, end)
                    elif 0xdc00 <= uni <= 0xdfff and not allow_surrogates:
                        msg = "Surrogates are not allowed"
                        raise _errmsg(msg, filename, s, end - 6, end)

                    char = chr(uni)

                append_chunk(char)

        def scan_object(filename: str, s: str, end: int) -> tuple[Any, int]:
            obj_idx: int = end - 1
            end = skip_comments(filename, s, end)
            try:
                nextchar: str = s[end]
            except IndexError:
                msg: str = "Unterminated object"
                raise _errmsg(msg, filename, s, obj_idx, end) from None

            if nextchar == "}":
                return mapping_hook([]), end + 1

            pairs: list[tuple[Any, Any]] = []
            append_pair: Callable[[tuple[Any, Any]], None] = pairs.append
            while True:
                key_idx: int = end
                if (nextchar := s[end:end + 1]) == '"':
                    key, end = scan_string(filename, s, end + 1)
                elif (
                    match := _match_unquoted_key(s, end)
                ) and match.group().isidentifier():
                    end = match.end()
                    if not allow_unquoted_keys:
                        msg = "Unquoted keys are not allowed"
                        raise _errmsg(msg, filename, s, key_idx, end)

                    key = match.group()
                else:
                    msg = "Expecting key"
                    raise _errmsg(msg, filename, s, end)

                # Reduce memory consumption
                key = memoize(key, key)
                colon_idx: int = end
                end = skip_comments(filename, s, end)
                if s[end:end + 1] != ":":
                    msg = "Expecting colon"
                    raise _errmsg(msg, filename, s, colon_idx)

                end = skip_comments(filename, s, end + 1)
                value, end = scan_value(filename, s, end)
                append_pair((key, value))
                comma_idx: int = end
                end = skip_comments(filename, s, end)
                try:
                    nextchar = s[end]
                except IndexError:
                    msg = "Unterminated object"
                    raise _errmsg(msg, filename, s, obj_idx, end) from None

                if nextchar == ",":
                    comma_idx = end
                    end = skip_comments(filename, s, end + 1)
                elif nextchar == "}":
                    return mapping_hook(pairs), end + 1
                elif end == comma_idx:
                    msg = "Expecting comma"
                    raise _errmsg(msg, filename, s, comma_idx)
                elif not allow_missing_commas:
                    msg = "Missing commas are not allowed"
                    raise _errmsg(msg, filename, s, comma_idx)

                try:
                    nextchar = s[end]
                except IndexError:
                    msg = "Unterminated object"
                    raise _errmsg(msg, filename, s, obj_idx, end) from None

                if nextchar == "}":
                    if not allow_trailing_comma:
                        msg = "Trailing comma is not allowed"
                        raise _errmsg(
                            msg, filename, s, comma_idx, comma_idx + 1,
                        )

                    return mapping_hook(pairs), end + 1

        def scan_array(filename: str, s: str, end: int) -> tuple[Any, int]:
            arr_idx: int = end - 1
            end = skip_comments(filename, s, end)
            try:
                nextchar: str = s[end]
            except IndexError:
                msg: str = "Unterminated array"
                raise _errmsg(msg, filename, s, arr_idx, end) from None

            if nextchar == "]":
                return sequence_hook([]), end + 1

            values: list[Any] = []
            append_value: Callable[[Any], None] = values.append
            while True:
                value, end = scan_value(filename, s, end)
                append_value(value)
                comma_idx: int = end
                end = skip_comments(filename, s, end)
                try:
                    nextchar = s[end]
                except IndexError:
                    msg = "Unterminated array"
                    raise _errmsg(msg, filename, s, arr_idx, end) from None

                if nextchar == ",":
                    comma_idx = end
                    end = skip_comments(filename, s, end + 1)
                elif nextchar == "]":
                    return sequence_hook(values), end + 1
                elif end == comma_idx:
                    msg = "Expecting comma"
                    raise _errmsg(msg, filename, s, comma_idx)
                elif not allow_missing_commas:
                    msg = "Missing commas are not allowed"
                    raise _errmsg(msg, filename, s, comma_idx)

                try:
                    nextchar = s[end]
                except IndexError:
                    msg = "Unterminated array"
                    raise _errmsg(msg, filename, s, arr_idx, end) from None

                if nextchar == "]":
                    if not allow_trailing_comma:
                        msg = "Trailing comma is not allowed"
                        raise _errmsg(
                            msg, filename, s, comma_idx, comma_idx + 1,
                        )

                    return sequence_hook(values), end + 1

        def scan_value(filename: str, s: str, idx: int) -> tuple[Any, int]:
            try:
                nextchar = s[idx]
            except IndexError:
                msg: str = "Expecting value"
                raise _errmsg(msg, filename, s, idx) from None

            value: Any
            if nextchar == '"':
                value, end = scan_string(filename, s, idx + 1)
            elif nextchar == "{":
                value, end = scan_object(filename, s, idx + 1)
            elif nextchar == "[":
                value, end = scan_array(filename, s, idx + 1)
            elif nextchar == "n" and s[idx:idx + 4] == "null":
                value, end = None, idx + 4
            elif nextchar == "t" and s[idx:idx + 4] == "true":
                value, end = bool_hook(True), idx + 4  # noqa: FBT003
            elif nextchar == "f" and s[idx:idx + 5] == "false":
                value, end = bool_hook(False), idx + 5  # noqa: FBT003
            elif number := _match_number(s, idx):
                integer, frac, exp = number.groups()
                end = number.end()
                if not frac and not exp:
                    try:
                        value = int(integer)
                    except ValueError:
                        msg = "Number is too big"
                        raise _errmsg(msg, filename, s, idx, end) from None

                    value = int_hook(value)
                else:
                    try:
                        value = parse_float(
                            integer + (frac or "") + (exp or ""),
                        )
                    except InvalidOperation:
                        msg = "Number is too big"
                        raise _errmsg(msg, filename, s, idx, end) from None

                    if not use_decimal and isinf(value):
                        msg = "Big numbers require decimal"
                        raise _errmsg(msg, filename, s, idx, end)

                    value = float_hook(value)
            elif nextchar == "N" and s[idx:idx + 3] == "NaN":
                if not allow_nan_and_infinity:
                    msg = "NaN is not allowed"
                    raise _errmsg(msg, filename, s, idx, idx + 3)

                value, end = float_hook(parse_float("NaN")), idx + 3
            elif nextchar == "I" and s[idx:idx + 8] == "Infinity":
                if not allow_nan_and_infinity:
                    msg = "Infinity is not allowed"
                    raise _errmsg(msg, filename, s, idx, idx + 8)

                value, end = float_hook(parse_float("Infinity")), idx + 8
            elif nextchar == "-" and s[idx:idx + 9] == "-Infinity":
                if not allow_nan_and_infinity:
                    msg = "-Infinity is not allowed"
                    raise _errmsg(msg, filename, s, idx, idx + 9)

                value, end = float_hook(parse_float("-Infinity")), idx + 9
            else:
                msg = "Expecting value"
                raise _errmsg(msg, filename, s, idx)

            return value, end

        def scanner(filename: str, s: str) -> Any:
            if s.startswith("\ufeff"):
                msg: str = "Unexpected UTF-8 BOM"
                raise _errmsg(msg, filename, s, 0, 1)

            end: int = skip_comments(filename, s, 0)
            try:
                obj, end = scan_value(filename, s, end)
            except JSONSyntaxError as exc:
                raise exc.with_traceback(None) from None
            finally:
                memo.clear()

            if (end := skip_comments(filename, s, end)) < len(s):
                msg = "Expecting end of file"
                raise _errmsg(msg, filename, s, end)

            return obj

        return scanner


class Decoder:
    """A configurable JSON decoder.

    .. versionchanged:: 2.0 Added ``types``.

    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param hooks: the :ref:`hooks <using_hooks>` used for transforming data
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`
    """

    def __init__(
        self,
        *,
        allow: Container[str] = NOTHING,
        hooks: dict[str, _Hook] | None = None,
        use_decimal: bool = False,
    ) -> None:
        """Create a new JSON decoder."""
        allow_surrogates: bool = "surrogates" in allow
        self._errors: str = "surrogatepass" if allow_surrogates else "strict"

        if hooks is None:
            hooks = {}

        self._scanner: _Scanner = make_scanner(
            hooks.get("bool", bool), hooks.get("float", float),
            hooks.get("int", int), hooks.get("mapping", dict),
            hooks.get("sequence", list), hooks.get("str", str),
            "comments" in allow, "missing_commas" in allow,
            "nan_and_infinity" in allow, allow_surrogates,
            "trailing_comma" in allow, "unquoted_keys" in allow, use_decimal,
        )

    def read(self, filename: _StrPath) -> Any:
        """Deserialize a JSON file to a Python object.

        :param filename: the path to the JSON file
        :raises JSONSyntaxError: if the JSON file is invalid
        :raises RecursionError: if the JSON file is too deeply nested
        :raises UnicodeDecodeError: when failing to decode the file
        :return: a Python object

        Example:
            >>> import jsonyx as json
            >>> from pathlib import Path
            >>> from tempfile import TemporaryDirectory
            >>> with TemporaryDirectory() as tmpdir:
            ...     filename = Path(tmpdir) / "file.json"
            ...     _ = filename.write_text('["filesystem API"]', "utf_8")
            ...     json.Decoder().read(filename)
            ...
            ['filesystem API']

        """
        return self.loads(Path(filename).read_bytes(), filename=filename)

    def load(
        self, fp: _SupportsRead[bytes | str], *, root: _StrPath = ".",
    ) -> Any:
        """Deserialize an open JSON file to a Python object.

        :param fp: an open JSON file
        :param root: the path to the archive containing this JSON file
        :raises JSONSyntaxError: if the JSON file is invalid
        :raises RecursionError: if the JSON file is too deeply nested
        :raises UnicodeDecodeError: when failing to decode the file
        :return: a Python object

        Example:
            >>> import jsonyx as json
            >>> from io import StringIO
            >>> decoder = json.Decoder()
            >>> io = StringIO('["streaming API"]')
            >>> decoder.load(io)
            ['streaming API']

        """
        name: str | None
        if name := getattr(fp, "name", None):
            return self.loads(fp.read(), filename=Path(root) / name)

        return self.loads(fp.read())

    def loads(
        self, s: bytearray | bytes | str, *, filename: _StrPath = "<string>",
    ) -> Any:
        """Deserialize a JSON string to a Python object.

        :param s: a JSON string
        :param filename: the path to the JSON file
        :raises JSONSyntaxError: if the JSON string is invalid
        :raises RecursionError: if the JSON string is too deeply nested
        :raises UnicodeDecodeError: when failing to decode the string
        :return: a Python object

        Example:
            >>> import jsonyx as json
            >>> decoder = json.Decoder()
            >>> decoder.loads('{"foo": ["bar", null, 1.0, 2]}')
            {'foo': ['bar', None, 1.0, 2]}

        .. tip:: Specify ``filename`` to display the filename in error
            messages.

        """
        filename = fspath(filename)
        if not filename.startswith("<") and not filename.endswith(">"):
            filename = realpath(filename)

        if not isinstance(s, str):
            s = s.decode(detect_encoding(s), self._errors)  # type: ignore

        return self._scanner(filename, s)  # type: ignore


Decoder.__module__ = "jsonyx"
