"""JSON encoder."""
from __future__ import annotations

__all__: list[str] = ["Encoder"]

import re
import sys
from io import StringIO
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
    _Hook = Callable[[Any], Any]
    _MatchFunc = Callable[[str], Match[str] | None]
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
_match_number: _MatchFunc = re.compile(
    r"""
    (-?0|-?[1-9][0-9]*) # integer
    (\.[0-9]+)?         # [frac]
    ([eE][-+]?[0-9]+)?  # [exp]
    """, _FLAGS,
).fullmatch

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
    ) -> _EncodeFunc[object]:
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

        def encode_float(num: Any) -> str:
            s: str = str(num)
            if _match_number(s):
                return s

            if s.lower() == "nan":
                s = "NaN"
            elif s.lower() in {"inf", "infinity"}:
                s = "Infinity"
            elif s.lower() in {"-inf", "-infinity"}:
                s = "-Infinity"
            else:
                msg: str = f"{num!r} is not JSON serializable"
                raise ValueError(msg)

            if not allow_nan_and_infinity:
                msg = f"{num!r} is not allowed"
                raise ValueError(msg)

            return s

        def write_sequence(
            seq: Any, write: _WriteFunc, indent_level: int, old_indent: str,
        ) -> None:
            if markers is not None:
                if (markerid := id(seq)) in markers:
                    msg: str = "Unexpected circular reference"
                    raise ValueError(msg)

                markers[markerid] = seq

            write("[")
            current_indent: str = old_indent
            if indent is None or indent_level >= max_indent_level or (
                not indent_leaves and not any(isinstance(hook(value), (
                    list, tuple, dict, array_types, object_types,
                )) for value in seq)
            ):
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
                        write(current_indent)
                else:
                    write(current_item_separator)

                write_value(value, write, indent_level, current_indent)

            if markers is not None:
                del markers[markerid]  # type: ignore

            if not first and indented:
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
            if markers is not None:
                if (markerid := id(mapping)) in markers:
                    msg: str = "Unexpected circular reference"
                    raise ValueError(msg)

                markers[markerid] = mapping

            write("{")
            current_indent: str = old_indent
            if indent is None or indent_level >= max_indent_level or (
                not indent_leaves and not any(isinstance(hook(value), (
                    list, tuple, dict, array_types, object_types,
                )) for value in mapping.values())
            ):
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
                new_key = hook(key)
                if isinstance(new_key, (str, str_types)):
                    s = str(new_key)
                else:
                    if new_key is None:
                        s = "null"
                    elif isinstance(new_key, (bool, bool_types)):
                        s = "true" if new_key else "false"
                    elif isinstance(new_key, (
                        float, int, float_types, int_types,
                    )):
                        s = encode_float(new_key)  # type: ignore
                    elif skipkeys:
                        continue
                    else:
                        msg = f"Keys must be str, not {type(new_key).__name__}"
                        raise TypeError(msg)

                    if not allow_non_str_keys:
                        if skipkeys:
                            continue

                        msg = "Non-string keys are not allowed"
                        raise TypeError(msg)

                if first:
                    first = False
                    if indented:
                        write(current_indent)
                else:
                    write(current_item_separator)

                if not quoted_keys and s.isidentifier() and (
                    not ensure_ascii or s.isascii()
                ):
                    write(s)
                else:
                    write(encode_string(s))

                write(key_separator)
                write_value(value, write, indent_level, current_indent)

            if markers is not None:
                del markers[markerid]  # type: ignore

            if not first and indented:
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
            obj = hook(obj)
            if obj is None:
                write("null")
            elif isinstance(obj, (bool, bool_types)):
                write("true" if obj else "false")
            elif isinstance(obj, (str, str_types)):
                write(encode_string(str(obj)))
            elif isinstance(obj, (float, int, float_types, int_types)):
                write(encode_float(obj))  # type: ignore
            elif isinstance(obj, (list, tuple, array_types)):
                write_sequence(obj, write, indent_level, current_indent)
            elif isinstance(obj, (dict, object_types)):
                write_mapping(obj, write, indent_level, current_indent)
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
                if markers is not None:
                    markers.clear()

            write(end)
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

        self._encoder: _EncodeFunc[object] = make_encoder(
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
