# Copyright (C) 2024 Nice Zombies
"""JSON run_filter_query tests."""
# TODO(Nice Zombies): add more tests
from __future__ import annotations

__all__: list[str] = []

import pytest

from jsonyx import JSONSyntaxError, run_filter_query
from jsonyx.test import check_syntax_err


def test_exist() -> None:
    """Test exist."""
    assert run_filter_query(([], 0), "@") == []


def test_not_exist() -> None:
    """Test not exist."""
    assert run_filter_query(([], 0), "!@") == [([], 0)]


@pytest.mark.parametrize(
    "query", ["@ <= -1", "@ < -1", "@ == 1", "@ != 0", "@ >= 1", "@ > 1"],
)
def test_operator(query: str) -> None:
    """Test operator."""
    assert run_filter_query(([0], 0), query) == []


@pytest.mark.parametrize("query", [
    # Before operator
    "@ ==0",

    # After operator
    "@== 0",
])
def test_operator_whitespace(query: str) -> None:
    """Test whitespace around operator."""
    assert run_filter_query([], query) == []


@pytest.mark.parametrize(("query", "msg", "colno", "end_colno"), [
    ("", "Expecting a relative query", 1, -1),
    ("$", "Expecting a relative query", 1, -1),
    ("!", "Expecting a relative query", 2, -1),
    ("@?", "Optional marker is not allowed", 2, 3),
    ("@[@]", "Filter is not allowed", 3, -1),
    ("@ == ", "Expecting value", 6, -1),
    ("@ == $", "Expecting value", 6, -1),
    ("@ == @?", "Optional marker is not allowed", 7, 8),
    ("@ == @[@]", "Filter is not allowed", 8, -1),
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
