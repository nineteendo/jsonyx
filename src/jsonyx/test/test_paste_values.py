"""JSON make_patch tests."""
# TODO(Nice Zombies): test set and update
from __future__ import annotations

__all__: list[str] = []

from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import paste_values

if TYPE_CHECKING:
    _Operation = dict[str, Any]


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4]),
    ([[1, 2, 3]], {"to": "@[0]"}, [[1, 2, 3, 4]]),
])
def test_append(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test append."""
    paste_values(([obj], 0), 4, {"mode": "append", **kwargs})
    assert obj == expected


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4, 5, 6]),
    ([[1, 2, 3]], {"to": "@[0]"}, [[1, 2, 3, 4, 5, 6]]),
])
def test_extend(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test extend."""
    paste_values(([obj], 0), [4, 5, 6], {"mode": "extend", **kwargs})
    assert obj == expected


def test_insert() -> None:
    """Test insert."""
    obj: list[Any] = [1, 2, 3]
    paste_values(([obj], 0), 0, {"mode": "insert", "to": "@[0]"})
    assert obj == [0, 1, 2, 3]


def test_insert_current_object() -> None:
    """Test insert at current object."""
    with pytest.raises(ValueError, match="Can not insert at current object"):
        paste_values(([0], 0), 0, {"mode": "insert", "to": "@"})
