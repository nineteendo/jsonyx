"""JSON apply_patch tests."""
# Test rest of operations
from __future__ import annotations

__all__: list[str] = []

from typing import Any

import pytest

from jsonyx import apply_patch


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4]),
    ([[1, 2, 3]], {"path": "$[0]"}, [[1, 2, 3, 4]]),
])  # type: ignore
def test_append(obj: Any, kwargs: dict[str, Any], expected: Any) -> None:
    """Test append."""
    assert apply_patch(obj, {"op": "append", "value": 4, **kwargs}) == expected


def test_append_copy() -> None:
    """Test if append makes a copy."""
    value: list[Any] = [4]
    patch: dict[str, Any] = {"op": "append", "value": value}
    result: list[Any] = apply_patch([[1], [2], [3]], patch)[3]
    assert result == value  # sanity check
    assert result is not value


@pytest.mark.parametrize(("obj", "kwargs"), [
    (0, {}),
    ([0], {"path": "$[0]"}),
])
def test_assert(obj: Any, kwargs: dict[str, Any]) -> None:
    """Test assert."""
    apply_patch(obj, {"op": "assert", "expr": "@ == 0", **kwargs})


@pytest.mark.parametrize(("obj", "kwargs", "match"), [
    (1, {}, "@ == 0"),
    ([1], {"path": "$[0]"}, "@ == 0"),
    (1, {"msg": "msg"}, "msg"),
])
def test_failed_assert(obj: Any, kwargs: dict[str, Any], match: str) -> None:
    """Test failed assert."""
    with pytest.raises(AssertionError, match=match):
        apply_patch(obj, {"op": "assert", "expr": "@ == 0", **kwargs})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    # without path
    ([1, 2, 3], {}, []),
    ({"a": 1, "b": 2, "c": 3}, {}, {}),

    # with path
    ([[1, 2, 3]], {"path": "$[0]"}, [[]]),
    ([{"a": 1, "b": 2, "c": 3}], {"path": "$[0]"}, [{}]),
])  # type: ignore
def test_clear(obj: Any, kwargs: dict[str, Any], expected: Any) -> None:
    """Test clear."""
    assert apply_patch(obj, {"op": "clear", **kwargs}) == expected


def test_invalid_clear() -> None:
    """Test invalid clear."""
    with pytest.raises(TypeError, match="Target must be dict or list, not"):
        apply_patch(0, {"op": "clear"})


@pytest.mark.parametrize(("obj", "path", "expected"), [
    # Allow slice
    ([1, 2, 3], "$[:]", []),

    # Reverse indices for queries
    ([1, 0, 2, 0, 3], "$[@ == 0]", [1, 2, 3]),
])  # type: ignore
def test_del(obj: Any, path: str, expected: Any) -> None:
    """Test del."""
    assert apply_patch(obj, {"op": "del", "path": path}) == expected


def test_del_root() -> None:
    """Test delete root."""
    with pytest.raises(ValueError, match="Can not delete the root"):
        apply_patch(0, {"op": "del", "path": "$"})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4, 5, 6]),
    ([[1, 2, 3]], {"path": "$[0]"}, [[1, 2, 3, 4, 5, 6]]),
])  # type: ignore
def test_extend(obj: Any, kwargs: dict[str, Any], expected: Any) -> None:
    """Test extend."""
    patch: dict[str, Any] = {"op": "extend", "value": [4, 5, 6], **kwargs}
    assert apply_patch(obj, patch) == expected


def test_extend_copy() -> None:
    """Test if extend makes a copy."""
    value: list[Any] = [4]
    patch: dict[str, Any] = {"op": "extend", "value": [value]}
    result: list[Any] = apply_patch([[1], [2], [3]], patch)[3]
    assert result == value  # sanity check
    assert result is not value


@pytest.mark.parametrize(("path", "expected"), [
    # Normal
    ("$[0]", [0, 1, 2, 3]),

    # Reverse indices for queries
    ("$[@]", [0, 1, 0, 2, 0, 3]),
])  # type: ignore
def test_insert(path: str, expected: Any) -> None:
    """Test insert."""
    patch: dict[str, Any] = {"op": "insert", "path": path, "value": 0}
    assert apply_patch([1, 2, 3], patch) == expected


def test_insert_copy() -> None:
    """Test if insert makes a copy."""
    value: list[Any] = [0]
    patch: dict[str, Any] = {"op": "insert", "path": "$[0]", "value": value}
    result: list[Any] = apply_patch([[1], [2], [3]], patch)[0]
    assert result == value  # sanity check
    assert result is not value


def test_insert_root() -> None:
    """Test insert at the root."""
    with pytest.raises(ValueError, match="Can not insert at the root"):
        apply_patch(0, {"op": "insert", "path": "$", "value": 0})
