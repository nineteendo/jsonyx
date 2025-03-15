"""JSON make_patch tests."""
# TODO(Nice Zombies): test zipping
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
    root: list[Any] = [obj]
    paste_values((root, 0), 4, {"mode": "append", **kwargs})
    assert root[0] == expected


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4, 5, 6]),
    ([[1, 2, 3]], {"to": "@[0]"}, [[1, 2, 3, 4, 5, 6]]),
])
def test_extend(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test extend."""
    root: list[Any] = [obj]
    paste_values((root, 0), [4, 5, 6], {"mode": "extend", **kwargs})
    assert root[0] == expected


def test_insert() -> None:
    """Test insert."""
    obj: list[Any] = [1, 2, 3]
    root: list[Any] = [obj]
    paste_values((root, 0), 0, {"mode": "insert", "to": "@[0]"})
    assert root[0] == [0, 1, 2, 3]


def test_insert_current_object() -> None:
    """Test insert at current object."""
    with pytest.raises(ValueError, match="Can not insert at current object"):
        paste_values(([0], 0), 0, {"mode": "insert", "to": "@"})


@pytest.mark.parametrize(("obj", "value", "kwargs", "expected"), [
    # Normal
    (0, 1, {}, 1),
    ([0], 1, {"to": "@[0]"}, [1]),
    ({"a": 0}, 1, {"to": "@.a"}, {"a": 1}),

    # Allow slice
    ([1, 2, 3], [4, 5, 6], {"to": "@[:]"}, [4, 5, 6]),
])
def test_set(obj: Any, value: Any, kwargs: _Operation, expected: Any) -> None:
    """Test set."""
    root: list[Any] = [obj]
    paste_values((root, 0), value, {"mode": "set", **kwargs})
    assert root[0] == expected


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ({"a": 1, "b": 2, "c": 3}, {}, {"a": 4, "b": 5, "c": 6}),
    ([{"a": 1, "b": 2, "c": 3}], {"to": "@[0]"}, [{"a": 4, "b": 5, "c": 6}]),
])
def test_update(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test update."""
    root: list[Any] = [obj]
    value: dict[str, Any] = {"a": 4, "b": 5, "c": 6}
    paste_values((root, 0), value, {"mode": "update", **kwargs})
    assert root[0] == expected
