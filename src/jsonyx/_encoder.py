"""JSON encoder."""
from __future__ import annotations

__all__: list[str] = ["Encoder"]

import re
import sys
from io import StringIO
from pathlib import Path
from re import DOTALL, MULTILINE, VERBOSE, Match, Pattern, RegexFlag
from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from jsonyx import TruncatedSyntaxError
from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container, ItemsView, Iterable
    from os import PathLike

    _T_contra = TypeVar("_T_contra", contravariant=True)

    # pylint: disable-next=R0903
    class _SupportsWrite(Protocol[_T_contra]):
        def write(self, s: _T_contra, /) -> object:
            """Write string."""

    _Encoder = Callable[[object], str]
    _Hook = Callable[[Any], Any]
    _StrPath = PathLike[str] | str


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

_ESCAPE_CHARS: Pattern[str] = re.compile(r'["\\\x00-\x1f]', _FLAGS)
_ASCII_ESCAPE_CHARS: Pattern[str] = re.compile(r'["\\]|[^\x20-\x7e]', _FLAGS)
_NUMBER: Pattern[str] = re.compile(
    r"""
    (-?0|-?[1-9][0-9]*) # integer
    (\.[0-9]+)?         # [frac]
    ([eE][-+]?[0-9]+)?  # [exp]
    """, _FLAGS,
)

try:
    if not TYPE_CHECKING:
        from _jsonyx import make_encoder
except ImportError:
    def make_encoder(
        array_types: type | tuple[type, ...],
        bool_types: type | tuple[type, ...],
        float_types: type | tuple[type, ...],
        hook: _Hook | None,
        indent: str | None,
        int_types: type | tuple[type, ...],
        object_types: type | tuple[type, ...],
        str_types: type | tuple[type, ...],
        end: str,
        item_separator: str,
        key_separator: str,
        long_item_separator: str,
        max_indent_level: int,
        allow_nan_and_infinity: bool,
        allow_non_str_keys: bool,
        allow_surrogates: bool,
        check_circular: bool,
        ensure_ascii: bool,
        indent_leaves: bool,
        quoted_keys: bool,
        skipkeys: bool,
        sort_keys: bool,
        trailing_comma: bool,
    ) -> _Encoder:
        """Make JSON encoder."""
        markers: dict[int, object] | None = {} if check_circular else None

        if hook is None:
            def new_hook(obj: Any) -> Any:
                return obj

            hook = new_hook

        if not ensure_ascii:
            def replace(match: Match[str]) -> str:
                return _ESCAPE_DCT[match.group()]

            def encode_string(s: str) -> str:
                return f'"{_ESCAPE_CHARS.sub(replace, s)}"'
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
                return f'"{_ASCII_ESCAPE_CHARS.sub(replace, s)}"'

        def encode_float(num: Any) -> str:
            s: str = str(num)
            if _NUMBER.fullmatch(s):
                return s

            s = s.lower()
            if s == "nan":
                s = "NaN"
            elif s in {"inf", "infinity"}:
                s = "Infinity"
            elif s in {"-inf", "-infinity"}:
                s = "-Infinity"
            else:
                msg: str = f"{num!r} is not JSON serializable"
                raise ValueError(msg)

            if not allow_nan_and_infinity:
                msg = f"{num!r} is not allowed"
                raise ValueError(msg)

            return s

        def is_unindented(values: Iterable[Any], indent_level: int) -> bool:
            return indent_level >= max_indent_level or (
                not indent_leaves and not any(isinstance(hook(value), (
                    list, tuple, dict, array_types, object_types,
                )) for value in values)
            )

        def write_sequence(
            seq: Any, io: StringIO, indent_level: int, old_indent: str,
        ) -> None:
            if markers is not None:
                if (markerid := id(seq)) in markers:
                    msg: str = "Unexpected circular reference"
                    raise ValueError(msg)

                markers[markerid] = seq

            io.write("[")
            current_indent: str = old_indent
            if indent is None or is_unindented(seq, indent_level):
                indented: bool = False
                current_item_separator: str = long_item_separator
            else:
                indented = True
                indent_level += 1
                current_indent += indent
                current_item_separator = item_separator + current_indent

            first: bool = True
            for value in seq:
                if first:
                    first = False
                    if indented:
                        io.write(current_indent)
                else:
                    io.write(current_item_separator)

                try:
                    write_value(value, io, indent_level, current_indent)
                except Exception as exc:
                    if (tb := exc.__traceback__) is not None:
                        exc.__traceback__ = tb.tb_next

                    raise

            if markers is not None:
                del markers[markerid]  # type: ignore

            if not first and indented:
                if trailing_comma:
                    io.write(item_separator)

                io.write(old_indent)

            io.write("]")

        def write_mapping(
            mapping: Any,
            io: StringIO,
            indent_level: int,
            old_indent: str,
        ) -> None:
            if markers is not None:
                if (markerid := id(mapping)) in markers:
                    msg: str = "Unexpected circular reference"
                    raise ValueError(msg)

                markers[markerid] = mapping

            io.write("{")
            current_indent: str = old_indent
            if indent is None or is_unindented(mapping.values(), indent_level):
                indented: bool = False
                current_item_separator: str = long_item_separator
            else:
                indented = True
                indent_level += 1
                current_indent += indent
                current_item_separator = item_separator + current_indent

            first: bool = True
            items: ItemsView[object, object] = mapping.items()
            for key, value in sorted(items) if sort_keys else items:
                key = hook(key)  # noqa: PLW2901
                if isinstance(key, (str, str_types)):
                    s = str(key)
                else:
                    if key is None:
                        s = "null"
                    elif isinstance(key, (bool, bool_types)):
                        s = "true" if key else "false"
                    elif isinstance(key, (float, int, float_types, int_types)):
                        s = encode_float(key)
                    elif skipkeys:
                        continue
                    else:
                        msg = f"Keys must be str, not {type(key).__name__}"
                        raise TypeError(msg)

                    if not allow_non_str_keys:
                        if skipkeys:
                            continue

                        msg = "Non-string keys are not allowed"
                        raise TypeError(msg)

                if first:
                    first = False
                    if indented:
                        io.write(current_indent)
                else:
                    io.write(current_item_separator)

                if not quoted_keys and s.isidentifier() and (
                    not ensure_ascii or s.isascii()
                ):
                    io.write(s)
                else:
                    io.write(encode_string(s))

                io.write(key_separator)
                try:
                    write_value(value, io, indent_level, current_indent)
                except Exception as exc:
                    if (tb := exc.__traceback__) is not None:
                        exc.__traceback__ = tb.tb_next

                    raise

            if markers is not None:
                del markers[markerid]  # type: ignore

            if not first and indented:
                if trailing_comma:
                    io.write(item_separator)

                io.write(old_indent)

            io.write("}")

        def write_value(
            obj: object,
            io: StringIO,
            indent_level: int,
            current_indent: str,
        ) -> None:
            obj = hook(obj)
            if obj is None:
                io.write("null")
            elif isinstance(obj, (bool, bool_types)):
                io.write("true" if obj else "false")
            elif isinstance(obj, (str, str_types)):
                io.write(encode_string(str(obj)))
            elif isinstance(obj, (float, int, float_types, int_types)):
                io.write(encode_float(obj))
            elif isinstance(obj, (list, tuple, array_types)):
                try:
                    write_sequence(obj, io, indent_level, current_indent)
                except Exception as exc:
                    if (tb := exc.__traceback__) is not None:
                        exc.__traceback__ = tb.tb_next

                    raise
            elif isinstance(obj, (dict, object_types)):
                try:
                    write_mapping(obj, io, indent_level, current_indent)
                except Exception as exc:
                    if (tb := exc.__traceback__) is not None:
                        exc.__traceback__ = tb.tb_next

                    raise
            else:
                msg: str = f"{type(obj).__name__} is not JSON serializable"
                raise TypeError(msg)

        def encoder(obj: object) -> str:
            io: StringIO = StringIO()
            try:
                write_value(obj, io, 0, "\n")
            finally:
                if markers is not None:
                    markers.clear()

            io.write(end)
            return io.getvalue()

        return encoder


class Encoder:
    r"""A configurable JSON encoder.

    .. versionchanged:: 2.0

        - Added ``commas``, ``indent_leaves``, ``max_indent_level``,
          ``quoted_keys`` and ``types``.
        - Made :class:`tuple` serializable by default instead of
          :class:`enum.Enum` and :class:`decimal.Decimal`.
        - Replaced ``item_separator`` and ``key_separator`` with
          ``separators``.

    .. versionchanged:: 2.1 Added ``check_circular``, ``hook`` and
        ``skipkeys``.

    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param check_circular: check for circular references
    :param commas: separate items by commas when indented
    :param hook: the :ref:`hook <encoding_hook>` used for transforming data
    :param end: the string to append at the end
    :param ensure_ascii: escape non-ASCII characters
    :param indent: the number of spaces or string to indent with
    :param indent_leaves: indent leaf objects and arrays
    :param max_indent_level: the level up to which to indent
    :param quoted_keys: quote keys which are :ref:`identifiers <identifiers>`
    :param separators: the item and key separator
    :param skipkeys: skip non-string keys
    :param sort_keys: sort the keys of objects
    :param trailing_comma: add a trailing comma when indented
    :param types: a dictionary of :ref:`additional types <protocol_types>`

    .. note:: The item separator is automatically stripped when indented.
    .. warning:: Avoid specifying ABCs for ``types``, that is very slow.
    .. seealso:: :class:`jsonyx.Decoder` for a decoder.
    """

    def __init__(
        self,
        *,
        allow: Container[str] = NOTHING,
        check_circular: bool = True,
        commas: bool = True,
        hook: _Hook | None = None,
        end: str = "\n",
        ensure_ascii: bool = False,
        indent: int | str | None = None,
        indent_leaves: bool = True,
        max_indent_level: int | None = None,
        quoted_keys: bool = True,
        separators: tuple[str, str] = (", ", ": "),
        skipkeys: bool = False,
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

        self._encoder: _Encoder = make_encoder(
            types.get("array", ()), types.get("bool", ()),
            types.get("float", ()), hook, indent, types.get("int", ()),
            types.get("object", ()), types.get("str", ()), end,
            item_separator, key_separator, long_item_separator,
            max_indent_level, "nan_and_infinity" in allow,
            "non_str_keys" in allow, allow_surrogates, check_circular,
            ensure_ascii, indent_leaves, quoted_keys, skipkeys, sort_keys,
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
        :raises OSError: if the file can't be opened
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
