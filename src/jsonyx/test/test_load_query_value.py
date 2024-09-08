# Copyright (C) 2024 Nice Zombies
"""JSON load_query_value tests."""
# TODO(Nice Zombies): add more tests
from __future__ import annotations

__all__: list[str] = []

from decimal import Decimal
from typing import Any

import pytest

# pylint: disable-next=W0611
from jsonyx import JSONSyntaxError, load_query_value
from jsonyx.allow import NAN_AND_INFINITY


def _check_syntax_err(
    exc_info: pytest.ExceptionInfo[Any], msg: str, colno: int,
    end_colno: int = 0,
) -> None:
    exc: Any = exc_info.value
    if not end_colno:
        end_colno = colno

    assert exc.msg == msg
    assert exc.lineno == 1
    assert exc.end_lineno == 1
    assert exc.colno == colno
    assert exc.end_colno == end_colno


@pytest.mark.parametrize(("s", "expected"), [
    ("true", True),
    ("false", False),
    ("null", None),
])
def test_literal_names(s: str, expected: bool | None) -> None:  # noqa: FBT001
    """Test literal names."""
    assert load_query_value(s) is expected


@pytest.mark.parametrize("s", ["Infinity", "-Infinity"])
@pytest.mark.parametrize("use_decimal", [True, False])
def test_infinity(s: str, use_decimal: bool) -> None:  # noqa: FBT001
    """Test infinity."""
    obj: object = load_query_value(
        s, allow=NAN_AND_INFINITY, use_decimal=use_decimal,
    )
    expected_type: type[Decimal | float] = Decimal if use_decimal else float
    expected: Decimal | float = expected_type(s)
    assert isinstance(obj, expected_type)
    assert obj == expected


@pytest.mark.parametrize("s", ["Infinity", "-Infinity"])
@pytest.mark.parametrize("use_decimal", [True, False])
def test_infinity_not_allowed(
    s: str, use_decimal: bool,  # noqa: FBT001
) -> None:
    """Test infinity when not allowed."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(s, use_decimal=use_decimal)

    _check_syntax_err(exc_info, f"{s} is not allowed", 1, len(s) + 1)


@pytest.mark.parametrize("s", ["", "foo"])
def test_expecting_value(s: str) -> None:
    """Test expecting JSON value."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(s)

    _check_syntax_err(exc_info, "Expecting value", 1)
