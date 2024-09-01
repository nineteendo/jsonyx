# Copyright (C) 2024 Nice Zombies
"""JSON encoder."""
from __future__ import annotations

__all__: list[str] = ["make_encoder"]

import re
from collections.abc import Mapping, Sequence
from decimal import Decimal
from io import StringIO
from math import inf, isfinite
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, ItemsView

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
        full_item_separator: str,
        key_separator: str,
        allow_nan_and_infinity: bool,  # noqa: FBT001
        allow_surrogates: bool,  # noqa: FBT001
        ensure_ascii: bool,  # noqa: FBT001
        indent_leaves: bool,  # noqa: FBT001
        sort_keys: bool,  # noqa: FBT001
        trailing_comma: bool,  # noqa: FBT001
        unquoted_keys: bool,  # noqa: FBT001
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
                current_item_separator: str = full_item_separator
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
                if trailing_comma:
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
                current_item_separator: str = full_item_separator
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

                if unquoted_keys and key.isidentifier() and (
                    not ensure_ascii or key.isascii()
                ):
                    write(key)
                else:
                    write(encode_string(key))

                write(key_separator)
                write_value(value, write, current_indent)

            del markers[markerid]
            if indented:
                if trailing_comma:
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
            fp: StringIO = StringIO()
            write: Callable[[str], object] = fp.write
            try:
                write_value(obj, write, "\n")
            except (ValueError, TypeError) as exc:
                raise exc.with_traceback(None) from None
            finally:
                markers.clear()

            write(end)
            return fp.getvalue()

        return encoder
