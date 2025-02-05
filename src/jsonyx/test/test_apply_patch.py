"""JSON apply_patch tests."""
# Test rest of operations
from __future__ import annotations

__all__: list[str] = []

from typing import Any

import pytest

from jsonyx import apply_patch


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([], {}, [0]),
    ([[]], {"path": "$[0]"}, [[0]]),
])  # type: ignore
def test_append(obj: Any, kwargs: dict[str, Any], expected: Any) -> None:
    """Test append operation."""
    assert apply_patch(obj, {"op": "append", "value": 0, **kwargs}) == expected


@pytest.mark.parametrize(("obj", "kwargs"), [
    (0, {}),
    ([0], {"path": "$[0]"}),
])
def test_assert(obj: Any, kwargs: dict[str, Any]) -> None:
    """Test assert operation."""
    apply_patch(obj, {"op": "assert", "expr": "@ == 0", **kwargs})


@pytest.mark.parametrize(("obj", "kwargs", "match"), [
    (1, {}, "@ == 0"),
    ([1], {"path": "$[0]"}, "@ == 0"),
    (1, {"msg": "msg"}, "msg"),
])
def test_failed_assert(obj: Any, kwargs: dict[str, Any], match: str) -> None:
    """Test failed assert operation."""
    with pytest.raises(AssertionError, match=match):
        apply_patch(obj, {"op": "assert", "expr": "@ == 0", **kwargs})


@pytest.mark.parametrize(("obj", "kwargs", "expected"), [
    ([1, 2, 3], {}, []),
    ({"a": 1, "b": 2, "c": 3}, {}, {}),

    ([[1, 2, 3]], {"path": "$[0]"}, [[]]),
    ([{"a": 1, "b": 2, "c": 3}], {"path": "$[0]"}, [{}]),
])  # type: ignore
def test_clear(obj: Any, kwargs: dict[str, Any], expected: Any) -> None:
    """Test clear operation."""
    assert apply_patch(obj, {"op": "clear", **kwargs}) == expected


def test_invalid_clear() -> None:
    """Test invalid clear operation."""
    with pytest.raises(TypeError, match="Target must be dict or list, not"):
        apply_patch(0, {"op": "clear"})
