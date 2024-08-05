# Copyright (C) 2022-2024 Nice Zombies
"""JSON patcher."""
from __future__ import annotations

from typing import Any

__all__: list[str] = ["patch"]


def _traverse(target: Any, path: str) -> tuple[Any, str]:
    keys: list[str] = path[1:].split("/")
    for key in keys[:-1]:
        target = target[key]

    return target, keys[-1]


def _replace_value(obj: Any, operation: dict[str, Any]) -> Any:
    target, key = _traverse(obj, operation["path"])
    if not key:
        obj = operation["value"]
    else:
        target[key] = operation["value"]

    return obj


def patch(obj: Any, operations: list[dict[str, Any]]) -> Any:
    """Patch a Python object with a list of operations.

    :param obj: a Python object
    :type obj: Any
    :param operations: a list of operations
    :type operations: list[dict[str, Any]]
    :return: the patched Python object
    :rtype: Any
    """
    for operation in operations:
        if operation["op"] == "replace":
            obj = _replace_value(obj, operation)

    return obj
