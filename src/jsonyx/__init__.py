# Copyright (C) 2024 Nice Zombies
# TODO(Nice Zombies): link to v2.0.0 in changelog
"""Configurable JSON manipulator for Python."""
from __future__ import annotations

__all__: list[str] = [
    "Decoder",
    "DuplicateKey",
    "Encoder",
    "JSONSyntaxError",
    "Manipulator",
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
    "run_filter_query",
    "run_select_query",
    "write",
]
__version__: str = "2.0.0"

from codecs import (
    BOM_UTF8, BOM_UTF16_BE, BOM_UTF16_LE, BOM_UTF32_BE, BOM_UTF32_LE,
)
from decimal import Decimal
from os import fspath
from os.path import realpath
from pathlib import Path
from sys import stdout
from typing import TYPE_CHECKING, Any, Literal

from jsonyx._decoder import DuplicateKey, JSONSyntaxError, make_scanner
from jsonyx._differ import make_patch
from jsonyx._encoder import make_encoder
from jsonyx._manipulator import Manipulator
from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container

    from _typeshed import StrPath, SupportsRead, SupportsWrite

    _AllowList = Container[Literal[
        "comments", "duplicate_keys", "missing_commas", "nan_and_infinity",
        "surrogates", "trailing_comma",
    ] | str]
    _Node = tuple[dict[Any, Any] | list[Any], int | slice | str]


class Decoder:
    """A configurable JSON decoder.

    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param use_decimal: use decimal instead of float, defaults to False
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
                     defaults to "."
        :type root: StrPath, optional
        :raises JSONSyntaxError: if the JSON file is invalid
        :return: a Python object
        :rtype: Any

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
        :param filename: the path to the JSON file, defaults to "<string>"
        :type filename: StrPath, optional
        :raises JSONSyntaxError: if the JSON string is invalid
        :return: a Python object
        :rtype: Any

        >>> json.Decoder().loads('{"foo": ["bar", null, 1.0, 2]}')
        {'foo': ['bar', None, 1.0, 2]}
        """
        filename = fspath(filename)
        if not filename.startswith("<") and not filename.endswith(">"):
            filename = realpath(filename)

        if not isinstance(s, str):
            s = s.decode(detect_encoding(s), self._errors)
        elif s.startswith("\ufeff"):
            msg: str = "Unexpected UTF-8 BOM"
            raise JSONSyntaxError(msg, filename, s, 0)

        return self._scanner(filename, s)


class Encoder:
    r"""A configurable JSON encoder.

    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param end: the string to append at the end, defaults to "\\n"
    :type end: str, optional
    :param ensure_ascii: escape non-ASCII characters, defaults to False
    :type ensure_ascii: bool, optional
    :param indent: indentation, defaults to None
    :type indent: int | str | None, optional
    :param item_separator: the separator between two items, defaults to ", "
    :type item_separator: str, optional
    :param key_separator: the separator between a key and a value, defaults to
                          ": "
    :type key_separator: str, optional
    :param sort_keys: sort the keys of objects, defaults to False
    :type sort_keys: bool, optional
    :param trailing_comma: add a trailing comma if indented, defaults to False
    :type trailing_comma: bool, optional
    :param unquoted_keys: don't quote keys which are identifiers, defaults to
                          False
    :type unquoted_keys: bool, optional

    .. versionchanged:: 2.0
        Added *unquoted_keys*.
    """

    def __init__(
        self,
        *,
        allow: _AllowList = NOTHING,
        end: str = "\n",
        ensure_ascii: bool = False,
        indent: int | str | None = None,
        item_separator: str = ", ",
        key_separator: str = ": ",
        sort_keys: bool = False,
        trailing_comma: bool = False,
        unquoted_keys: bool = False,
    ) -> None:
        """Create a new JSON encoder."""
        allow_nan_and_infinity: bool = "nan_and_infinity" in allow
        allow_surrogates: bool = "surrogates" in allow
        decimal_str: Callable[[Decimal], str] = Decimal.__str__

        if indent is not None:
            item_separator = item_separator.rstrip()
            if isinstance(indent, int):
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
            encode_decimal, indent, end, item_separator, key_separator,
            allow_nan_and_infinity, allow_surrogates, ensure_ascii, sort_keys,
            trailing_comma, unquoted_keys,
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
        :param fp: an open JSON file, defaults to stdout
        :type fp: SupportsWrite[str], optional
        :raises TypeError: for unserializable values
        :raises ValueError: for invalid values

        >>> import jsonyx as json
        >>> encoder = json.Encoder()
        >>> encoder.dump(["foo", {"bar": ('baz', None, 1.0, 2)}])
        ["foo", {"bar": ["baz", null, 1.0, 2]}]
        >>> from io import StringIO
        >>> io = StringIO()
        >>> encoder.dump(["streaming API"], io)
        >>> io.getvalue()
        '["streaming API"]\n'
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
        >>> json.Encoder().dumps(["foo", {"bar": ('baz', None, 1.0, 2)}])
        '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'
        """
        return self._encoder(obj)


def detect_encoding(b: bytearray | bytes) -> str:
    r"""Detect JSON encoding.

    :param b: a JSON string
    :type b: bytearray | bytes
    :return: the detected encoding
    :rtype: str

    >>> import jsonyx as json
    >>> b = b'\x00"\x00f\x00o\x00o\x00"'
    >>> b.decode(json.detect_encoding(b))
    '"foo"'
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


def format_syntax_error(exc: JSONSyntaxError) -> list[str]:
    """Format JSON syntax error.

    :param exc: a JSON syntax error
    :type exc: JSONSyntaxError
    :return: a list of strings, each ending in a newline
    :rtype: list[str]

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
    """
    if exc.end_lineno == exc.lineno:
        line_range: str = f"{exc.lineno:d}"
    else:
        line_range = f"{exc.lineno:d}-{exc.end_lineno:d}"

    if exc.end_colno == exc.colno:
        column_range: str = f"{exc.colno:d}"
    else:
        column_range = f"{exc.colno:d}-{exc.end_colno:d}"

    caret_indent: str = " " * (exc.offset - 1)  # type: ignore
    caret_selection: str = "^" * (exc.end_offset - exc.offset)  # type: ignore
    return [
        f'  File "{exc.filename}", line {line_range}, column {column_range}\n',
        f"    {exc.text}\n",
        f"    {caret_indent}{caret_selection}\n",
        f"{exc.__module__}.{type(exc).__qualname__}: {exc.msg}\n",
    ]


def read(
    filename: StrPath,
    *,
    allow: _AllowList = NOTHING,
    use_decimal: bool = False,
) -> Any:
    """Deserialize a JSON file to a Python object.

    :param filename: the path to the JSON file
    :type filename: StrPath
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param use_decimal: use decimal instead of float, defaults to False
    :type use_decimal: bool, optional
    :raises JSONSyntaxError: if the JSON file is invalid
    :return: a Python object.
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

    .. seealso::
        :func:`jsonyx.Decoder.read`
    """
    return Decoder(allow=allow, use_decimal=use_decimal).read(filename)


def load(
    fp: SupportsRead[bytes | str],
    *,
    allow: _AllowList = NOTHING,
    root: StrPath = ".",
    use_decimal: bool = False,
) -> Any:
    """Deserialize an open JSON file to a Python object.

    :param fp: an open JSON file
    :type fp: SupportsRead[bytes | str]
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param root: the path to the archive containing this JSON file, defaults to
                 "."
    :type root: StrPath, optional
    :param use_decimal: use decimal instead of float, defaults to False
    :type use_decimal: bool, optional
    :raises JSONSyntaxError: if the JSON file is invalid
    :return: a Python object
    :rtype: Any

    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)
    ['streaming API']

    .. seealso::
        :func:`jsonyx.Decoder.read`
    """
    return Decoder(allow=allow, use_decimal=use_decimal).load(fp, root=root)


def loads(
    s: bytearray | bytes | str,
    *,
    allow: _AllowList = NOTHING,
    filename: StrPath = "<string>",
    use_decimal: bool = False,
) -> Any:
    """Deserialize a JSON string to a Python object.

    :param s: a JSON string
    :type s: bytearray | bytes | str
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param filename: the path to the JSON file, defaults to "<string>"
    :type filename: StrPath, optional
    :param use_decimal: use decimal instead of float, defaults to False
    :type use_decimal: bool, optional
    :raises JSONSyntaxError: if the JSON string is invalid
    :return: a Python object
    :rtype: Any

    >>> json.loads('{"foo": ["bar", null, 1.0, 2]}')
    {'foo': ['bar', None, 1.0, 2]}

    .. seealso::
        :func:`jsonyx.Decoder.read`
    """
    return Decoder(allow=allow, use_decimal=use_decimal).loads(
        s, filename=filename,
    )


def write(
    obj: object,
    filename: StrPath,
    *,
    allow: _AllowList = NOTHING,
    end: str = "\n",
    ensure_ascii: bool = False,
    indent: int | str | None = None,
    item_separator: str = ", ",
    key_separator: str = ": ",
    sort_keys: bool = False,
    trailing_comma: bool = False,
    unquoted_keys: bool = False,
) -> None:
    r"""Serialize a Python object to a JSON file.

    :param obj: a Python object
    :type obj: object
    :param filename: the path to the JSON file
    :type filename: StrPath
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param end: the string to append at the end, defaults to "\\n"
    :type end: str, optional
    :param ensure_ascii: escape non-ASCII characters, defaults to False
    :type ensure_ascii: bool, optional
    :param indent: indentation, defaults to None
    :type indent: int | str | None, optional
    :param item_separator: the separator between two items, defaults to ", "
    :type item_separator: str, optional
    :param key_separator: the separator between a key and a value, defaults to
                          ": "
    :type key_separator: str, optional
    :param sort_keys: sort the keys of objects, defaults to False
    :type sort_keys: bool, optional
    :param trailing_comma: add a trailing comma if indented, defaults to False
    :type trailing_comma: bool, optional
    :param unquoted_keys: don't quote keys which are identifiers, defaults to
                          False
    :type unquoted_keys: bool, optional
    :raises TypeError: for unserializable values
    :raises ValueError: for invalid values

    >>> import jsonyx as json
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as tmpdir:
    ...     filename = Path(tmpdir) / "file.json"
    ...     json.write(["filesystem API"], filename)
    ...     filename.read_text("utf_8")
    ...
    '["filesystem API"]\n'

    .. seealso::
        :func:`jsonyx.Encoder.write`

    .. versionchanged:: 2.0
        Added *unquoted_keys*.
    """
    return Encoder(
        allow=allow,
        end=end,
        ensure_ascii=ensure_ascii,
        indent=indent,
        item_separator=item_separator,
        key_separator=key_separator,
        sort_keys=sort_keys,
        trailing_comma=trailing_comma,
        unquoted_keys=unquoted_keys,
    ).write(obj, filename)


def dump(
    obj: object,
    fp: SupportsWrite[str] = stdout,
    *,
    allow: _AllowList = NOTHING,
    end: str = "\n",
    ensure_ascii: bool = False,
    indent: int | str | None = None,
    item_separator: str = ", ",
    key_separator: str = ": ",
    sort_keys: bool = False,
    trailing_comma: bool = False,
    unquoted_keys: bool = False,
) -> None:
    r"""Serialize a Python object to an open JSON file.

    :param obj: a Python object
    :type obj: object
    :param fp: an open JSON file, defaults to stdout
    :type fp: SupportsWrite[str], optional
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param end: the string to append at the end, defaults to "\\n"
    :type end: str, optional
    :param ensure_ascii: escape non-ASCII characters, defaults to False
    :type ensure_ascii: bool, optional
    :param indent: indentation, defaults to None
    :type indent: int | str | None, optional
    :param item_separator: the separator between two items, defaults to ", "
    :type item_separator: str, optional
    :param key_separator: the separator between a key and a value, defaults to
                          ": "
    :type key_separator: str, optional
    :param sort_keys: sort the keys of objects, defaults to False
    :type sort_keys: bool, optional
    :param trailing_comma: add a trailing comma if indented, defaults to False
    :type trailing_comma: bool, optional
    :param unquoted_keys: don't quote keys which are identifiers, defaults to
                          False
    :type unquoted_keys: bool, optional
    :raises TypeError: for unserializable values
    :raises ValueError: for invalid values

    >>> import jsonyx as json
    >>> json.dump(["foo", {"bar": ('baz', None, 1.0, 2)}])
    ["foo", {"bar": ["baz", null, 1.0, 2]}]
    >>> from io import StringIO
    >>> io = StringIO()
    >>> json.dump(["streaming API"], io)
    >>> io.getvalue()
    '["streaming API"]\n'

    .. seealso::
        :func:`jsonyx.Encoder.dump`

    .. versionchanged:: 2.0
        Added *unquoted_keys*.
    """
    Encoder(
        allow=allow,
        end=end,
        ensure_ascii=ensure_ascii,
        indent=indent,
        item_separator=item_separator,
        key_separator=key_separator,
        sort_keys=sort_keys,
        trailing_comma=trailing_comma,
        unquoted_keys=unquoted_keys,
    ).dump(obj, fp)


def dumps(
    obj: object,
    *,
    allow: _AllowList = NOTHING,
    end: str = "\n",
    ensure_ascii: bool = False,
    indent: int | str | None = None,
    item_separator: str = ", ",
    key_separator: str = ": ",
    sort_keys: bool = False,
    trailing_comma: bool = False,
    unquoted_keys: bool = False,
) -> str:
    r"""Serialize a Python object to a JSON string.

    :param obj: a Python object
    :type obj: object
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param end: the string to append at the end, defaults to "\\n"
    :type end: str, optional
    :param ensure_ascii: escape non-ASCII characters, defaults to False
    :type ensure_ascii: bool, optional
    :param indent: indentation, defaults to None
    :type indent: int | str | None, optional
    :param item_separator: the separator between two items, defaults to ", "
    :type item_separator: str, optional
    :param key_separator: the separator between a key and a value, defaults to
                          ": "
    :type key_separator: str, optional
    :param sort_keys: sort the keys of objects, defaults to False
    :type sort_keys: bool, optional
    :param trailing_comma: add a trailing comma if indented, defaults to False
    :type trailing_comma: bool, optional
    :param unquoted_keys: don't quote keys which are identifiers, defaults to
                          False
    :type unquoted_keys: bool, optional
    :raises TypeError: for unserializable values
    :raises ValueError: for invalid values
    :return: a JSON string
    :rtype: str

    >>> import jsonyx as json
    >>> json.dumps(["foo", {"bar": ('baz', None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]\n'

    .. seealso::
        :func:`jsonyx.Encoder.dumps`

    .. versionchanged:: 2.0
        Added *unquoted_keys*.
    """
    return Encoder(
        allow=allow,
        end=end,
        ensure_ascii=ensure_ascii,
        indent=indent,
        item_separator=item_separator,
        key_separator=key_separator,
        sort_keys=sort_keys,
        trailing_comma=trailing_comma,
        unquoted_keys=unquoted_keys,
    ).dumps(obj)


def apply_patch(
    obj: Any,
    patch: dict[str, Any] | list[dict[str, Any]],
    *,
    allow: _AllowList = NOTHING,
    use_decimal: bool = False,
) -> Any:
    """Apply a JSON patch to a Python object.

    :param obj: a Python object
    :type obj: Any
    :param patch: a JSON patch
    :type patch: dict[str, Any] | list[dict[str, Any]]
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param use_decimal: use decimal instead of float, defaults to False
    :type use_decimal: bool, optional
    :raises AssertionError: if an assertion fails
    :raises SyntaxError: if a query is invalid
    :raises TypeError: if a value has the wrong type
    :raises ValueError: if a value is invalid
    :return: the patched Python object
    :rtype: Any

    >>> import jsonyx as json
    >>> json.apply_patch([1, 2, 3], {"op": "clear"})
    []

    .. seealso::
        :func:`jsonyx.Manipulator.apply_patch`

    .. versionadded:: 2.0
    """
    return Manipulator(allow=allow, use_decimal=use_decimal).apply_patch(
        obj, patch,
    )


def run_select_query(
    nodes: _Node | list[_Node],
    query: str,
    *,
    allow: _AllowList = NOTHING,
    allow_slice: bool = False,
    mapping: bool = False,
    relative: bool = False,
    use_decimal: bool = False,
) -> list[_Node]:
    """Run a JSON select query on a node or a list of nodes.

    :param nodes: a node or a list of nodes
    :type nodes: _Node | list[_Node]
    :param query: a JSON select query
    :type query: str
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param allow_slice: allow slice, defaults to False
    :type allow_slice: bool, optional
    :param use_decimal: use decimal instead of float, defaults to False
    :type use_decimal: bool, optional
    :raises SyntaxError: if the select query is invalid
    :raises ValueError: if a value is invalid
    :return: the selected list of nodes
    :rtype: list[_Node]

    >>> import jsonyx as json
    >>> root = [[1, 2, 3, 4, 5, 6]]
    >>> node = root, 0
    >>> for target, key in json.run_select_query(node, "$[@ > 3]"):
    ...     target[key] = None
    ...
    >>> root[0]
    [1, 2, 3, None, None, None]

    .. seealso::
        :func:`jsonyx.Manipulator.run_select_query`

    .. versionadded:: 2.0
    """
    return Manipulator(allow=allow, use_decimal=use_decimal).run_select_query(
        nodes,
        query,
        allow_slice=allow_slice,
        mapping=mapping,
        relative=relative,
    )


def run_filter_query(
    nodes: _Node | list[_Node],
    query: str,
    *,
    allow: _AllowList = NOTHING,
    use_decimal: bool = False,
) -> list[_Node]:
    """Run a JSON filter query on a node or a list of nodes.

    :param nodes: a node or a list of nodes
    :type nodes: _Node | list[_Node]
    :param query: a JSON filter query
    :type query: str
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param use_decimal: use decimal instead of float, defaults to False
    :type use_decimal: bool, optional
    :raises SyntaxError: if the filter query is invalid
    :return: the filtered list of nodes
    :rtype: list[_Node]

    >>> import jsonyx as json
    >>> node = [None], 0
    >>> assert json.run_filter_query(node, "@ == null")

    .. seealso::
        :func:`jsonyx.Manipulator.run_filter_query`

    .. versionadded:: 2.0
    """
    return Manipulator(allow=allow, use_decimal=use_decimal).run_filter_query(
        nodes, query,
    )


def load_query_value(
    s: str,
    *,
    allow: _AllowList = NOTHING,
    use_decimal: bool = False,
) -> Any:
    """Deserialize a JSON query value to a Python object.

    :param s: a JSON query value
    :type s: str
    :param allow: the allowed JSON deviations, defaults to NOTHING
    :type allow: Container[str], optional
    :param use_decimal: use decimal instead of float, defaults to False
    :type use_decimal: bool, optional
    :raises SyntaxError: if the query value is invalid
    :return: a Python object
    :rtype: Any

    >>> import jsonyx as json
    >>> json.load_query_value("'~'foo'")
    "'foo"

    .. seealso::
        :func:`jsonyx.Manipulator.load_query_value`

    .. versionadded:: 2.0
    """
    return Manipulator(allow=allow, use_decimal=use_decimal).load_query_value(
        s,
    )
