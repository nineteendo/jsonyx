"""Test free threading."""
from __future__ import annotations

__all__: list[str] = []

from collections import UserDict
from threading import Barrier, Thread
from typing import TYPE_CHECKING, Any

import pytest

import jsonyx.allow

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import ModuleType


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
            types: dict[str, type] = {"object": UserDict}
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


@pytest.mark.parametrize("object_type", [UserDict, dict])
def test_mutating_mapping(
    cjson: ModuleType, object_type: type[UserDict[int, int] | dict[int, int]],
) -> None:
    """Test mutating mapping."""
    def worker(
        barrier: Barrier,
        data: list[UserDict[int, int] | dict[int, int]],
        index: int,
    ) -> None:
        barrier.wait()
        while data:
            for d in data:
                if len(d) > 5:
                    d.clear()
                else:
                    d[index] = index
    data: list[UserDict[int, int] | dict[int, int]] = [
        object_type(), object_type(),
    ]
    _encode_json_helper(cjson, worker, data)
