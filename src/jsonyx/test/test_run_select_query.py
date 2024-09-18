# Copyright (C) 2024 Nice Zombies
"""JSON run_select_query tests."""
# TODO(Nice Zombies): add more tests
from __future__ import annotations

__all__: list[str] = []

import sys
from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import JSONSyntaxError, run_select_query
from jsonyx.test import check_syntax_err

if TYPE_CHECKING:
    _Target = dict[Any, Any] | list[Any]
    _Key = int | slice | str
    _Node = tuple[_Target, _Key]


# pylint: disable-next=R0903
class _Slicer:
    @staticmethod
    def __getitem__(item: Any) -> Any:
        return item


_slicer: _Slicer = _Slicer()


@pytest.mark.parametrize(("node", "query", "expected"), [
    # List
    (([], slice(0)), "$?", ([], slice(0))),
    (([], 0), "$?", []),
    (([0], 0), "$?", ([0], 0)),

    # Dict
    (({}, ""), "$?", []),
    (({"": 0}, ""), "$?", ({"": 0}, "")),
])  # type: ignore
def test_optional_marker(
    node: _Node, query: str, expected: _Node | list[_Node],
) -> None:
    """Test optional marker."""
    if isinstance(expected, tuple):
        expected = [expected]

    assert run_select_query(node, query, allow_slice=True) == expected


def test_optional_marker_not_allowed() -> None:
    """Test optional marker when not allowed."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], "$?", mapping=True)

    check_syntax_err(exc_info, "Optional marker is not allowed", 2, 3)


@pytest.mark.parametrize("key", [
    # First character
    "A", "_", "\u16ee", "\u1885", "\u2118",

    # Remaining characters
    "A0", "AA", "A_", "A\u0300", "A\u2118",
])
def test_property(key: str) -> None:
    """Test query."""
    assert run_select_query(([{}], 0), f"$.{key}") == [({}, key)]


@pytest.mark.parametrize("key", [
    # First character
    "\x00", " ", "!", "$", "0", "\xb2", "\u0300", "\u037a", "\u0488",

    # Remaining characters
    "A\xb2", "A\u037a", "A\u0488",
])
def test_invalid_property(key: str) -> None:
    """Test invalid property."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], f"$.{key}")

    check_syntax_err(exc_info, "Expecting property", 3)


@pytest.mark.parametrize(("query", "expected"), [
    # Slice
    ("$[:]", _slicer[:]),
    ("$[:-1]", _slicer[:-1]),
    ("$[:0]", _slicer[:0]),
    ("$[:1]", _slicer[:1]),
    ("$[:10]", _slicer[:10]),
    ("$[:11]", _slicer[:11]),
    ("$[-1:]", _slicer[-1:]),
    ("$[0:]", _slicer[0:]),
    ("$[1:]", _slicer[1:]),
    ("$[10:]", _slicer[10:]),
    ("$[11:]", _slicer[11:]),

    # Extended slice
    ("$[::]", _slicer[::]),
    ("$[::-1]", _slicer[::-1]),
    ("$[::0]", _slicer[::0]),
    ("$[::1]", _slicer[::1]),
    ("$[::10]", _slicer[::10]),
    ("$[::11]", _slicer[::11]),
    ("$[:-1:]", _slicer[:-1:]),
    ("$[:0:]", _slicer[:0:]),
    ("$[:1:]", _slicer[:1:]),
    ("$[:10:]", _slicer[:10:]),
    ("$[:11:]", _slicer[:11:]),
    ("$[-1::]", _slicer[-1::]),
    ("$[0::]", _slicer[0::]),
    ("$[1::]", _slicer[1::]),
    ("$[10::]", _slicer[10::]),
    ("$[11::]", _slicer[11::]),
])
def test_slice(query: str, expected: slice) -> None:
    """Test slice."""
    node: _Node = [[]], 0
    assert run_select_query(node, query, allow_slice=True) == [([], expected)]


@pytest.mark.skipif(
    not hasattr(sys, "get_int_max_str_digits"),
    reason="requires integer string conversion length limit",
)
def test_too_big_start() -> None:
    """Test too big start."""
    num: str = "1" + "0" * sys.get_int_max_str_digits()
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query(([[]], 0), f"$[{num}::]")

    check_syntax_err(exc_info, "Start is too big", 3, 3 + len(num))


@pytest.mark.skipif(
    not hasattr(sys, "get_int_max_str_digits"),
    reason="requires integer string conversion length limit",
)
def test_too_big_stop() -> None:
    """Test too big stop."""
    num: str = "1" + "0" * sys.get_int_max_str_digits()
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query(([[]], 0), f"$[:{num}:]")

    check_syntax_err(exc_info, "Stop is too big", 4, 4 + len(num))


@pytest.mark.skipif(
    not hasattr(sys, "get_int_max_str_digits"),
    reason="requires integer string conversion length limit",
)
def test_too_big_step() -> None:
    """Test too big step."""
    num: str = "1" + "0" * sys.get_int_max_str_digits()
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query(([[]], 0), f"$[::{num}]")

    check_syntax_err(exc_info, "Step is too big", 5, 5 + len(num))


@pytest.mark.parametrize("num", [
    # Sign
    "-1",

    # Integer
    "0", "1", "10", "11",
])
def test_index(num: str) -> None:
    """Test index."""
    assert run_select_query(([[]], 0), f"$[{num}]") == [([], int(num))]


@pytest.mark.skipif(
    not hasattr(sys, "get_int_max_str_digits"),
    reason="requires integer string conversion length limit",
)
def test_too_big_int() -> None:
    """Test too big integer."""
    num: str = "1" + "0" * sys.get_int_max_str_digits()
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query(([[]], 0), f"$[{num}]")

    check_syntax_err(exc_info, "Index is too big", 3, 3 + len(num))


@pytest.mark.parametrize(("obj", "query", "keys"), [
    ([1, 2, 3], "$[@]", [0, 1, 2]),
    ({"a": 1, "b": 2, "c": 3}, "$[@]", ["a", "b", "c"]),
])
def test_filter(obj: _Target, query: str, keys: list[_Key]) -> None:
    """Test filter."""
    assert run_select_query(([obj], 0), query) == [(obj, key) for key in keys]


def test_filter_not_allowed() -> None:
    """Test filter when not allowed."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], "$[@]", mapping=True)

    check_syntax_err(exc_info, "Filter is not allowed", 3)


@pytest.mark.parametrize(("obj", "query", "expected"), [
    # Root
    (0, "$", ([0], 0)),

    # Key
    ({}, "$['']", ({}, "")),

    # Multiple levels
    ([[[0]]], "$[0][0][0]", ([0], 0)),
])  # type: ignore
def test_query(obj: _Target, query: str, expected: _Node) -> None:
    """Test root."""
    assert run_select_query(([obj], 0), query) == [expected]


@pytest.mark.parametrize(("query", "msg", "colno"), [
    ("", "Expecting an absolute query", 1),
    ("@", "Expecting an absolute query", 1),
    ("$[0", "Expecting a closing bracket", 4),
    ("$ $ $", "Expecting end of file", 2),
])
def test_invalid_query(query: str, msg: str, colno: int) -> None:
    """Test invalid query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], query)

    check_syntax_err(exc_info, msg, colno)


@pytest.mark.parametrize("query", ["", "$"])
def test_invalid_relative_query(query: str) -> None:
    """Test invalid relative query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], query, relative=True)

    check_syntax_err(exc_info, "Expecting a relative query")
