# Copyright (C) 2024 Nice Zombies
"""JSON make_patch tests."""
from __future__ import annotations

__all__: list[str] = []

from decimal import Decimal
from math import nan
from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import make_patch

if TYPE_CHECKING:
    _Operation = dict[str, Any]


@pytest.mark.parametrize("obj", [
    # Dict
    {}, {"": 0},

    # List
    [], [0],

    # NaN
    nan, Decimal("nan"),

    # Basic
    "", 0, Decimal(0), 0.0, Decimal("0.0"), True, False, None,
])
def test_equal(obj: object) -> None:
    """Test equal."""
    assert not make_patch(obj, obj)


@pytest.mark.parametrize(("old", "new", "expected"), [
    # Different type
    ("", 0, [{"op": "set", "path": "$", "value": 0}]),

    # Dict
    ({"a": 1, "c": 3, "d": 4}, {"b": 2, "c": 5, "d": 4}, [
        {"op": "del", "path": "$.a"},
        {"op": "set", "path": "$.b", "value": 2},
        {"op": "set", "path": "$.c", "value": 5},
    ]),

    # List
    ([1, 2, 3], [2, 4, 5], [
        {"op": "del", "path": "$[0]"},
        {"op": "set", "path": "$[1]", "value": 4},
        {"op": "insert", "path": "$[2]", "value": 5},
    ]),

    # Replacing NaN
    (nan, 0.0, [{"op": "set", "path": "$", "value": 0.0}]),

    # Basic
    (1, 2, [{"op": "set", "path": "$", "value": 2}]),
])  # type: ignore
def test_not_equal(
    old: object, new: object, expected: list[_Operation],
) -> None:
    """Test not equal."""
    assert make_patch(old, new) == expected
