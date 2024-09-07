# Copyright (C) 2024 Nice Zombies
"""JSON encoder."""
from __future__ import annotations

__all__: list[str] = ["Encoder"]

import re
from collections.abc import Mapping, Sequence
from decimal import Decimal
from io import StringIO
from math import inf, isfinite
from pathlib import Path
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from sys import stdout
from typing import TYPE_CHECKING, Literal

from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container, ItemsView

    from _typeshed import StrPath, SupportsWrite

    _AllowList = Container[Literal[
        "comments", "duplicate_keys", "missing_commas", "nan_and_infinity",
        "surrogates", "trailing_comma",
    ] | str]


_ESCAPE_DCT: dict[str, str] = {chr(i): f"\\u{i:04x}" for i in range(0x20)} | {
    '"': '\\"',
    "\\": "\\\\",
    "\b": "\\b",
    "\f": "\\f",
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
}
_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL

_escape: Callable[[Callable[[Match[str]], str], str], str] = re.compile(
    r'["\\\x00-\x1f]', _FLAGS,
).sub
_escape_ascii: Callable[[Callable[[Match[str]], str], str], str] = re.compile(
    r'["\\]|[^\x20-\x7e]', _FLAGS,
).sub

try:
    if not TYPE_CHECKING:
        from _jsonyx import make_encoder
except ImportError:
    def make_encoder(
        encode_decimal: Callable[[Decimal], str],
        indent: str | None,
        end: str,
        item_separator: str,
        long_item_separator: str,
        key_separator: str,
        add_trailing_comma: bool,  # noqa: FBT001
        allow_nan_and_infinity: bool,  # noqa: FBT001
        allow_surrogates: bool,  # noqa: FBT001
        ensure_ascii: bool,  # noqa: FBT001
        indent_leaves: bool,  # noqa: FBT001
        quote_keys: bool,  # noqa: FBT001
        sort_keys: bool,  # noqa: FBT001
    ) -> Callable[[object], str]:
        """Make JSON encoder."""
        float_repr: Callable[[float], str] = float.__repr__
        int_repr: Callable[[int], str] = int.__repr__
        markers: dict[int, object] = {}

        if not ensure_ascii:
            def replace(match: Match[str]) -> str:
                return _ESCAPE_DCT[match.group()]

            def encode_string(s: str) -> str:
                return f'"{_escape(replace, s)}"'
        else:
            def replace(match: Match[str]) -> str:
                s: str = match.group()
                try:
                    return _ESCAPE_DCT[s]
                except KeyError:
                    if (uni := ord(s)) >= 0x10000:
                        # surrogate pair
                        uni -= 0x10000
                        uni1: int = 0xd800 | ((uni >> 10) & 0x3ff)
                        uni2: int = 0xdc00 | (uni & 0x3ff)
                        return f"\\u{uni1:04x}\\u{uni2:04x}"

                    if 0xd800 <= uni <= 0xdfff and not allow_surrogates:
                        msg: str = "Surrogates are not allowed"
                        raise ValueError(msg) from None

                    return f"\\u{uni:04x}"

            def encode_string(s: str) -> str:
                return f'"{_escape_ascii(replace, s)}"'

        def floatstr(num: float) -> str:
            if isfinite(num):
                return float_repr(num)

            if not allow_nan_and_infinity:
                msg: str = f"{num!r} is not allowed"
                raise ValueError(msg)

            if num == inf:
                return "Infinity"

            if num == -inf:
                return "-Infinity"

            return "NaN"

        def write_sequence(
            seq: Sequence[object], write: Callable[[str], object],
            old_indent: str,
        ) -> None:
            if not seq:
                write("[]")
                return

            if (markerid := id(seq)) in markers:
                msg: str = "Unexpected circular reference"
                raise ValueError(msg)

            markers[markerid] = seq
            write("[")
            current_indent: str = old_indent
            if indent is None or (not indent_leaves and all(
                value is None or isinstance(value, (Decimal, float, int, str))
                for value in seq
            )):
                indented: bool = False
                current_item_separator: str = long_item_separator
            else:
                indented = True
                current_indent += indent
                current_item_separator = item_separator + current_indent
                write(current_indent)

            first: bool = True
            for value in seq:
                if first:
                    first = False
                else:
                    write(current_item_separator)

                write_value(value, write, current_indent)

            del markers[markerid]
            if indented:
                if add_trailing_comma:
                    write(item_separator)

                write(old_indent)

            write("]")

        def write_dict(
            mapping: Mapping[object, object], write: Callable[[str], object],
            old_indent: str,
        ) -> None:
            if not mapping:
                write("{}")
                return

            if (markerid := id(mapping)) in markers:
                msg: str = "Unexpected circular reference"
                raise ValueError(msg)

            markers[markerid] = mapping
            write("{")
            current_indent: str = old_indent
            if indent is None or (not indent_leaves and all(
                value is None or isinstance(value, (Decimal, float, int, str))
                for value in mapping.values()
            )):
                indented: bool = False
                current_item_separator: str = long_item_separator
            else:
                indented = True
                current_indent += indent
                current_item_separator = item_separator + current_indent
                write(current_indent)

            first: bool = True
            items: ItemsView[object, object] = mapping.items()
            for key, value in sorted(items) if sort_keys else items:
                if not isinstance(key, str):
                    msg = f"Keys must be str, not {type(key).__name__}"
                    raise TypeError(msg)

                if first:
                    first = False
                else:
                    write(current_item_separator)

                if not quote_keys and key.isidentifier() and (
                    not ensure_ascii or key.isascii()
                ):
                    write(key)
                else:
                    write(encode_string(key))

                write(key_separator)
                write_value(value, write, current_indent)

            del markers[markerid]
            if indented:
                if add_trailing_comma:
                    write(item_separator)

                write(old_indent)

            write("}")

        def write_value(
            obj: object, write: Callable[[str], object], current_indent: str,
        ) -> None:
            if isinstance(obj, str):
                write(encode_string(obj))
            elif obj is None:
                write("null")
            elif isinstance(obj, int):
                if obj is True:
                    write("true")
                elif obj is False:
                    write("false")
                else:
                    write(int_repr(obj))
            elif isinstance(obj, float):
                write(floatstr(obj))
            elif isinstance(obj, Sequence) and not isinstance(
                obj, (bytearray, bytes, memoryview, str),
            ):
                write_sequence(obj, write, current_indent)  # type: ignore
            elif isinstance(obj, Mapping):
                write_dict(obj, write, current_indent)  # type: ignore
            elif isinstance(obj, Decimal):
                write(encode_decimal(obj))
            else:
                msg: str = (
                    f"{type(obj).__name__} is not JSON "  # type: ignore
                    "serializable"
                )
                raise TypeError(msg)

        def encoder(obj: object) -> str:
            io: StringIO = StringIO()
            write: Callable[[str], object] = io.write
            try:
                write_value(obj, write, "\n")
            except (ValueError, TypeError) as exc:
                raise exc.with_traceback(None) from None
            finally:
                markers.clear()

            write(end)
            return io.getvalue()

        return encoder


class Encoder:
    r"""A configurable JSON encoder.

    :param add_commas: separate items by commas when indented, defaults to
                       ``True``
    :type add_commas: bool, optional
    :param add_trailing_comma: add a trailing comma when indented, defaults to
                               ``False``
    :type add_trailing_comma: bool, optional
    :param allow: the allowed JSON deviations, defaults to
                  :data:`jsonyx.allow.NOTHING`
    :type allow: Container[str], optional
    :param end: the string to append at the end, defaults to ``"\n"``
    :type end: str, optional
    :param ensure_ascii: escape non-ASCII characters, defaults to ``False``
    :type ensure_ascii: bool, optional
    :param indent: the number of spaces or string to indent with, defaults to
                   ``None``
    :type indent: int | str | None, optional
    :param indent_leaves: indent leaf objects and arrays, defaults to ``False``
    :type indent_leaves: bool, optional
    :param quote_keys: quote keys which are identifiers, defaults to ``True``
    :type quote_keys: bool, optional
    :param separators: the item and key separator, defaults to ``(", ", ": ")``
    :type separators: tuple[str, str], optional
    :param sort_keys: sort the keys of objects, defaults to ``False``
    :type sort_keys: bool, optional

    .. note::
        The item separator is automatically stripped when indented.

    .. versionchanged:: 2.0
        Added *add_commas*, *quote_keys*, *indent_leaves*.
        Merged *item_separator* and *key_separator* as *separators*.
        Renamed *trailing_comma* to *add_trailing_comma*.
    """

    def __init__(
        self,
        *,
        add_commas: bool = True,
        add_trailing_comma: bool = False,
        allow: _AllowList = NOTHING,
        end: str = "\n",
        ensure_ascii: bool = False,
        indent: int | str | None = None,
        indent_leaves: bool = False,
        quote_keys: bool = True,
        separators: tuple[str, str] = (", ", ": "),
        sort_keys: bool = False,
    ) -> None:
        """Create a new JSON encoder."""
        allow_nan_and_infinity: bool = "nan_and_infinity" in allow
        allow_surrogates: bool = "surrogates" in allow
        decimal_str: Callable[[Decimal], str] = Decimal.__str__

        long_item_separator, key_separator = separators
        if add_commas:
            item_separator: str = long_item_separator.rstrip()
        else:
            item_separator = ""

        if indent is not None and isinstance(indent, int):
            indent = " " * indent

        def encode_decimal(decimal: Decimal) -> str:
            if not decimal.is_finite():
                if decimal.is_snan():
                    msg: str = f"{decimal!r} is not JSON serializable"
                    raise ValueError(msg)

                if not allow_nan_and_infinity:
                    msg = f"{decimal!r} is not allowed"
                    raise ValueError(msg)

                if decimal.is_qnan():
                    return "NaN"

            return decimal_str(decimal)

        self._encoder: Callable[[object], str] = make_encoder(
            encode_decimal, indent, end, item_separator, long_item_separator,
            key_separator, add_commas and add_trailing_comma,
            allow_nan_and_infinity, allow_surrogates, ensure_ascii,
            indent_leaves, quote_keys, sort_keys,
        )
        self._errors: str = "surrogatepass" if allow_surrogates else "strict"

    def write(self, obj: object, filename: StrPath) -> None:
        r"""Serialize a Python object to a JSON file.

        :param obj: a Python object
        :type obj: object
        :param filename: the path to the JSON file
        :type filename: StrPath
        :raises TypeError: for unserializable values
        :raises ValueError: for invalid values

        >>> import jsonyx as json
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> with TemporaryDirectory() as tmpdir:
        ...     filename = Path(tmpdir) / "file.json"
        ...     json.Encoder().write(["filesystem API"], filename)
        ...     filename.read_text("utf_8")
        ...
        '["filesystem API"]\n'
        """
        Path(filename).write_text(self._encoder(obj), "utf_8", self._errors)

    def dump(self, obj: object, fp: SupportsWrite[str] = stdout) -> None:
        r"""Serialize a Python object to an open JSON file.

        :param obj: a Python object
        :type obj: object
        :param fp: an open JSON file, defaults to :data:`sys.stdout`
        :type fp: SupportsWrite[str], optional
        :raises TypeError: for unserializable values
        :raises ValueError: for invalid values

        >>> import jsonyx as json
        >>> encoder = json.Encoder()
        >>> encoder.dump(["foo", {"bar": ("baz", None, 1.0, 2)}])
        ["foo", {"bar": ["baz", null, 1.0, 2]}]
        >>> from io import StringIO
        >>> io = StringIO()
        >>> encoder.dump(["streaming API"], io)
        >>> io.getvalue()
        '["streaming API"]\n'

        .. warning::
            To pretty-print unpaired surrogates, you need to use
            :data:`jsonyx.allow.SURROGATES` and ``ensure_ascii=True``.
        """
        fp.write(self._encoder(obj))

    def dumps(self, obj: object) -> str:
        r"""Serialize a Python object to a JSON string.

        :param obj: a Python object
        :type obj: object
        :raises TypeError: for unserializable values
        :raises ValueError: for invalid values
        :return: a JSON string
        :rtype: str

        >>> import jsonyx as json
        >>> json.Encoder().dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])
        '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'
        """
        return self._encoder(obj)


Encoder.__module__ = "jsonyx"
