# Copyright (C) 2024 Nice Zombies
"""JSON run_filter_query tests."""
from __future__ import annotations

__all__: list[str] = []

from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import JSONSyntaxError, run_filter_query
from jsonyx.test import check_syntax_err

if TYPE_CHECKING:
    _Node = tuple[dict[Any, Any] | list[Any], int | slice | str]


@pytest.mark.parametrize(("obj", "keep"), [
    # Missing key
    ([], False),

    # Key present
    ([0], True),
])
def test_has_key(obj: list[Any], keep: bool) -> None:  # noqa: FBT001
    """Test has key."""
    expected: list[_Node] = [(obj, 0)] if keep else []
    assert run_filter_query((obj, 0), "@") == expected


@pytest.mark.parametrize(("obj", "keep"), [
    # Missing key
    ([], True),

    # Key present
    ([0], False),
])
def test_has_not_key(obj: list[Any], keep: bool) -> None:  # noqa: FBT001
    """Test has not key."""
    expected: list[_Node] = [(obj, 0)] if keep else []
    assert run_filter_query((obj, 0), "!@") == expected


@pytest.mark.parametrize(("query", "keep"), [
    # Less than or equal to
    ("@ <= -1", False),
    ("@ <= 0", True),
    ("@ <= 1", True),

    # Less than
    ("@ < -1", False),
    ("@ < 0", False),
    ("@ < 1", True),

    # Equal to
    ("@ == 1", False),
    ("@ == 0", True),

    # Not equal to
    ("@ != 0", False),
    ("@ != 1", True),

    # Greater than or equal to
    ("@ >= 1", False),
    ("@ >= 0", True),
    ("@ >= -1", True),

    # Greater than
    ("@ > 1", False),
    ("@ > 0", False),
    ("@ > -1", True),
])
def test_operator(query: str, keep: bool) -> None:  # noqa: FBT001
    """Test operator."""
    expected: list[_Node] = [([0], 0)] if keep else []
    assert run_filter_query(([0], 0), query) == expected


@pytest.mark.parametrize("query", [
    # No whitespace
    "@==0",

    # Before operator
    "@ ==0",

    # After operator
    "@== 0",
])
def test_operator_whitespace(query: str) -> None:
    """Test whitespace around operator."""
    assert not run_filter_query([], query)


@pytest.mark.parametrize(("obj", "keep"), [
    # Missing first key
    ({"b": 0}, False),

    # Missing second key
    ({"a": 0}, False),

    # Both keys present
    ({"a": 0, "b": 1}, False),  # Different value
    ({"a": 0, "b": 0}, True),  # Same value
])
def test_value_comparison(
    obj: dict[Any, Any], keep: bool,  # noqa: FBT001
) -> None:
    """Test comparison of two values."""
    expected: list[_Node] = [([obj], 0)] if keep else []
    assert run_filter_query(([obj], 0), "@.a == @.b") == expected


def test_and() -> None:
    """Test and."""
    query: str = "@ != 1 && @ != 2 && @ != 3"
    assert run_filter_query(([0], 0), query) == [([0], 0)]


@pytest.mark.parametrize("query", [
    # Before and
    "@!=1 &&@!=2 &&@!=3",

    # After and
    "@!=1&& @!=2&& @!=3",
])
def test_whitespace(query: str) -> None:
    """Test whitespace around and."""
    assert run_filter_query(([0], 0), query) == [([0], 0)]


@pytest.mark.parametrize(("query", "msg", "colno", "end_colno"), [
    ("", "Expecting a relative query", 1, -1),
    ("$", "Expecting a relative query", 1, -1),
    ("!", "Expecting a relative query", 2, -1),
    ("@?", "Optional marker is not allowed", 2, 3),
    ("@ == ", "Expecting value", 6, -1),
    ("@ == $", "Expecting value", 6, -1),
    ("@ == @?", "Optional marker is not allowed", 7, 8),
    ("@ && ", "Expecting a relative query", 6, -1),
    ("!@ == @", "Unexpected operator", 4, 6),
    ("@ @ @", "Expecting end of file", 2, -1),
])
def test_invalid_query(
    query: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_filter_query([], query)

    check_syntax_err(exc_info, msg, colno, end_colno)

    ("@[:]", "Filter is not allowed", 3, -1),
    ("@ == @[:]", "Filter is not allowed", 8, -1),


def test_slice() -> None:
    """Test slice."""
