"""JSON select_nodes tests."""
from __future__ import annotations

__all__: list[str] = []

from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import JSONSyntaxError, select_nodes
from jsonyx.allow import MISSING_COMMAS, TRAILING_COMMA
from jsonyx.test import check_syntax_err

if TYPE_CHECKING:
    _Target = dict[str, Any] | list[Any]
    _Node = tuple[_Target, Any]


# pylint: disable-next=R0903
class _Slicer:
    @staticmethod
    def __getitem__(item: slice) -> slice:
        return item


_slicer: _Slicer = _Slicer()


@pytest.mark.parametrize(("node", "keep"), [
    # List
    (([], 0), False),
    (([0], 0), True),

    # Dict
    (({}, ""), False),
    (({"": 0}, ""), True),
])  # type: ignore
@pytest.mark.parametrize("query", ["$?", "${@}"])
def test_optional_marker(node: _Node, query: str, keep: bool) -> None:
    """Test optional marker."""
    expected: list[_Node] = [node] if keep else []
    assert select_nodes(node, query) == expected


@pytest.mark.parametrize("key", [
    # Ascending
    _slicer[:],

    # Descending
    _slicer[::-1],
])
@pytest.mark.parametrize("query", ["$?", "${@}"])
def test_optional_marker_slice(key: slice, query: str) -> None:
    """Test optional marker with slice."""
    obj: list[Any] = [1, 2, 3]
    expected: list[_Node] = [(obj, i) for i in range(3)]
    assert select_nodes((obj, key), query) == expected


@pytest.mark.parametrize("key", [
    # First character
    "A", "_", "\u16ee", "\u1885", "\u2118",

    # Remaining characters
    "A0", "AA", "A_", "A\u0300", "A\u2118",
])
def test_property(key: str) -> None:
    """Test property."""
    assert select_nodes(([{}], 0), f"$.{key}") == [({}, key)]


@pytest.mark.parametrize("key", [
    # First character
    "\x00", "!", "$", "0", "\xb2", "\u0300", "\u037a", "\u0488",

    # Remaining characters
    "A\x00", "A!", "A$", "A\xb2", "A\u037a", "A\u0488",
])
def test_invalid_property(key: str) -> None:
    """Test invalid property."""
    with pytest.raises(JSONSyntaxError):
        select_nodes([], f"$.{key}")


@pytest.mark.parametrize("query", [
    # At the end
    "$.a",

    # In the middle
    "$.a?", "$.a.b", "$.a[:]", "$.a[0]", "$.a['']", "$.a[@]", "$.a{@}",
])
def test_list_property(query: str) -> None:
    """Test property on a list."""
    match: str = "List index must be int or slice, not"
    with pytest.raises(TypeError, match=match):
        select_nodes(([[]], 0), query, allow_slice=True)


@pytest.mark.parametrize("query", [
    # At the end
    "@.a",

    # In the middle
    "@.a.b", "@.a[0]", "@.a['']",
])
def test_relative_list_property(query: str) -> None:
    """Test relative property on a list."""
    with pytest.raises(TypeError, match="List index must be int, not"):
        select_nodes(([[]], 0), query, relative=True)


@pytest.mark.parametrize(("query", "expected"), [
    # Slice
    ("$[:]", _slicer[:]),
    ("$[-1:]", _slicer[-1:]),
    ("$[0:]", _slicer[0:]),
    ("$[1:]", _slicer[1:]),
    ("$[10:]", _slicer[10:]),
    ("$[11:]", _slicer[11:]),
    ("$[:-1]", _slicer[:-1]),
    ("$[:0]", _slicer[:0]),
    ("$[:1]", _slicer[:1]),
    ("$[:10]", _slicer[:10]),
    ("$[:11]", _slicer[:11]),

    # Extended slice
    ("$[::]", _slicer[::]),
    ("$[-1::]", _slicer[-1::]),
    ("$[0::]", _slicer[0::]),
    ("$[1::]", _slicer[1::]),
    ("$[10::]", _slicer[10::]),
    ("$[11::]", _slicer[11::]),
    ("$[:-1:]", _slicer[:-1:]),
    ("$[:0:]", _slicer[:0:]),
    ("$[:1:]", _slicer[:1:]),
    ("$[:10:]", _slicer[:10:]),
    ("$[:11:]", _slicer[:11:]),
    ("$[::-1]", _slicer[::-1]),
    ("$[::0]", _slicer[::0]),
    ("$[::1]", _slicer[::1]),
    ("$[::10]", _slicer[::10]),
    ("$[::11]", _slicer[::11]),
])
def test_slice(query: str, expected: slice) -> None:
    """Test slice."""
    assert select_nodes(([[]], 0), query, allow_slice=True) == [([], expected)]


@pytest.mark.parametrize("query", [
    # Slice
    "$[1\uff10:]", "$[:1\uff10]",

    # Extended slice
    "$[1\uff10::]", "$[:1\uff10:]", "$[::1\uff10]",
])
def test_invalid_slice(query: str) -> None:
    """Test slice."""
    with pytest.raises(JSONSyntaxError):
        select_nodes([], query)


@pytest.mark.parametrize(("obj", "msg"), [
    ([], "List index must be int, not"),
    ({}, "Dict key must be str, not"),
])
@pytest.mark.parametrize("query", [
    # At the end
    "@[:]",

    # In the middle
    "@[:].b", "@[:][:]", "@[:][0]", "@[:]['']",
])
def test_slice_not_allowed(obj: _Target, msg: str, query: str) -> None:
    """Test slice when not allowed."""
    with pytest.raises(TypeError, match=msg):
        select_nodes(([obj], 0), query, relative=True)


@pytest.mark.parametrize("num", [
    # Sign
    "-1",

    # Integer
    "0", "1", "10", "11",
])
def test_idx(num: str) -> None:
    """Test index."""
    assert select_nodes(([[]], 0), f"$[{num}]") == [([], int(num))]


def test_invalid_idx() -> None:
    """Test invalid idx."""
    with pytest.raises(JSONSyntaxError):
        select_nodes(([[]], 0), "$[1\uff10]")


@pytest.mark.parametrize(("query", "keys"), [
    # Whitespace
    ("$[1,2,3]", [1, 2, 3]),  # no whitespace
    ("$[1 ,2 ,3]", [1, 2, 3]),  # before commas
    ("$[1, 2, 3]", [1, 2, 3]),  # after commas

    # Sorting
    ("$[3,2,1]", [1, 2, 3]),  # positive indices
    ("$[-3, -2, -1]", [-1, -2, -3]),  # negative indices
])
def test_index_array(query: str, keys: list[Any]) -> None:
    """Test index array."""
    assert select_nodes(([[]], 0), query) == [([], key) for key in keys]


@pytest.mark.parametrize(("query", "msg", "end_colno"), [
    ("$[1-2-3]", "Expecting comma", -1),
    ("$[1 2 3]", "Missing commas are not allowed", -1),
    ("$[0,]", "Trailing comma is not allowed", 5),
])
def test_invalid_index_array(query: str, msg: str, end_colno: int) -> None:
    """Test invalid index array."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        select_nodes(([[]], 0), query)

    check_syntax_err(exc_info, msg, 4, end_colno)


@pytest.mark.parametrize("query", [
    # At the end
    "$[0]",

    # In the middle
    "$[0]?", "$[0].b", "$[0][:]", "$[0][0]", "$[0]['']", "$[0][@]", "$[0]{@}",
])
def test_dict_idx(query: str) -> None:
    """Test index on a dict."""
    with pytest.raises(TypeError, match="Dict key must be str, not"):
        select_nodes(([{}], 0), query)


@pytest.mark.parametrize(("query", "keys"), [
    # One value
    ("$['']", [""]),

    # Multiple values
    ("$['a','b','c']", ["a", "b", "c"]),  # no whitespace
    ("$['a' ,'b' ,'c']", ["a", "b", "c"]),  # whitespace before commas
    ("$['a', 'b', 'c']", ["a", "b", "c"]),  # whitespace after commas
])
def test_property_array(query: str, keys: list[Any]) -> None:
    """Test property array."""
    assert select_nodes(([{}], 0), query) == [({}, key) for key in keys]


@pytest.mark.parametrize(("query", "msg", "colno", "end_colno"), [
    ("$['a' 'b' 'c']", "Missing commas are not allowed", 6, -1),
    ("$['',]", "Trailing comma is not allowed", 5, 6),
])
def test_invalid_property_array(
    query: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid property array."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        select_nodes(([{}], 0), query)

    check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize(("obj", "query", "keys"), [
    ([], "$[1 2 3]", [1, 2, 3]),
    ({}, "$['a' 'b' 'c']", ["a", "b", "c"]),
])
def test_missing_commas(obj: Any, query: str, keys: list[Any]) -> None:
    """Test missing commas."""
    expected: list[_Node] = [(obj, key) for key in keys]
    assert select_nodes(([obj], 0), query, allow=MISSING_COMMAS) == expected


@pytest.mark.parametrize(("obj", "query", "key"), [
    ([], "$[0,]", 0),
    ({}, "$['',]", ""),
])
def test_trailing_comma(obj: Any, query: str, key: Any) -> None:
    """Test missing comma."""
    expected: list[_Node] = [(obj, key)]
    assert select_nodes(([obj], 0), query, allow=TRAILING_COMMA) == expected


@pytest.mark.parametrize(("obj", "keys"), [
    ([1, 2, 3], [0, 1, 2]),
    ({"a": 1, "b": 2, "c": 3}, ["a", "b", "c"]),
])
def test_filter(obj: _Target, keys: list[Any]) -> None:
    """Test filter."""
    assert select_nodes(([obj], 0), "$[@]") == [(obj, key) for key in keys]


@pytest.mark.parametrize(("obj", "query"), [
    # No selectors
    (0, "$"),

    # One selector
    ([0], "$[0]"),

    # Multiple selectors
    ([[[0]]], "$[0][0][0]"),
])
def test_query(obj: _Target, query: str) -> None:
    """Test query."""
    assert select_nodes(([obj], 0), query) == [([0], 0)]


@pytest.mark.parametrize(("query", "msg", "colno", "end_colno"), [
    ("", "Expecting an absolute query", 1, -1),
    ("@", "Expecting an absolute query", 1, -1),
    ("$.", "Expecting property", 3, -1),
    ("$[0", "Unterminated subscript", 2, 4),
    ("${@", "Unterminated condition", 2, 4),
    ("$ $ $", "Expecting end of file", 2, -1),
])
def test_invalid_query(
    query: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        select_nodes([], query)

    check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize(("query", "msg", "colno", "end_colno"), [
    ("", "Expecting a relative query", 1, -1),
    ("$", "Expecting a relative query", 1, -1),
    ("@?", "Optional markers are not allowed in relative query", 2, 3),
    ("@{@}", "Conditions are not allowed in relative query", 2, -1),
    ("@[@]", "Filters are not allowed in relative query", 3, -1),
    ("@[1, 2, 3]", "Arrays are not allowed in relative query", 3, 10),
    ("@['a', 'b', 'c']", "Arrays are not allowed in relative query", 3, 16),
])
def test_invalid_relative_query(
    query: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid relative query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        select_nodes([], query, relative=True)

    check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize("query", [
    # At the end
    "$[0]",

    # In the middle
    "$[0]?", "$[0].b", "$[0][:]", "$[0][0]", "$[0]['']", "$[0][@]", "$[0]{@}",
])
def test_invalid_target(query: str) -> None:
    """Test invalid target."""
    with pytest.raises(TypeError, match="Target must be dict or list, not"):
        select_nodes(([0], 0), query)
