"""Test free threading."""
from __future__ import annotations

__all__: list[str] = []

from threading import Barrier, Thread
from typing import TYPE_CHECKING, Any

import jsonyx.allow

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType


# pylint: disable-next=R0903
class _MyMapping:
    def __init__(self) -> None:
        self._items: list[tuple[object, object]] = []
        self._keys: list[object] = []
        self._values: list[object] = []

    def items(self) -> list[tuple[object, object]]:
        """Return items."""
        return self._items

    def keys(self) -> list[object]:
        """Return keys."""
        return self._keys

    def values(self) -> list[object]:
        """Return values."""
        return self._values


def _encode_json_helper(
    json: ModuleType,
    worker: Callable[..., object],
    data: list[Any],
    number_of_threads: int = 12,
    number_of_json_encodings: int = 100,
) -> None:
    barrier: Barrier = Barrier(number_of_threads)
    worker_threads: list[Thread] = [Thread(
        target=worker, args=[barrier, data, index],
    ) for index in range(number_of_threads)]
    try:
        for t in worker_threads:
            t.start()

        for _ in range(number_of_json_encodings):
            types: dict[str, type] = {"object": _MyMapping}
            json.dumps(data, allow=jsonyx.allow.NON_STR_KEYS, types=types)

    finally:
        data.clear()
        for t in worker_threads:
            t.join()


def test_mutating_list(cjson: ModuleType) -> None:
    """Test mutating list."""
    def worker(barrier: Barrier, data: list[list[int]], index: int) -> None:
        barrier.wait()
        while data:
            for d in data:
                if len(d) > 5:
                    d.clear()
                else:
                    d.append(index)
    data: list[list[int]] = [[], []]
    _encode_json_helper(cjson, worker, data)


def test_mutating_dict(cjson: ModuleType) -> None:
    """Test mutating dict."""
    def worker(
        barrier: Barrier, data: list[dict[int, int]], index: int,
    ) -> None:
        barrier.wait()
        while data:
            for d in data:
                if len(d) > 5:
                    d.clear()
                else:
                    d[index] = index
    data: list[dict[int, int]] = [{}, {}]
    _encode_json_helper(cjson, worker, data)


def test_mutating_mapping(cjson: ModuleType) -> None:
    """Test mutating mapping."""
    def worker(
        barrier: Barrier, data: list[_MyMapping], index: int,
    ) -> None:
        barrier.wait()
        while data:
            for d in data:
                if len(d.items()) > 5:
                    d.items().clear()
                else:
                    d.items().append((index, index))
    data: list[_MyMapping] = [_MyMapping(), _MyMapping()]
    _encode_json_helper(cjson, worker, data)
