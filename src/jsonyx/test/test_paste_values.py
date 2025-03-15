"""JSON make_patch tests."""
# TODO(Nice Zombies): test extend, insert, set and update
from __future__ import annotations

__all__: list[str] = []

from typing import Any

from jsonyx import paste_values


def test_append() -> None:
    """Test append."""
    obj: list[Any] = [1, 2, 3]
    paste_values(([obj], 0), 4, {"mode": "append"})
    assert obj == [1, 2, 3, 4]
