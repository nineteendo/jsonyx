"""JSON paste_values tests."""
from __future__ import annotations

__all__: list[str] = []

from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import paste_values

if TYPE_CHECKING:
    _Operation = dict[str, Any]


def _apply_paste(obj: Any, value: Any, operation: _Operation) -> Any:
    root: list[Any] = [obj]
    paste_values((root, 0), value, operation)
    return root[0]


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4]),
    ([[1, 2, 3]], {"to": "@[0]"}, [[1, 2, 3, 4]]),
])
def test_append(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test append."""
    assert _apply_paste(obj, 4, {"mode": "append", **kwargs}) == expected


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4, 5, 6]),
    ([[1, 2, 3]], {"to": "@[0]"}, [[1, 2, 3, 4, 5, 6]]),
])
def test_extend(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test extend."""
    value: list[Any] = [4, 5, 6]
    assert _apply_paste(obj, value, {"mode": "extend", **kwargs}) == expected


def test_insert() -> None:
    """Test insert."""
    operation: _Operation = {"mode": "insert", "to": "@[0]"}
    assert _apply_paste([1, 2, 3], 0, operation) == [0, 1, 2, 3]


def test_insert_current_object() -> None:
    """Test insert at current object."""
    with pytest.raises(ValueError, match="Can not insert at current object"):
        _apply_paste(0, 0, {"mode": "insert", "to": "@"})


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
    assert _apply_paste(obj, value, {"mode": "set", **kwargs}) == expected


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ({"a": 1, "b": 2, "c": 3}, {}, {"a": 4, "b": 5, "c": 6}),
    ([{"a": 1, "b": 2, "c": 3}], {"to": "@[0]"}, [{"a": 4, "b": 5, "c": 6}]),
])
def test_update(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test update."""
    value: dict[str, Any] = {"a": 4, "b": 5, "c": 6}
    assert _apply_paste(obj, value, {"mode": "update", **kwargs}) == expected


@pytest.mark.parametrize("mode", [
    "assert", "clear", "copy", "del", "move", "reverse", "sort",
])
def test_unknown_mode(mode: str) -> None:
    """Test unknown mode."""
    with pytest.raises(ValueError, match="Unknown mode"):
        _apply_paste(0, 0, {"mode": mode})
