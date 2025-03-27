"""JSON differ."""
from __future__ import annotations

__all__: list[str] = ["make_patch"]

import re
from decimal import Decimal
from math import isnan
from re import DOTALL, MULTILINE, VERBOSE, Match
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, KeysView

    _Operation = dict[str, Any]
    _SubFunc = Callable[[str | Callable[[Match[str]], str], str], str]

_REPL: str = r"~\1"

_escape: _SubFunc = re.compile(r"(['~])", VERBOSE | MULTILINE | DOTALL).sub


def _encode_query_key(key: str) -> str:
    return f".{key}" if key.isidentifier() else f"['{_escape(_REPL, key)}']"


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
            result = all(map(_eq, a, b))  # type: ignore
    elif isinstance(a, (Decimal, float)) and isnan(a):
        result = isnan(b)
    else:
        result = a == b

    return result


def _get_lcs(old: list[Any], new: list[Any]) -> list[Any]:
    dp: list[list[int]] = [[0] * (len(new) + 1) for _ in range(len(old) + 1)]
    for i, old_value in enumerate(old):
        for j, new_value in enumerate(new):
            if _eq(old_value, new_value):
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


def _make_patch(
    old: Any, new: Any, patch: list[_Operation], path: str = "$",
) -> None:
    if _eq(old, new):
        return

    if isinstance(old, dict) and isinstance(new, dict):
        old_keys: KeysView[Any] = old.keys()  # type: ignore
        new_keys: KeysView[Any] = new.keys()  # type: ignore
        for key in old_keys:
            new_path: str = f"{path}{_encode_query_key(key)}"
            if key in new_keys:
                _make_patch(old[key], new[key], patch, new_path)
            else:
                patch.append({"op": "del", "path": new_path})

        for key in new_keys:
            if key not in old_keys:  # preserve order
                new_path = f"{path}{_encode_query_key(key)}"
                patch.append(
                    {"op": "set", "path": new_path, "value": new[key]},
                )
    elif isinstance(old, list) and isinstance(new, list):
        lcs: list[Any] = _get_lcs(old, new)  # type: ignore
        old_idx = new_idx = lcs_idx = 0
        while old_idx < len(old) or new_idx < len(new):  # type: ignore
            new_path = f"{path}[{new_idx}]"
            removed: bool = old_idx < len(old) and (  # type: ignore
                lcs_idx >= len(lcs) or not _eq(old[old_idx], lcs[lcs_idx])
            )
            inserted: bool = new_idx < len(new) and (  # type: ignore
                lcs_idx >= len(lcs) or not _eq(new[new_idx], lcs[lcs_idx])
            )
            if removed and inserted:
                _make_patch(old[old_idx], new[new_idx], patch, new_path)
                old_idx += 1
                new_idx += 1
            elif removed:
                patch.append({"op": "del", "path": new_path})
                old_idx += 1
            elif inserted:
                patch.append(
                    {"op": "insert", "path": new_path, "value": new[new_idx]},
                )
                new_idx += 1
            else:
                old_idx += 1
                new_idx += 1
                lcs_idx += 1
    else:
        patch.append({"op": "set", "path": path, "value": new})


def make_patch(old: Any, new: Any) -> list[_Operation]:
    """Make a JSON patch from two Python objects.

    .. versionadded:: 2.0

    :param old: the old Python object
    :param new: the new Python object
    :raises RecursionError: if the object is too deeply nested
    :return: the :doc:`JSON patch </json-patch-spec>`

    Example:
        >>> import jsonyx as json
        >>> json.make_patch([1, 2, 3], [1, 3])
        [{'op': 'del', 'path': '$[1]'}]

    """
    patch: list[_Operation] = []
    _make_patch(old, new, patch)
    return patch


make_patch.__module__ = "jsonyx"
