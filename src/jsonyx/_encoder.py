"""JSON encoder."""
from __future__ import annotations

__all__: list[str] = ["Encoder"]

import re
import sys
from decimal import Decimal
from io import StringIO
from math import inf, isfinite
from pathlib import Path
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from jsonyx import TruncatedSyntaxError
from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container, ItemsView
    from os import PathLike

    _T = TypeVar("_T")
    _T_contra = TypeVar("_T_contra", contravariant=True)

    # pylint: disable-next=R0903
    class _SupportsWrite(Protocol[_T_contra]):
        def write(self, s: _T_contra, /) -> object:
            """Write string."""

    _EncodeFunc = Callable[[_T], str]
    _StrPath = PathLike[str] | str
    _SubFunc = Callable[[str | Callable[[Match[str]], str], str], str]
    _WriteFunc = Callable[[str], object]


_ESCAPE_DCT: dict[str, str] = {
    **{chr(i): f"\\u{i:04x}" for i in range(0x20)},
    '"': '\\"',
    "\\": "\\\\",
    "\b": "\\b",
    "\f": "\\f",
    "\n": "\\n",
    "\r": "\\r",
    "\t": "\\t",
}
_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL

_escape: _SubFunc = re.compile(r'["\\\x00-\x1f]', _FLAGS).sub
_escape_ascii: _SubFunc = re.compile(r'["\\]|[^\x20-\x7e]', _FLAGS).sub

try:
    if not TYPE_CHECKING:
        from _jsonyx import make_encoder
except ImportError:
    def make_encoder(
        bool_types: type | tuple[type, ...],
        float_types: type | tuple[type, ...],
        indent: str | None,
        int_types: type | tuple[type, ...],
        mapping_types: type | tuple[type, ...],
        sequence_types: type | tuple[type, ...],
        str_types: type | tuple[type, ...],
        end: str,
        item_separator: str,
        long_item_separator: str,
        key_separator: str,
        max_indent_level: int,
        allow_nan_and_infinity: bool,  # noqa: FBT001
        allow_surrogates: bool,  # noqa: FBT001
        ensure_ascii: bool,  # noqa: FBT001
        indent_leaves: bool,  # noqa: FBT001
        quoted_keys: bool,  # noqa: FBT001
        sort_keys: bool,  # noqa: FBT001
        trailing_comma: bool,  # noqa: FBT001
    ) -> _EncodeFunc[object]:
        """Make JSON encoder."""
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
                return repr(num)

            if not allow_nan_and_infinity:
                msg: str = f"{num!r} is not allowed"
                raise ValueError(msg)

            if num == inf:
                return "Infinity"

            if num == -inf:
                return "-Infinity"

            return "NaN"

        def decimalstr(decimal: Decimal) -> str:
            if not decimal.is_finite():
                if decimal.is_snan():
                    msg: str = f"{decimal!r} is not JSON serializable"
                    raise ValueError(msg)

                if not allow_nan_and_infinity:
                    msg = f"{decimal!r} is not allowed"
                    raise ValueError(msg)

                if decimal.is_qnan():
                    return "NaN"

            return str(decimal)

        def write_sequence(
            seq: Any, write: _WriteFunc, indent_level: int, old_indent: str,
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
            if indent is None or indent_level >= max_indent_level or (
                not indent_leaves and not any(isinstance(
                    value, (list, tuple, dict, sequence_types, mapping_types),
                ) for value in seq)
            ):
                indented: bool = False
                current_item_separator: str = long_item_separator
            else:
                indented = True
                indent_level += 1
                current_indent += indent
                current_item_separator = item_separator + current_indent
                write(current_indent)

            first: bool = True
            for value in seq:
                if first:
                    first = False
                else:
                    write(current_item_separator)

                write_value(value, write, indent_level, current_indent)

            del markers[markerid]
            if indented:
                if trailing_comma:
                    write(item_separator)

                write(old_indent)

            write("]")

        def write_mapping(
            mapping: Any,
            write: _WriteFunc,
            indent_level: int,
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
            if indent is None or indent_level >= max_indent_level or (
                not indent_leaves and not any(isinstance(
                    value, (list, tuple, dict, sequence_types, mapping_types),
                ) for value in mapping.values())
            ):
                indented: bool = False
                current_item_separator: str = long_item_separator
            else:
                indented = True
                indent_level += 1
                current_indent += indent
                current_item_separator = item_separator + current_indent
                write(current_indent)

            first: bool = True
            items: ItemsView[object, object] = mapping.items()
            for key, value in sorted(items) if sort_keys else items:
                if not isinstance(key, (str, str_types)):
                    msg = f"Keys must be str, not {type(key).__name__}"
                    raise TypeError(msg)

                key = str(key)  # noqa: PLW2901
                if first:
                    first = False
                else:
                    write(current_item_separator)

                if not quoted_keys and key.isidentifier() and (
                    not ensure_ascii or key.isascii()
                ):
                    write(key)
                else:
                    write(encode_string(key))

                write(key_separator)
                write_value(value, write, indent_level, current_indent)

            del markers[markerid]
            if indented:
                if trailing_comma:
                    write(item_separator)

                write(old_indent)

            write("}")

        def write_value(
            obj: object,
            write: _WriteFunc,
            indent_level: int,
            current_indent: str,
        ) -> None:
            if obj is None:
                write("null")
            elif isinstance(obj, (bool, bool_types)):
                write("true" if obj else "false")
            elif isinstance(obj, (str, str_types)):
                write(encode_string(str(obj)))
            elif isinstance(obj, (int, int_types)):
                write(repr(int(obj)))  # type: ignore
            elif isinstance(obj, (float, float_types)):
                write(floatstr(float(obj)))  # type: ignore
            elif isinstance(obj, (list, tuple, sequence_types)):
                write_sequence(obj, write, indent_level, current_indent)
            elif isinstance(obj, (dict, mapping_types)):
                write_mapping(obj, write, indent_level, current_indent)
            elif isinstance(obj, Decimal):
                write(decimalstr(obj))
            else:
                msg: str = f"{type(obj).__name__} is not JSON serializable"
                raise TypeError(msg)

        def encoder(obj: object) -> str:
            io: StringIO = StringIO()
            write: _WriteFunc = io.write
            try:
                write_value(obj, write, 0, "\n")
            except (ValueError, TypeError) as exc:
                raise exc.with_traceback(None) from None
            finally:
                markers.clear()

            write(end)
            return io.getvalue()

        return encoder


class Encoder:
    r"""A configurable JSON encoder.

    .. versionchanged:: 2.0

        - Added ``commas``, ``indent_leaves``, ``max_indent_level``,
          ``quoted_keys`` and ``types``.
        - Made :class:`tuple` JSON serializable.
        - Merged ``item_separator`` and ``key_separator`` as ``separators``.

    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param commas: separate items by commas when indented
    :param end: the string to append at the end
    :param ensure_ascii: escape non-ASCII characters
    :param indent: the number of spaces or string to indent with
    :param indent_leaves: indent leaf objects and arrays
    :param max_indent_level: the level up to which to indent
    :param quoted_keys: quote keys which are :ref:`identifiers <identifiers>`
    :param separators: the item and key separator
    :param sort_keys: sort the keys of objects
    :param trailing_comma: add a trailing comma when indented
    :param types: a dictionary of :ref:`additional types <protocol_types>`

    .. note:: The item separator is automatically stripped when indented.

    .. warning:: Avoid specifying ABCs for ``types``, that is very slow.
    """

    def __init__(
        self,
        *,
        allow: Container[str] = NOTHING,
        commas: bool = True,
        end: str = "\n",
        ensure_ascii: bool = False,
        indent: int | str | None = None,
        indent_leaves: bool = True,
        max_indent_level: int | None = None,
        quoted_keys: bool = True,
        separators: tuple[str, str] = (", ", ": "),
        sort_keys: bool = False,
        trailing_comma: bool = False,
        types: dict[str, type | tuple[type, ...]] | None = None,
    ) -> None:
        """Create a new JSON encoder."""
        allow_surrogates: bool = "surrogates" in allow
        long_item_separator, key_separator = separators
        if commas:
            item_separator: str = long_item_separator.rstrip()
        else:
            item_separator = ""

        if indent is not None and isinstance(indent, int):
            indent *= " "

        if max_indent_level is None:
            max_indent_level = sys.maxsize

        if types is None:
            types = {}

        self._encoder: _EncodeFunc[object] = make_encoder(
            types.get("bool", ()), types.get("float", ()), indent,
            types.get("int", ()), types.get("mapping", ()),
            types.get("sequence", ()), types.get("str", ()), end,
            item_separator, long_item_separator, key_separator,
            max_indent_level, "nan_and_infinity" in allow, allow_surrogates,
            ensure_ascii, indent_leaves, quoted_keys, sort_keys,
            commas and trailing_comma,
        )
        self._errors: str = "surrogatepass" if allow_surrogates else "strict"

    def write(
        self, obj: object, filename: _StrPath, encoding: str = "utf-8",
    ) -> None:
        r"""Serialize a Python object to a JSON file.

        .. versionchanged:: 2.0 Added ``encoding``.

        :param obj: a Python object
        :param filename: the path to the JSON file
        :param encoding: the JSON encoding
        :raises RecursionError: if the object is too deeply nested
        :raises TypeError: for unserializable values
        :raises TruncatedSyntaxError: when failing to encode the file
        :raises ValueError: for invalid values

        Example:
            >>> import jsonyx as json
            >>> from pathlib import Path
            >>> from tempfile import TemporaryDirectory
            >>> encoder = json.Encoder()
            >>> with TemporaryDirectory() as tmpdir:
            ...     filename = Path(tmpdir) / "file.json"
            ...     encoder.write(["filesystem API"], filename)
            ...     filename.read_text("utf-8")
            ...
            '["filesystem API"]\n'

        """
        with Path(filename).open("w", -1, encoding, self._errors) as fp:
            self.dump(obj, fp)

    def dump(self, obj: object, fp: _SupportsWrite[str] | None = None) -> None:
        r"""Serialize a Python object to an open JSON file.

        :param obj: a Python object
        :param fp: an open JSON file
        :raises RecursionError: if the object is too deeply nested
        :raises TypeError: for unserializable values
        :raises TruncatedSyntaxError: when failing to write to the file
        :raises ValueError: for invalid values

        Example:
            Writing to standard output:

            >>> import jsonyx as json
            >>> encoder = json.Encoder()
            >>> import jsonyx as json
            >>> encoder.dump('"foo\bar')
            "\"foo\bar"
            >>> encoder.dump("\\")
            "\\"
            >>> encoder.dump("\u20AC")
            "€"

            Writing to an open file:

            >>> import jsonyx as json
            >>> from io import StringIO
            >>> io = StringIO()
            >>> encoder.dump(["streaming API"], io)
            >>> io.getvalue()
            '["streaming API"]\n'

        """
        s: str = self._encoder(obj)
        try:
            if fp is None:
                sys.stdout.write(s)  # Use sys.stdout to work with doctest
            else:
                fp.write(s)
        except UnicodeEncodeError as exc:
            msg: str = f"(unicode error) {exc}"
            raise TruncatedSyntaxError(
                msg, "<string>", exc.object, exc.start, exc.end,
            ) from None

    def dumps(self, obj: object) -> str:
        r"""Serialize a Python object to a JSON string.

        :param obj: a Python object
        :raises RecursionError: if the object is too deeply nested
        :raises TypeError: for unserializable values
        :raises ValueError: for invalid values
        :return: a JSON string

        Example:
            >>> import jsonyx as json
            >>> encoder = json.Encoder()
            >>> encoder.dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])
            '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'

        """
        return self._encoder(obj)


Encoder.__module__ = "jsonyx"
