"""Customizable JSON library for Python."""
from __future__ import annotations

__all__: list[str] = [
    "Decoder",
    "Encoder",
    "JSONSyntaxError",
    "Manipulator",
    "TruncatedSyntaxError",
    "apply_filter",
    "apply_patch",
    "detect_encoding",
    "dump",
    "dumps",
    "format_syntax_error",
    "load",
    "load_query_value",
    "loads",
    "make_patch",
    "read",
    "select_nodes",
    "write",
]
__version__: str = "2.2.0"

from typing import TYPE_CHECKING, Any, Protocol, TypeVar

from jsonyx._decoder import (
    Decoder, JSONSyntaxError, TruncatedSyntaxError, detect_encoding,
)
from jsonyx._differ import make_patch
from jsonyx._encoder import Encoder
from jsonyx._manipulator import Manipulator
from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container
    from os import PathLike

    _T_co = TypeVar("_T_co", covariant=True)
    _T_contra = TypeVar("_T_contra", contravariant=True)

    # pylint: disable-next=R0903
    class _SupportsRead(Protocol[_T_co]):
        def read(self, length: int = ..., /) -> _T_co:  # type: ignore
            """Read string."""

    # pylint: disable-next=R0903
    class _SupportsWrite(Protocol[_T_contra]):
        def write(self, s: _T_contra, /) -> object:
            """Write string."""

    _Node = tuple[dict[Any, Any] | list[Any], Any]
    _Operation = dict[str, Any]
    _StrPath = PathLike[str] | str
    _Hook = Callable[[Any], Any]


def format_syntax_error(exc: TruncatedSyntaxError) -> list[str]:
    """Format a truncated syntax error.

    :param exc: a truncated syntax error
    :return: a list of strings, each ending in a newline

    Example:
        >>> import jsonyx as json
        >>> try:
        ...     json.loads("[,]")
        ... except json.JSONSyntaxError as exc:
        ...     print("Traceback (most recent call last):")
        ...     print(end="".join(json.format_syntax_error(exc)))
        ...
        Traceback (most recent call last):
          File "<string>", line 1, column 2
            [,]
             ^
        jsonyx.JSONSyntaxError: Expecting value

    .. note:: Don't use :func:`traceback.format_exception_only`, it displays
        less information.

    """
    if exc.end_lineno == exc.lineno:
        line_range: str = f"{exc.lineno:d}"
    else:
        line_range = f"{exc.lineno:d}-{exc.end_lineno:d}"

    if exc.end_colno == exc.colno:
        column_range: str = f"{exc.colno:d}"
    else:
        column_range = f"{exc.colno:d}-{exc.end_colno:d}"

    indent: str = " " * (exc.offset - 1)  # type: ignore
    if exc.end_lineno == exc.lineno:
        selection: str = "^" * (exc.end_offset - exc.offset)  # type: ignore
    else:
        selection = "^" * (len(exc.text) - exc.offset + 1)  # type: ignore

    return [
        f'  File "{exc.filename}", line {line_range}, column {column_range}\n',
        f"    {exc.text}\n",
        f"    {indent}{selection}\n",
        f"{exc.__module__}.{type(exc).__qualname__}: {exc.msg}\n",
    ]


def read(
    filename: _StrPath,
    *,
    allow: Container[str] = NOTHING,
    cache_keys: bool = False,
    hooks: dict[str, _Hook] | None = None,
) -> Any:
    """Deserialize a JSON file to a Python object.

    .. versionchanged:: 2.0 Replaced ``use_decimal`` with ``hooks``.

    .. versionchanged:: 2.2

        - Added ``cache_keys``.
        - Disabled caching keys by default.

    :param filename: the path to the JSON file
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param cache_keys: re-use the keys of objects
    :param hooks: the :ref:`hooks <decoding_hooks>` used for transforming data
    :raises OSError: if the file can't be opened
    :raises TruncatedSyntaxError: when failing to decode the file
    :return: a Python object.

    Example:
        >>> import jsonyx as json
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> with TemporaryDirectory() as tmpdir:
        ...     filename = Path(tmpdir) / "file.json"
        ...     _ = filename.write_text('["filesystem API"]', "utf-8")
        ...     json.Decoder().read(filename)
        ...
        ['filesystem API']

    """
    return Decoder(
        allow=allow, cache_keys=cache_keys, hooks=hooks,
    ).read(filename)


def load(
    fp: _SupportsRead[bytes | str],
    *,
    allow: Container[str] = NOTHING,
    cache_keys: bool = False,
    hooks: dict[str, _Hook] | None = None,
    root: _StrPath = ".",
) -> Any:
    """Deserialize an open JSON file to a Python object.

    .. versionchanged:: 2.0 Replaced ``use_decimal`` with ``hooks``.

    .. versionchanged:: 2.2

        - Added ``cache_keys``.
        - Disabled caching keys by default.

    :param fp: an open JSON file
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param cache_keys: re-use the keys of objects
    :param hooks: the :ref:`hooks <decoding_hooks>` used for transforming data
    :param root: the path to the archive containing this JSON file
    :raises TruncatedSyntaxError: when failing to decode the file
    :return: a Python object

    Example:
        >>> import jsonyx as json
        >>> from io import StringIO
        >>> io = StringIO('["streaming API"]')
        >>> json.load(io)
        ['streaming API']

    .. tip:: Specify ``root`` to display the zip filename in error messages.

    """
    return Decoder(
        allow=allow, cache_keys=cache_keys, hooks=hooks,
    ).load(fp, root=root)


def loads(
    s: bytes | str,
    *,
    allow: Container[str] = NOTHING,
    cache_keys: bool = False,
    filename: _StrPath = "<string>",
    hooks: dict[str, _Hook] | None = None,
) -> Any:
    r"""Deserialize a JSON string to a Python object.

    .. versionchanged:: 2.0 Replaced ``use_decimal`` with ``hooks``.

    .. versionchanged:: 2.2

        - Added ``cache_keys``.
        - Disabled caching keys by default.

    :param s: a JSON string
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param cache_keys: re-use the keys of objects
    :param filename: the path to the JSON file
    :param hooks: the :ref:`hooks <decoding_hooks>` used for transforming data
    :raises TruncatedSyntaxError: when failing to decode the string
    :return: a Python object

    Example:
        >>> import jsonyx as json
        >>> json.loads('{"foo": ["bar", null, 1.0, 2]}')
        {'foo': ['bar', None, 1.0, 2]}
        >>> json.loads(r'"\"foo\bar"')
        '"foo\x08ar'

    .. tip:: Specify ``filename`` to display the filename in error messages.

    """
    return Decoder(
        allow=allow, cache_keys=cache_keys, hooks=hooks,
    ).loads(s, filename=filename)


def write(
    obj: object,
    filename: _StrPath,
    encoding: str = "utf-8",
    *,
    allow: Container[str] = NOTHING,
    check_circular: bool = True,
    commas: bool = True,
    end: str = "\n",
    ensure_ascii: bool = False,
    hook: _Hook | None = None,
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
    r"""Serialize a Python object to a JSON file.

    .. versionchanged:: 2.0

        - Added ``commas``, ``encoding``, ``indent_leaves``,
          ``max_indent_level``, ``quoted_keys`` and ``types``.
        - Made :class:`tuple` serializable by default instead of
          :class:`enum.Enum` and :class:`decimal.Decimal`.
        - Replaced ``item_separator`` and ``key_separator`` with
          ``separators``.

    .. versionchanged:: 2.1 Added ``check_circular``, ``hook`` and
        ``skipkeys``.

    :param obj: a Python object
    :param filename: the path to the JSON file
    :param encoding: the JSON encoding
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param check_circular: check for circular references
    :param commas: separate items by commas when indented
    :param end: the string to append at the end
    :param ensure_ascii: escape non-ASCII characters
    :param hook: the :ref:`hook <encoding_hook>` used for transforming data
    :param indent: the number of spaces or string to indent with
    :param indent_leaves: indent leaf objects and arrays
    :param max_indent_level: the level up to which to indent
    :param quoted_keys: quote keys which are :ref:`identifiers <identifiers>`
    :param separators: the item and key separator
    :param skipkeys: skip non-string keys
    :param sort_keys: sort the keys of objects
    :param trailing_comma: add a trailing comma when indented
    :param types: a dictionary of :ref:`additional types <protocol_types>`
    :raises OSError: if the file can't be opened
    :raises RecursionError: if the object is too deeply nested
    :raises TypeError: for unserializable values
    :raises TruncatedSyntaxError: when failing to encode the file
    :raises ValueError: for invalid values

    Example:
        >>> import jsonyx as json
        >>> from pathlib import Path
        >>> from tempfile import TemporaryDirectory
        >>> with TemporaryDirectory() as tmpdir:
        ...     filename = Path(tmpdir) / "file.json"
        ...     json.write(["filesystem API"], filename)
        ...     filename.read_text("utf-8")
        ...
        '["filesystem API"]\n'

    .. note:: The item separator is automatically stripped when indented.
    .. warning:: Avoid specifying ABCs for ``types``, that is very slow.

    """
    Encoder(
        allow=allow,
        check_circular=check_circular,
        commas=commas,
        end=end,
        ensure_ascii=ensure_ascii,
        hook=hook,
        indent=indent,
        indent_leaves=indent_leaves,
        max_indent_level=max_indent_level,
        quoted_keys=quoted_keys,
        separators=separators,
        skipkeys=skipkeys,
        sort_keys=sort_keys,
        trailing_comma=trailing_comma,
        types=types,
    ).write(obj, filename, encoding)


def dump(
    obj: object,
    fp: _SupportsWrite[str] | None = None,
    *,
    allow: Container[str] = NOTHING,
    check_circular: bool = True,
    commas: bool = True,
    end: str = "\n",
    ensure_ascii: bool = False,
    hook: _Hook | None = None,
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
    r"""Serialize a Python object to an open JSON file.

    .. versionchanged:: 2.0

        - Added ``commas``, ``indent_leaves``, ``max_indent_level``,
          ``quoted_keys`` and ``types``.
        - Made :class:`tuple` serializable by default instead of
          :class:`enum.Enum` and :class:`decimal.Decimal`.
        - Replaced ``item_separator`` and ``key_separator`` with
          ``separators``.

    .. versionchanged:: 2.1 Added ``check_circular``, ``hook`` and
        ``skipkeys``.

    :param obj: a Python object
    :param fp: an open JSON file
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param check_circular: check for circular references
    :param commas: separate items by commas when indented
    :param end: the string to append at the end
    :param ensure_ascii: escape non-ASCII characters
    :param hook: the :ref:`hook <encoding_hook>` used for transforming data
    :param indent: the number of spaces or string to indent with
    :param indent_leaves: indent leaf objects and arrays
    :param max_indent_level: the level up to which to indent
    :param quoted_keys: quote keys which are :ref:`identifiers <identifiers>`
    :param separators: the item and key separator
    :param skipkeys: skip non-string keys
    :param sort_keys: sort the keys of objects
    :param trailing_comma: add a trailing comma when indented
    :param types: a dictionary of :ref:`additional types <protocol_types>`
    :raises RecursionError: if the object is too deeply nested
    :raises TypeError: for unserializable values
    :raises TruncatedSyntaxError: when failing to write to the file
    :raises ValueError: for invalid values

    Example:
        Writing to standard output:

        >>> import jsonyx as json
        >>> json.dump('"foo\bar')
        "\"foo\bar"
        >>> json.dump("\\")
        "\\"
        >>> json.dump("\u20AC")
        "€"

        Writing to an open file:

        >>> import jsonyx as json
        >>> from io import StringIO
        >>> io = StringIO()
        >>> json.dump(["streaming API"], io)
        >>> io.getvalue()
        '["streaming API"]\n'

    .. note:: The item separator is automatically stripped when indented.
    .. warning:: Avoid specifying ABCs for ``types``, that is very slow.

    """
    Encoder(
        allow=allow,
        check_circular=check_circular,
        commas=commas,
        end=end,
        ensure_ascii=ensure_ascii,
        hook=hook,
        indent=indent,
        indent_leaves=indent_leaves,
        max_indent_level=max_indent_level,
        quoted_keys=quoted_keys,
        separators=separators,
        skipkeys=skipkeys,
        sort_keys=sort_keys,
        trailing_comma=trailing_comma,
        types=types,
    ).dump(obj, fp)


def dumps(
    obj: object,
    *,
    allow: Container[str] = NOTHING,
    check_circular: bool = True,
    commas: bool = True,
    end: str = "\n",
    ensure_ascii: bool = False,
    hook: _Hook | None = None,
    indent: int | str | None = None,
    indent_leaves: bool = True,
    max_indent_level: int | None = None,
    quoted_keys: bool = True,
    separators: tuple[str, str] = (", ", ": "),
    skipkeys: bool = False,
    sort_keys: bool = False,
    trailing_comma: bool = False,
    types: dict[str, type | tuple[type, ...]] | None = None,
) -> str:
    r"""Serialize a Python object to a JSON string.

    .. versionchanged:: 2.0

        - Added ``commas``, ``indent_leaves``, ``max_indent_level``,
          ``quoted_keys`` and ``types``.
        - Made :class:`tuple` serializable by default instead of
          :class:`enum.Enum` and :class:`decimal.Decimal`.
        - Replaced ``item_separator`` and ``key_separator`` with
          ``separators``.

    .. versionchanged:: 2.1 Added ``check_circular``, ``hook`` and
        ``skipkeys``.

    :param obj: a Python object
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param check_circular: check for circular references
    :param commas: separate items by commas when indented
    :param end: the string to append at the end
    :param ensure_ascii: escape non-ASCII characters
    :param hook: the :ref:`hook <encoding_hook>` used for transforming data
    :param indent: the number of spaces or string to indent with
    :param indent_leaves: indent leaf objects and arrays
    :param max_indent_level: the level up to which to indent
    :param quoted_keys: quote keys which are :ref:`identifiers <identifiers>`
    :param separators: the item and key separator
    :param skipkeys: skip non-string keys
    :param sort_keys: sort the keys of objects
    :param trailing_comma: add a trailing comma when indented
    :param types: a dictionary of :ref:`additional types <protocol_types>`
    :raises RecursionError: if the object is too deeply nested
    :raises TypeError: for unserializable values
    :raises ValueError: for invalid values
    :return: a JSON string

    Example:
        >>> import jsonyx as json
        >>> json.dumps(["foo", {"bar": ("baz", None, 1.0, 2)}])
        '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'

    .. note:: The item separator is automatically stripped when indented.
    .. warning:: Avoid specifying ABCs for ``types``, that is very slow.

    """
    return Encoder(
        allow=allow,
        check_circular=check_circular,
        commas=commas,
        end=end,
        ensure_ascii=ensure_ascii,
        hook=hook,
        indent=indent,
        indent_leaves=indent_leaves,
        max_indent_level=max_indent_level,
        quoted_keys=quoted_keys,
        separators=separators,
        skipkeys=skipkeys,
        sort_keys=sort_keys,
        trailing_comma=trailing_comma,
        types=types,
    ).dumps(obj)


def apply_patch(
    obj: Any,
    patch: _Operation | list[_Operation],
    *,
    allow: Container[str] = NOTHING,
    use_decimal: bool = False,
) -> Any:
    """Apply a JSON patch to a Python object.

    .. versionadded:: 2.0

    :param obj: a Python object
    :param patch: a :doc:`JSON patch </json-patch-spec>`
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`
    :raises AssertionError: if an assertion fails
    :raises IndexError: if an index is out of range
    :raises JSONSyntaxError: if a query is invalid
    :raises KeyError: if a key is not found
    :raises TypeError: if a value has the wrong type
    :raises ValueError: if a value is invalid
    :return: the patched Python object

    Example:
        >>> import jsonyx as json
        >>> json.apply_patch([1, 2, 3], {"op": "del", "path": "$[1]"})
        [1, 3]

    .. tip:: Using a :ref:`filter` instead of an index is more robust.

    """
    return Manipulator(allow=allow, use_decimal=use_decimal).apply_patch(
        obj, patch,
    )


def paste_values(
    current_nodes: _Node | list[_Node],
    values: Any | list[Any],
    operation: _Operation,
    *,
    allow: Container[str] = NOTHING,
    use_decimal: bool = False,
) -> None:
    """Paste value to a node or values to a list of nodes.

    .. versionadded:: 2.0

    :param current_nodes: a node or a list of nodes
    :param values: a value or a list of values
    :param operation: a JSON :ref:`copy` or :ref:`move` operation
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`
    :raises IndexError: if an index is out of range
    :raises JSONSyntaxError: if a query is invalid
    :raises KeyError: if a key is not found
    :raises TypeError: if a value has the wrong type
    :raises ValueError: if a value is invalid

    Example:
        >>> import jsonyx as json
        >>> obj = [1, 2, 3]
        >>> root = [obj]
        >>> node = root, 0  # pointer to obj
        >>> json.paste_values(node, 4, {"mode": "append"})
        >>> root[0]
        [1, 2, 3, 4]

    """
    Manipulator(allow=allow, use_decimal=use_decimal).paste_values(
        current_nodes, values, operation,
    )


def select_nodes(
    nodes: _Node | list[_Node],
    query: str,
    *,
    allow: Container[str] = NOTHING,
    allow_slice: bool = False,
    relative: bool = False,
    use_decimal: bool = False,
) -> list[_Node]:
    """Select nodes from a node or a list of nodes.

    .. versionadded:: 2.0

    :param nodes: a node or a list of nodes
    :param query: an :ref:`JSON select query <query>`
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param allow_slice: allow slice
    :param relative: query must start with ``"@"`` instead of ``"$"``
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`
    :raises IndexError: if an index is out of range
    :raises JSONSyntaxError: if the select query is invalid
    :raises KeyError: if a key is not found
    :raises TypeError: if a value has the wrong type
    :return: the selected list of nodes

    Example:
        >>> import jsonyx as json
        >>> obj = [1, 2, 3, 4, 5, 6]
        >>> root = [obj]
        >>> node = root, 0  # pointer to obj
        >>> for target, key in json.select_nodes(node, "$[@ > 3]"):
        ...     target[key] = None
        ...
        >>> root[0]
        [1, 2, 3, None, None, None]

    """
    return Manipulator(allow=allow, use_decimal=use_decimal).select_nodes(
        nodes, query, allow_slice=allow_slice, relative=relative,
    )


def apply_filter(
    nodes: _Node | list[_Node],
    query: str,
    *,
    allow: Container[str] = NOTHING,
    use_decimal: bool = False,
) -> list[_Node]:
    """Apply a JSON filter query to a node or a list of nodes.

    .. versionadded:: 2.0

    :param nodes: a node or a list of nodes
    :param query: a :ref:`JSON filter query <filter>`
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`
    :raises IndexError: if an index is out of range
    :raises JSONSyntaxError: if the filter query is invalid
    :raises KeyError: if a key is not found
    :raises TypeError: if a value has the wrong type
    :return: the filtered list of nodes

    Example:
        >>> import jsonyx as json
        >>> obj = None
        >>> root = [obj]
        >>> node = root, 0  # pointer to obj
        >>> assert json.apply_filter(node, "@ == null")

    """
    return Manipulator(allow=allow, use_decimal=use_decimal).apply_filter(
        nodes, query,
    )


def load_query_value(
    s: str,
    *,
    allow: Container[str] = NOTHING,
    use_decimal: bool = False,
) -> Any:
    """Deserialize a JSON query value to a Python object.

    .. versionadded:: 2.0

    :param s: a :ref:`JSON query value <query_value>`
    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`
    :raises JSONSyntaxError: if the query value is invalid
    :return: a Python object

    Example:
        >>> import jsonyx as json
        >>> json.load_query_value("'~'foo'")
        "'foo"

    """
    return Manipulator(allow=allow, use_decimal=use_decimal).load_query_value(
        s,
    )
