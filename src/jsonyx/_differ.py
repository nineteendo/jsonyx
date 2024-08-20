# Copyright (C) 2024 Nice Zombies
"""JSON differ."""
from __future__ import annotations

__all__: list[str] = ["make_patch"]

import re
from itertools import starmap
from math import isnan
from re import Match
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, KeysView

_escape: Callable[[Callable[[Match[str]], str], str], str] = re.compile(
    r"[!&.<=>?[\]~]",
).sub


def _replace(match: Match[str]) -> str:
    return "~" + match.group()


def _eq(a: Any, b: Any) -> bool:
    if type(a) is not type(b):
        result = False
    elif isinstance(a, dict):
        if a.keys() != b.keys():
            result = False
        else:
            result = all(_eq(a[key], b[key]) for key in a)  # type: ignore
    elif isinstance(a, list):
        if len(a) != len(b):  # type: ignore
            result = False
        else:
            result = all(starmap(_eq, zip(a, b, strict=True)))  # type: ignore
    elif isinstance(a, float) and isnan(a):
        result = isnan(b)
    else:
        result = a == b

    return result


def _get_lcs(old: list[Any], new: list[Any]) -> list[Any]:
    dp: list[list[int]] = [[0] * (len(new) + 1) for _ in range(len(old) + 1)]
    for i, oldi in enumerate(old):
        for j, newj in enumerate(new):
            if _eq(oldi, newj):
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])

    lcs: list[Any] = []
    i, j = len(old), len(new)
    while i > 0 and j > 0:
        if _eq(old[i - 1], new[j - 1]):
            lcs.append(old[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return lcs[::-1]


def _make_patch(  # noqa: C901
    old: Any, new: Any, patch: list[dict[str, Any]], path: str = "$",
) -> None:
    if _eq(old, new):
        return

    if isinstance(old, dict) and isinstance(new, dict):
        old_keys: KeysView[Any] = old.keys()  # type: ignore
        new_keys: KeysView[Any] = new.keys()  # type: ignore
        for key in old_keys - new_keys:
            patch.append(  # noqa: PERF401
                {"op": "del", "path": f"{path}.{_escape(_replace, key)}"},
            )

        for key in new_keys - old_keys:
            patch.append({  # noqa: PERF401
                "op": "set",
                "path": f"{path}.{_escape(_replace, key)}",
                "value": new[key],
            })

        for key in old_keys & new_keys:
            _make_patch(
                old[key], new[key], patch, f"{path}.{_escape(_replace, key)}",
            )
    elif isinstance(old, list) and isinstance(new, list):
        lcs: list[Any] = _get_lcs(old, new)  # type: ignore
        old_idx = new_idx = lcs_idx = 0
        while old_idx < len(old) or new_idx < len(new):  # type: ignore
            removed: bool = old_idx < len(old) and (  # type: ignore
                lcs_idx >= len(lcs)
                or not _eq(old[old_idx], lcs[lcs_idx])
            )
            inserted: bool = new_idx < len(new) and (  # type: ignore
                lcs_idx >= len(lcs)
                or not _eq(new[new_idx], lcs[lcs_idx])
            )
            if removed and inserted:
                _make_patch(
                    old[old_idx], new[new_idx], patch, f"{path}[{new_idx}]",
                )
                old_idx += 1
                new_idx += 1
            elif removed and not inserted:
                patch.append({"op": "del", "path": f"{path}[{new_idx}]"})
                old_idx += 1
            elif not removed and inserted:
                patch.append({
                    "op": "insert",
                    "path": f"{path}[{new_idx}]",
                    "value": new[new_idx],
                })
                new_idx += 1
            elif not (removed or inserted):
                old_idx += 1
                new_idx += 1
                lcs_idx += 1
    else:
        patch.append({"op": "replace", "path": path, "value": new})


def make_patch(old: Any, new: Any) -> list[dict[str, Any]]:
    """Make a JSON patch from an old and new Python object.

    :param old: the old Python object
    :type old: Any
    :param new: the new Python object
    :type new: Any
    :return: the JSON patch
    :rtype: list[dict[str, Any]]

    >>> import jsonyx as json
    >>> json.make_patch([1, 2, 3, 5], [1, 3, 4, 5])
    [{'op': 'del', 'path': '$[1]'}, {'op': 'insert', 'path': '$[2]', 'value': 4}]
    """
    patch: list[dict[str, Any]] = []
    _make_patch(old, new, patch)
    return patch
