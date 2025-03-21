"""JSON apply_patch tests."""
from __future__ import annotations

__all__: list[str] = []

from re import escape
from typing import TYPE_CHECKING, Any

import pytest

from jsonyx import apply_patch

if TYPE_CHECKING:
    _Operation = dict[str, Any]


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4]),
    ([[1, 2, 3]], {"path": "$[0]"}, [[1, 2, 3, 4]]),
])
def test_append(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test append."""
    assert apply_patch(obj, {"op": "append", "value": 4, **kwargs}) == expected


def test_append_copy() -> None:
    """Test if append makes a copy."""
    value: list[Any] = [0]
    result: list[Any] = apply_patch([], {"op": "append", "value": value})[0]
    assert result == value  # sanity check
    assert result is not value


@pytest.mark.parametrize(("obj", "kwargs"), [
    (0, {}),
    ([0], {"path": "$[0]"}),
])
def test_assert(obj: Any, kwargs: _Operation) -> None:
    """Test assert."""
    apply_patch(obj, {"op": "assert", "expr": "@ == 0", **kwargs})


@pytest.mark.parametrize(("obj", "kwargs", "match"), [
    (1, {}, "Path $: @ == 0"),
    ([1], {"path": "$[0]"}, "Path $[0]: @ == 0"),
    (1, {"msg": "msg"}, "msg"),
])
def test_failed_assert(obj: Any, kwargs: _Operation, match: str) -> None:
    """Test failed assert."""
    with pytest.raises(AssertionError, match=escape(match)):
        apply_patch(obj, {"op": "assert", "expr": "@ == 0", **kwargs})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    # Without path
    ([1, 2, 3], {}, []),
    ({"a": 1, "b": 2, "c": 3}, {}, {}),

    # With path
    ([[1, 2, 3]], {"path": "$[0]"}, [[]]),
    ([{"a": 1, "b": 2, "c": 3}], {"path": "$[0]"}, [{}]),
])  # type: ignore
def test_clear(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test clear."""
    assert apply_patch(obj, {"op": "clear", **kwargs}) == expected


def test_invalid_clear() -> None:
    """Test invalid clear."""
    with pytest.raises(TypeError, match="Target must be dict or list, not"):
        apply_patch(0, {"op": "clear"})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    # Without path
    ([0], {"mode": "append", "from": "@[0]"}, [0, 0]),
    ({"a": 0}, {"mode": "set", "from": "@.a", "to": "@.b"}, {"a": 0, "b": 0}),

    # With path
    ([[0]], {"mode": "append", "path": "$[0]", "from": "@[0]"}, [[0, 0]]),
    (
        [{"a": 0}],
        {"mode": "set", "path": "$[0]", "from": "@.a", "to": "@.b"},
        [{"a": 0, "b": 0}],
    ),

    # Allow slice
    ([1, 2, 3], {"mode": "extend", "from": "@[::-1]"}, [1, 2, 3, 3, 2, 1]),
])
def test_copy(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test copy."""
    assert apply_patch(obj, {"op": "copy", **kwargs}) == expected


def test_copy_copy() -> None:
    """Test if copy makes a copy."""
    value: list[Any] = [0]
    patch: _Operation = {"op": "copy", "mode": "set", "from": "@[0]"}
    result: list[Any] = apply_patch([value], patch)
    assert result == value  # sanity check
    assert result is not value


@pytest.mark.parametrize(("obj", "path", "expected"), [
    # List and dict
    ([1, 2, 3, 4], "$[3]", [1, 2, 3]),
    ({"a": 1, "b": 2, "c": 3, "d": 4}, "$.d", {"a": 1, "b": 2, "c": 3}),

    # Allow slice
    ([1, 2, 3], "$[:]", []),

    # Reverse indices for queries
    ([1, 0, 2, 0, 3], "$[@ == 0]", [1, 2, 3]),
])
def test_del(obj: Any, path: str, expected: Any) -> None:
    """Test delete."""
    assert apply_patch(obj, {"op": "del", "path": path}) == expected


def test_del_root() -> None:
    """Test delete root."""
    with pytest.raises(ValueError, match="Can not delete root"):
        apply_patch(0, {"op": "del", "path": "$"})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [1, 2, 3, 4, 5, 6]),
    ([[1, 2, 3]], {"path": "$[0]"}, [[1, 2, 3, 4, 5, 6]]),
])
def test_extend(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test extend."""
    patch: _Operation = {"op": "extend", "values": [4, 5, 6], **kwargs}
    assert apply_patch(obj, patch) == expected


def test_extend_copy() -> None:
    """Test if extend makes a copy."""
    value: list[Any] = [0]
    result: list[Any] = apply_patch([], {"op": "extend", "values": [value]})[0]
    assert result == value  # sanity check
    assert result is not value


@pytest.mark.parametrize(("path", "expected"), [
    # Normal
    ("$[0]", [0, 1, 2, 3]),

    # Reverse indices for queries
    ("$[@]", [0, 1, 0, 2, 0, 3]),
])
def test_insert(path: str, expected: Any) -> None:
    """Test insert."""
    patch: _Operation = {"op": "insert", "path": path, "value": 0}
    assert apply_patch([1, 2, 3], patch) == expected


def test_insert_copy() -> None:
    """Test if insert makes a copy."""
    value: list[Any] = [0]
    patch: _Operation = {"op": "insert", "path": "$[0]", "value": value}
    result: list[Any] = apply_patch([], patch)[0]
    assert result == value  # sanity check
    assert result is not value


def test_insert_root() -> None:
    """Test insert at root."""
    with pytest.raises(ValueError, match="Can not insert at root"):
        apply_patch(0, {"op": "insert", "path": "$", "value": 0})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    # Without path
    ([1, 2], {"mode": "append", "from": "@[0]"}, [2, 1]),
    ({"a": 0}, {"mode": "set", "from": "@.a", "to": "@.b"}, {"b": 0}),

    # With path
    ([[1, 2]], {"mode": "append", "path": "$[0]", "from": "@[0]"}, [[2, 1]]),
    (
        [{"a": 0}],
        {"mode": "set", "path": "$[0]", "from": "@.a", "to": "@.b"},
        [{"b": 0}],
    ),

    # Allow slice
    ([1, 2, 3], {"mode": "extend", "from": "@[::-1]"}, [3, 2, 1]),
])
def test_move(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test move."""
    assert apply_patch(obj, {"op": "move", **kwargs}) == expected


def test_move_current_object() -> None:
    """Test move current object."""
    with pytest.raises(ValueError, match="Can not move current object"):
        apply_patch(0, {"op": "move", "mode": "set", "from": "@"})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, [3, 2, 1]),
    ([[1, 2, 3]], {"path": "$[0]"}, [[3, 2, 1]]),
])
def test_reverse(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test reverse."""
    assert apply_patch(obj, {"op": "reverse", **kwargs}) == expected


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    # Normal
    (0, {"value": 1}, 1),
    ([0], {"path": "$[0]", "value": 1}, [1]),
    ({"a": 0}, {"path": "$.a", "value": 1}, {"a": 1}),

    # Allow slice
    ([1, 2, 3], {"path": "$[:]", "value": [4, 5, 6]}, [4, 5, 6]),
])
def test_set(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test set."""
    assert apply_patch(obj, {"op": "set", **kwargs}) == expected


def test_set_copy() -> None:
    """Test if set makes a copy."""
    value: list[Any] = [1]
    result: list[Any] = apply_patch([0], {"op": "set", "value": value})
    assert result == value  # sanity check
    assert result is not value


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([3, 1, 2], {}, [1, 2, 3]),
    ([[3, 1, 2]], {"path": "$[0]"}, [[1, 2, 3]]),
    ([3, 1, 2], {"reverse": True}, [3, 2, 1]),
])
def test_sort(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test sort."""
    assert apply_patch(obj, {"op": "sort", **kwargs}) == expected


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ({"a": 1, "b": 2, "c": 3}, {}, {"a": 4, "b": 5, "c": 6}),
    ([{"a": 1, "b": 2, "c": 3}], {"path": "$[0]"}, [{"a": 4, "b": 5, "c": 6}]),
])
def test_update(obj: Any, kwargs: _Operation, expected: Any) -> None:
    """Test update."""
    properties: dict[str, Any] = {"a": 4, "b": 5, "c": 6}
    patch: _Operation = {"op": "update", "properties": properties, **kwargs}
    assert apply_patch(obj, patch) == expected


def test_update_copy() -> None:
    """Test if update makes a copy."""
    value: list[Any] = [1]
    patch: _Operation = {"op": "update", "properties": {"a": [1]}}
    result: list[Any] = apply_patch({}, patch)["a"]
    assert result == value  # sanity check
    assert result is not value


@pytest.mark.parametrize(("paths", "expected"), [
    # Empty list
    ([], {"a": 1, "b": 2, "c": 3}),

    # Multiple operations
    (["$.a", "$.b", "$.c"], {}),
])
def test_operations(paths: list[str], expected: dict[str, Any]) -> None:
    """Test operations."""
    patch: list[_Operation] = [{"op": "del", "path": path} for path in paths]
    assert apply_patch({"a": 1, "b": 2, "c": 3}, patch) == expected


def test_unknown_operation() -> None:
    """Test unknown operation."""
    with pytest.raises(ValueError, match="Unknown operation"):
        apply_patch(0, {"op": "foo"})
