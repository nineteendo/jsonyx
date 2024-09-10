# Copyright (C) 2024 Nice Zombies
"""JSON run_select_query tests."""
# TODO(Nice Zombies): add more tests
from __future__ import annotations

__all__: list[str] = []

from typing import Any

import pytest

from jsonyx import JSONSyntaxError, run_select_query


def _check_syntax_err(
    exc_info: pytest.ExceptionInfo[Any], msg: str, colno: int = 1,
    end_colno: int = -1,
) -> None:
    exc: Any = exc_info.value
    if end_colno < 0:
        end_colno = colno

    assert exc.msg == msg
    assert exc.lineno == 1
    assert exc.end_lineno == 1
    assert exc.colno == colno
    assert exc.end_colno == end_colno


@pytest.mark.parametrize(("query", "msg", "colno", "end_colno"), [
    ("", "Expecting an absolute query", 1, -1),
    ("@", "Expecting an absolute query", 1, -1),
])
def test_invalid_query(
    query: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], query)

    _check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize("key", [
    # First character
    "\x00", " ", "!", "$", "0", "\xb2", "\u0300", "\u037a", "\u0488",

    # Remaining characters
    "A\xb2", "A\u037a", "A\u0488",
])
def test_invalid_unquoted_key(key: str) -> None:
    """Test invalid unquoted key."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], f"$.{key}")

    _check_syntax_err(exc_info, "Expecting key", 3)


@pytest.mark.parametrize(("query", "msg", "colno", "end_colno"), [
    ("$?", "Unexpected optional marker", 2, 3),
    ("$[@]", "Expecting key", 3, -1),
])
def test_invalid_mapping_query(
    query: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid mapping query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], query, mapping=True)

    _check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize("query", ["", "$"])
def test_invalid_relative_query(query: str) -> None:
    """Test invalid relative query."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        run_select_query([], query, relative=True)

    _check_syntax_err(exc_info, "Expecting a relative query")
