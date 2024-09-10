# Copyright (C) 2024 Nice Zombies
"""JSON make_patch tests."""
# TODO(Nice Zombies): add more tests
from __future__ import annotations

__all__: list[str] = []

from decimal import Decimal
from math import nan

import pytest

from jsonyx import make_patch


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
