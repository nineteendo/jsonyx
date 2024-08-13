# Copyright (C) 2024 Nice Zombies
"""JSON patcher."""
# TODO(Nice Zombies): add error messages
# TODO(Nice Zombies): export API
# TODO(Nice Zombies): raise JSONSyntaxError
# TODO(Nice Zombies): remove executable code
# TODO(Nice Zombies): update command line options
# TODO(Nice Zombies): write documentation
# TODO(Nice Zombies): write tests
from __future__ import annotations

__all__: list[str] = ["patch"]

import re
from math import isinf
from operator import eq, ge, gt, le, lt, ne
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from sys import maxsize
from typing import TYPE_CHECKING, Any

from jsonyx import dump

if TYPE_CHECKING:
    from collections.abc import Callable

input_json: Any = [
    {
        "cost": 1,
        "price": 2,
    },
    {
        "cost": 2,
        "price": 1,
    },
]
patch_json: list[dict[str, Any]] = [
    {
        "op": "del",
        "path": "$[@.price<@.cost]",
    },
]

_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL

_match_idx: Callable[[str, int], Match[str] | None] = re.compile(
    r"end|-?(?:0|[1-9]\d*)", _FLAGS,
).match
_match_key_chunk: Callable[[str, int], Match[str] | None] = re.compile(
    r"[^!&.<=>[\]~]*", _FLAGS,
).match
_match_number: Callable[[str, int], Match[str] | None] = re.compile(
    r"(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?", _FLAGS,
).match
_match_str_chunk: Callable[[str, int], Match[str] | None] = re.compile(
    r"[^'~]*", _FLAGS,
).match


def _get_key(s: str, end: int = 0) -> tuple[str, int]:
    chunks: list[str] = []
    append_chunk: Callable[[str], None] = chunks.append
    while True:
        if match := _match_key_chunk(s, end):
            end = match.end()
            append_chunk(match.group())

        if s[end:end + 1] != "~":
            return "".join(chunks), end

        end += 1
        try:
            esc: str = s[end]
        except IndexError:
            raise SyntaxError from None

        if esc not in {"!", "&", ".", "<", "=", ">", "[", "]", "~"}:
            raise SyntaxError

        end += 1
        append_chunk(esc)


def _get_targets(
    node: tuple[dict[Any, Any] | list[Any], int | slice | str],
) -> list[dict[Any, Any] | list[Any]]:
    target, key = node
    if isinstance(target, dict) and not isinstance(key, str):
        raise TypeError

    if isinstance(target, list) and isinstance(key, str):
        raise TypeError

    if isinstance(key, slice):
        targets: list[Any] = target[key]
    else:
        targets = [target[key]]  # type: ignore

    if not all(isinstance(target, (dict, list)) for target in targets):
        raise TypeError

    return targets


def _get_idx(match: Match[str]) -> tuple[int, int]:
    if (group := match.group()) == "end":
        idx: int = maxsize
    else:
        idx = int(group)

    return idx, match.end()


def _get_operator(
    s: str, end: int,
) -> tuple[Callable[[Any, Any], Any] | None, int]:
    if s[end:end + 1] == "<":
        operator, end = lt, end + 1
    elif s[end:end + 1] == "<=":
        operator, end = le, end + 2
    elif s[end:end + 2] == "==":
        operator, end = eq, end + 2
    elif s[end:end + 2] == "!=":
        operator, end = ne, end + 2
    elif s[end:end + 1] == ">=":
        operator, end = ge, end + 2
    elif s[end:end + 1] == ">":
        operator, end = gt, end + 1
    else:
        operator = None

    return operator, end


def _get_str(s: str, end: int) -> tuple[str, int]:
    chunks: list[str] = []
    append_chunk: Callable[[str], None] = chunks.append
    while True:
        if match := _match_str_chunk(s, end):
            end = match.end()
            append_chunk(match.group())

        try:
            terminator: str = s[end]
        except IndexError:
            raise SyntaxError from None

        if terminator == "'":
            return "".join(chunks), end + 1

        end += 1
        try:
            esc: str = s[end]
        except IndexError:
            raise SyntaxError from None

        if esc not in {"'", "~"}:
            raise SyntaxError

        end += 1
        append_chunk(esc)


# TODO(Nice Zombies): allow_nan_and_infinity=False
# TODO(Nice Zombies): use_decimal=True
def _get_value(s: str, idx: int) -> tuple[Any, int]:  # noqa: C901
    try:
        nextchar: str = s[idx]
    except IndexError:
        raise SyntaxError from None

    value: Any
    if nextchar == "'":
        value, end = _get_str(s, idx + 1)
    elif nextchar == "n" and s[idx:idx + 4] == "null":
        value, end = None, idx + 4
    elif nextchar == "t" and s[idx:idx + 4] == "true":
        value, end = True, idx + 4
    elif nextchar == "f" and s[idx:idx + 5] == "false":
        value, end = False, idx + 5
    elif number := _match_number(s, idx):
        integer, frac, exp = number.groups()
        end = number.end()
        if frac or exp:
            value = float(integer + (frac or "") + (exp or ""))
            if isinf(value):
                raise SyntaxError
        else:
            value = int(integer)
    elif nextchar == "I" and s[idx:idx + 8] == "Infinity":
        value, end = float("Infinity"), idx + 8
    elif nextchar == "-" and s[idx:idx + 9] == "-Infinity":
        value, end = float("-Infinity"), idx + 9
    else:
        raise SyntaxError

    return value, end


# pylint: disable-next=R0912
def _run_query(  # noqa: C901, PLR0912
    nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]],
    s: str,
    end: int,
) -> tuple[list[tuple[dict[Any, Any] | list[Any], int | slice | str]], int]:
    nodes = [
        (target, key)
        for node in nodes
        for target in _get_targets(node)
        for key in (
            target.keys()
            if isinstance(target, dict) else
            range(len(target))
        )
    ]

    while True:
        negate_filter: bool = s[end:end + 1] == "!"
        if negate_filter:
            end += 1

        key: int | slice | str
        key, end = _get_key(s, end)
        if key != "@":
            raise SyntaxError

        filter_nodes, end = _traverse(nodes, s, end, single=True)
        pairs: list[
            tuple[tuple[dict[Any, Any] | list[Any], int | slice | str], Any]
        ] = []
        for node, (target, key) in zip(nodes, filter_nodes):
            if isinstance(target, dict) and not isinstance(key, str):
                raise TypeError

            if isinstance(target, list) and isinstance(key, str):
                raise TypeError

            if (
                key in target
                if isinstance(target, dict) else
                -len(target) <= key < len(target)  # type: ignore
            ) != negate_filter:
                pairs.append((node, target[key]))  # type: ignore

        operator, end = _get_operator(s, end)
        if operator is None:
            nodes = [node for node, _target in pairs]
        elif negate_filter:
            raise SyntaxError
        elif s[end:end + 1] != "@":
            value, end = _get_value(s, end)
            nodes = [node for node, target in pairs if operator(target, value)]
        else:
            key, end = _get_key(s, end)
            if key != "@":
                raise SyntaxError

            filter2_nodes, end = _traverse(nodes, s, end, single=True)
            nodes = []
            for (node, target), (target2, key) in zip(pairs, filter2_nodes):
                if isinstance(target2, dict) and not isinstance(key, str):
                    raise TypeError

                if isinstance(target2, list) and isinstance(key, str):
                    raise TypeError

                if (
                    key in target2
                    if isinstance(target2, dict) else
                    -len(target2) <= key < len(target2)  # type: ignore
                ) and operator(target, target2[key]):  # type: ignore
                    nodes.append(node)

        if s[end:end + 2] != "&&":
            return nodes, end

        end += 2


# pylint: disable-next=R0912
def _traverse(  # noqa: C901, PLR0912
    nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]],
    s: str,
    end: int,
    *,
    single: bool = False,
) -> tuple[list[tuple[dict[Any, Any] | list[Any], int | slice | str]], int]:
    while True:
        key: int | slice | str
        if (terminator := s[end:end + 1]) == ".":
            key, end = _get_key(s, end + 1)
            nodes = [
                (target, key)
                for node in nodes
                for target in _get_targets(node)
            ]
        elif terminator == "[":
            if match := _match_idx(s, end + 1):
                idx, end = _get_idx(match)
                if s[end:end + 1] != ":":
                    key = idx
                elif single:
                    raise SyntaxError
                elif match := _match_idx(s, end + 1):
                    idx2, end = _get_idx(match)
                    key = slice(idx, idx2)
                else:
                    raise SyntaxError

                nodes = [
                    (target, key)
                    for node in nodes
                    for target in _get_targets(node)
                ]
            elif single:
                raise SyntaxError
            else:
                nodes, end = _run_query(nodes, s, end + 1)

            try:
                terminator = s[end]
            except IndexError:
                raise SyntaxError from None

            if terminator != "]":
                raise SyntaxError

            end += 1
        else:
            return nodes, end


def _traverser(
    nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]], s: str,
) -> list[tuple[dict[Any, Any] | list[Any], int | slice | str]]:
    key, end = _get_key(s)
    if key != "$":
        raise SyntaxError

    nodes, end = _traverse(nodes, s, end)
    if end < len(s):
        raise SyntaxError

    return nodes


# pylint: disable-next=R0912
def patch(  # noqa: C901, PLR0912
    obj: Any, operations: list[dict[str, Any]],
) -> Any:
    """Patch a Python object with a list of operations.

    :param obj: a Python object
    :type obj: Any
    :param operations: a list of operations
    :type operations: list[dict[str, Any]]
    :return: the patched Python object
    :rtype: Any
    """
    root: list[Any] = [obj]
    nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]] = [
        (root, 0),
    ]
    for operation in operations:
        op: str = operation["op"]
        path: str = operation["path"]
        if op == "del":
            # Reverse to preserve indices for queries
            for target, key in reversed(_traverser(nodes, path)):
                if target is root:
                    raise ValueError

                if isinstance(target, dict) and not isinstance(key, str):
                    raise TypeError

                if isinstance(target, list) and isinstance(key, str):
                    raise TypeError

                del target[key]  # type: ignore
        elif op == "insert":
            value: Any = operation["value"]
            # Reverse to preserve indices for queries
            for target, key in reversed(_traverser(nodes, path)):
                if target is root:
                    raise ValueError

                if isinstance(target, dict):
                    raise TypeError

                if not isinstance(key, int):
                    raise TypeError

                target.insert(key, value)
        elif op == "set":
            value = operation["value"]
            for target, key in _traverser(nodes, path):
                if isinstance(target, dict) and not isinstance(key, str):
                    raise TypeError

                if isinstance(target, list) and isinstance(key, str):
                    raise TypeError

                target[key] = value  # type: ignore
        else:
            raise ValueError

    return root[0]


dump(patch(input_json, patch_json), indent=4)
