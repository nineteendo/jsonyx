# Copyright (C) 2024 Nice Zombies
"""JSON decoder."""
# TODO(Nice Zombies): add specification
from __future__ import annotations

__all__: list[str] = [
    "Decoder",
    "DuplicateKey",
    "JSONSyntaxError",
    "detect_encoding",
]

import re
from codecs import (
    BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE,
)
from decimal import Decimal, InvalidOperation
from math import isinf
from os import fspath
from os.path import realpath
from pathlib import Path
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from shutil import get_terminal_size
from typing import TYPE_CHECKING, Any, Literal

from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container

    from _typeshed import StrPath, SupportsRead

    _AllowList = Container[Literal[
        "comments", "duplicate_keys", "missing_commas", "nan_and_infinity",
        "surrogates", "trailing_comma",
    ] | str]


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

_match_chunk: Callable[[str, int], Match[str] | None] = re.compile(
    r'[^"\\\x00-\x1f]+', _FLAGS,
).match
_match_line_end: Callable[[str, int], Match[str] | None] = re.compile(
    r"[^\n\r]+", _FLAGS,
).match
_match_number: Callable[[str, int], Match[str] | None] = re.compile(
    r"""
    (-?0|-?[1-9]\d*) # integer
    (\.\d+)?         # [frac]
    ([eE][-+]?\d+)?  # [exp]
    """, _FLAGS,
).match
_match_unquoted_key: Callable[[str, int], Match[str] | None] = re.compile(
    r"(?:\w+|[^\x00-\x7f]+)+", _FLAGS,
).match
_match_whitespace: Callable[[str, int], Match[str] | None] = re.compile(
    r"[ \t\n\r]+", _FLAGS,
).match


def _get_err_context(doc: str, start: int, end: int) -> tuple[int, str, int]:
    line_start: int = max(
        doc.rfind("\n", 0, start), doc.rfind("\r", 0, start),
    ) + 1
    if match := _match_line_end(doc, start):
        line_end: int = match.end()
    else:
        line_end = start

    if (end := min(max(start + 1, line_end), end)) == start:
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
    esc: str = s[end:end + 4]
    if len(esc) == 4 and esc[1] not in "xX":
        try:
            return int(esc, 16)
        except ValueError:
            pass

    msg: str = "Expecting 4 hex digits"
    raise _errmsg(msg, filename, s, end, -4)


try:
    if not TYPE_CHECKING:
        from _jsonyx import DuplicateKey
except ImportError:
    class DuplicateKey(str):
        """A key that can appear multiple times in a dictionary.

        >>> import jsonyx as json
        >>> {json.DuplicateKey('key'): 'value 1', json.DuplicateKey('key'): 'value 2'}
        {'key': 'value 1', 'key': 'value 2'}

        See :data:`jsonyx.allow.DUPLICATE_KEYS` for loading a dictionary with
        duplicate keys.

        .. tip::
            To retrieve the value of a duplicate key, you can
            :ref:`use a multi dict <use_multidict>`.
        """

        __slots__: tuple[()] = ()

        def __hash__(self) -> int:
            """Return hash."""
            return id(self)

    DuplicateKey.__module__ = "jsonyx"


class JSONSyntaxError(SyntaxError):
    """Invalid JSON (query) syntax.

    :param msg: an error message
    :type msg: str
    :param filename: the path to the JSON file
    :type filename: str
    :param doc: a JSON string
    :type doc: str
    :param start: the start position
    :type start: int
    :param end: the end position, defaults to ``0``
    :type end: int, optional
    """

    def __init__(
        self, msg: str, filename: str, doc: str, start: int, end: int = 0,
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
        super().__init__(
            msg, (filename, lineno, offset, text, end_lineno, end_offset),
        )
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
    :type b: bytearray | bytes
    :return: the detected encoding
    :rtype: str

    >>> import jsonyx as json
    >>> b = b'\x00"\x00f\x00o\x00o\x00"'
    >>> b.decode(json.detect_encoding(b))
    '"foo"'

    .. note::
        Supports only ``"utf_8"``, ``"utf_8-sig"``, ``"utf_16"``,
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
        allow_comments: bool,  # noqa: FBT001
        allow_duplicate_keys: bool,  # noqa: FBT001
        allow_missing_commas: bool,  # noqa: FBT001
        allow_nan_and_infinity: bool,  # noqa: FBT001
        allow_surrogates: bool,  # noqa: FBT001
        allow_trailing_comma: bool,  # noqa: FBT001
        allow_unquoted_keys: bool,  # noqa: FBT001
        use_decimal: bool,  # noqa: FBT001
    ) -> Callable[[str, str], Any]:
        """Make JSON scanner."""
        memo: dict[str, str] = {}
        memoize: Callable[[str, str], str] = memo.setdefault
        parse_float: Callable[
            [str], Decimal | float,
        ] = Decimal if use_decimal else float

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

        def scan_string(filename: str, s: str, end: int) -> tuple[str, int]:
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
                    return "".join(chunks), end + 1

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

        def scan_object(
            filename: str, s: str, end: int,
        ) -> tuple[dict[str, Any], int]:
            obj_idx: int = end - 1
            end = skip_comments(filename, s, end)
            try:
                nextchar: str = s[end]
            except IndexError:
                msg: str = "Unterminated object"
                raise _errmsg(msg, filename, s, obj_idx, end) from None

            if nextchar == "}":
                return {}, end + 1

            result: dict[str, Any] = {}
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
                    msg = "Expecting string"
                    raise _errmsg(msg, filename, s, end)

                if key not in result:
                    # Reduce memory consumption
                    key = memoize(key, key)
                elif not allow_duplicate_keys:
                    msg = "Duplicate keys are not allowed"
                    raise _errmsg(msg, filename, s, key_idx, end)
                else:
                    key = DuplicateKey(key)

                colon_idx: int = end
                end = skip_comments(filename, s, end)
                if s[end:end + 1] != ":":
                    msg = "Expecting colon"
                    raise _errmsg(msg, filename, s, colon_idx)

                end = skip_comments(filename, s, end + 1)
                result[key], end = scan_value(filename, s, end)
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
                    return result, end + 1
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

                    return result, end + 1

        def scan_array(
            filename: str, s: str, end: int,
        ) -> tuple[list[Any], int]:
            arr_idx: int = end - 1
            end = skip_comments(filename, s, end)
            try:
                nextchar: str = s[end]
            except IndexError:
                msg: str = "Unterminated array"
                raise _errmsg(msg, filename, s, arr_idx, end) from None

            if nextchar == "]":
                return [], end + 1

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
                    return values, end + 1
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

                    return values, end + 1

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
                value, end = True, idx + 4
            elif nextchar == "f" and s[idx:idx + 5] == "false":
                value, end = False, idx + 5
            elif number := _match_number(s, idx):
                integer, frac, exp = number.groups()
                end = number.end()
                if frac or exp:
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
                else:
                    value = int(integer)
            elif nextchar == "N" and s[idx:idx + 3] == "NaN":
                if not allow_nan_and_infinity:
                    msg = "NaN is not allowed"
                    raise _errmsg(msg, filename, s, idx, idx + 3)

                value, end = parse_float("NaN"), idx + 3
            elif nextchar == "I" and s[idx:idx + 8] == "Infinity":
                if not allow_nan_and_infinity:
                    msg = "Infinity is not allowed"
                    raise _errmsg(msg, filename, s, idx, idx + 8)

                value, end = parse_float("Infinity"), idx + 8
            elif nextchar == "-" and s[idx:idx + 9] == "-Infinity":
                if not allow_nan_and_infinity:
                    msg = "-Infinity is not allowed"
                    raise _errmsg(msg, filename, s, idx, idx + 9)

                value, end = parse_float("-Infinity"), idx + 9
            else:
                msg = "Expecting value"
                raise _errmsg(msg, filename, s, idx)

            return value, end

        def scanner(filename: str, s: str) -> Any:
            if s.startswith("\ufeff"):
                msg: str = "Unexpected UTF-8 BOM"
                raise JSONSyntaxError(msg, filename, s, 0)

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

    :param allow: the allowed JSON deviations, defaults to
                  :data:`jsonyx.allow.NOTHING`
    :type allow: Container[str], optional
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`,
                        defaults to ``False``
    :type use_decimal: bool, optional
    """

    def __init__(
        self, *, allow: _AllowList = NOTHING, use_decimal: bool = False,
    ) -> None:
        """Create a new JSON decoder."""
        allow_surrogates: bool = "surrogates" in allow
        self._errors: str = "surrogatepass" if allow_surrogates else "strict"
        self._scanner: Callable[[str, str], tuple[Any]] = make_scanner(
            "comments" in allow, "duplicate_keys" in allow,
            "missing_commas" in allow, "nan_and_infinity" in allow,
            allow_surrogates, "trailing_comma" in allow,
            "unquoted_keys" in allow, use_decimal,
        )

    def read(self, filename: StrPath) -> Any:
        """Deserialize a JSON file to a Python object.

        :param filename: the path to the JSON file
        :type filename: StrPath
        :raises JSONSyntaxError: if the JSON file is invalid
        :return: a Python object
        :rtype: Any

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
        self, fp: SupportsRead[bytes | str], *, root: StrPath = ".",
    ) -> Any:
        """Deserialize an open JSON file to a Python object.

        :param fp: an open JSON file
        :type fp: SupportsRead[bytes | str]
        :param root: the path to the archive containing this JSON file,
                     defaults to ``"."``
        :type root: StrPath, optional
        :raises JSONSyntaxError: if the JSON file is invalid
        :return: a Python object
        :rtype: Any

        >>> import jsonyx as json
        >>> from io import StringIO
        >>> io = StringIO('["streaming API"]')
        >>> json.Decoder().load(io)
        ['streaming API']
        """
        name: str | None
        if name := getattr(fp, "name", None):
            return self.loads(fp.read(), filename=Path(root) / name)

        return self.loads(fp.read())

    def loads(
        self, s: bytearray | bytes | str, *, filename: StrPath = "<string>",
    ) -> Any:
        """Deserialize a JSON string to a Python object.

        :param s: a JSON string
        :type s: bytearray | bytes | str
        :param filename: the path to the JSON file, defaults to ``"<string>"``
        :type filename: StrPath, optional
        :raises JSONSyntaxError: if the JSON string is invalid
        :return: a Python object
        :rtype: Any

        >>> import jsonyx as json
        >>> json.Decoder().loads('{"foo": ["bar", null, 1.0, 2]}')
        {'foo': ['bar', None, 1.0, 2]}

        .. tip::
            Specify *filename* to display the filename in error messages.
        """
        filename = fspath(filename)
        if not filename.startswith("<") and not filename.endswith(">"):
            filename = realpath(filename)

        if not isinstance(s, str):
            s = s.decode(detect_encoding(s), self._errors)

        return self._scanner(filename, s)


Decoder.__module__ = "jsonyx"
