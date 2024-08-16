# Copyright (C) 2024 Nice Zombies
"""JSON manipulator."""
# TODO(Nice Zombies): generate patch
# TODO(Nice Zombies): update schema
# TODO(Nice Zombies): write documentation
# TODO(Nice Zombies): write specification
from __future__ import annotations

__all__: list[str] = ["Manipulator"]

import re
from decimal import Decimal, InvalidOperation
from math import isinf
from operator import eq, ge, gt, le, lt, ne
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from sys import maxsize
from typing import TYPE_CHECKING, Any, Literal

from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container

    _AllowList = Container[Literal[
        "comments", "duplicate_keys", "missing_commas", "nan_and_infinity",
        "surrogates", "trailing_comma",
    ] | str]


_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL

_match_idx: Callable[[str, int], Match[str] | None] = re.compile(
    r"end|start|-?(?:0|[1-9]\d*)", _FLAGS,
).match
_match_int: Callable[[str, int], Match[str] | None] = re.compile(
    r"-?(?:0|[1-9]\d*)", _FLAGS,
).match
_match_key_chunk: Callable[[str, int], Match[str] | None] = re.compile(
    r"[^!&.<=>?[\]~]*", _FLAGS,
).match
_match_number: Callable[[str, int], Match[str] | None] = re.compile(
    r"(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?", _FLAGS,
).match
_match_str_chunk: Callable[[str, int], Match[str] | None] = re.compile(
    r"[^'~]*", _FLAGS,
).match


def _check_query_key(
    target: dict[Any, Any] | list[Any], key: int | slice | str,
    *,
    allow_slice: bool = False,
) -> None:
    if isinstance(target, dict) and not isinstance(key, str):
        raise TypeError

    if isinstance(target, list):
        if allow_slice and isinstance(key, str):
            raise TypeError

        if not allow_slice and not isinstance(key, int):
            raise TypeError


def _get_query_targets(
    node: tuple[dict[Any, Any] | list[Any], int | slice | str],
    *,
    mapping: bool = False,
) -> list[dict[Any, Any] | list[Any]]:
    target, key = node
    _check_query_key(target, key, allow_slice=True)
    if not isinstance(key, slice):
        targets: list[Any] = [target[key]]  # type: ignore
    elif mapping:
        raise ValueError
    else:
        targets = target[key]

    if not all(isinstance(target, (dict, list)) for target in targets):
        raise TypeError

    return targets


def _get_query_idx(match: Match[str]) -> tuple[int, int]:
    if (group := match.group()) == "end":
        idx: int = maxsize
    elif group == "start":
        idx = -maxsize - 1
    else:
        idx = int(group)

    return idx, match.end()


def _scan_query_key(query: str, end: int = 0) -> tuple[str, int]:
    chunks: list[str] = []
    append_chunk: Callable[[str], None] = chunks.append
    while True:
        if match := _match_key_chunk(query, end):
            end = match.end()
            append_chunk(match.group())

        if query[end:end + 1] != "~":
            return "".join(chunks), end

        end += 1
        try:
            esc: str = query[end]
        except IndexError:
            raise SyntaxError from None

        if esc not in {"!", "&", ".", "<", "=", ">", "?", "[", "]", "~"}:
            raise SyntaxError

        end += 1
        append_chunk(esc)


def _scan_query_operator(
    query: str, end: int,
) -> tuple[Callable[[Any, Any], Any] | None, int]:
    if query[end:end + 1] == "<":
        operator, end = lt, end + 1
    elif query[end:end + 1] == "<=":
        operator, end = le, end + 2
    elif query[end:end + 2] == "==":
        operator, end = eq, end + 2
    elif query[end:end + 2] == "!=":
        operator, end = ne, end + 2
    elif query[end:end + 1] == ">=":
        operator, end = ge, end + 2
    elif query[end:end + 1] == ">":
        operator, end = gt, end + 1
    else:
        operator = None

    return operator, end


def _scan_query_string(s: str, end: int) -> tuple[str, int]:
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


# TODO(Nice Zombies): add error messages
# TODO(Nice Zombies): add paste
# TODO(Nice Zombies): raise JSONSyntaxError
# pylint: disable-next=R0915
class Manipulator:
    """JSON manipulator."""

    def __init__(
        self, *, allow: _AllowList = NOTHING, use_decimal: bool = False,
    ) -> None:
        """Create a new JSON manipulator.

        :param allow: the allowed JSON deviations, defaults to NOTHING
        :type allow: Container[str], optional
        :param use_decimal: use decimal instead of float, defaults to False
        :type use_decimal: bool, optional
        """
        self._allow_nan_and_infinity: bool = "nan_and_infinity" in allow
        self._parse_float: Callable[
            [str], Decimal | float,
        ] = Decimal if use_decimal else float
        self._use_decimal: bool = use_decimal

    # pylint: disable-next=R0912
    def _scan_query_value(  # noqa: C901, PLR0912
        self, s: str, idx: int = 0,
    ) -> tuple[Any, int]:
        try:
            nextchar: str = s[idx]
        except IndexError:
            raise SyntaxError from None

        value: Any
        if nextchar == "'":
            value, end = _scan_query_string(s, idx + 1)
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
                try:
                    value = self._parse_float(
                        integer + (frac or "") + (exp or ""),
                    )
                except InvalidOperation:
                    raise SyntaxError from None

                if not self._use_decimal and isinf(value):
                    raise SyntaxError
            else:
                value = int(integer)
        elif nextchar == "I" and s[idx:idx + 8] == "Infinity":
            if not self._allow_nan_and_infinity:
                raise SyntaxError

            value, end = float("Infinity"), idx + 8
        elif nextchar == "-" and s[idx:idx + 9] == "-Infinity":
            if not self._allow_nan_and_infinity:
                raise SyntaxError

            value, end = float("-Infinity"), idx + 9
        else:
            raise SyntaxError

        return value, end

    def _run_filter_query(
        self,
        nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]],
        query: str,
        end: int,
    ) -> tuple[
        list[tuple[dict[Any, Any] | list[Any], int | slice | str]], int,
    ]:
        while True:
            negate_filter: bool = query[end:end + 1] == "!"
            if negate_filter:
                end += 1

            filter_nodes, end = self._run_select_query(
                nodes, query, end, mapping=True, relative=True,
            )
            pairs: list[tuple[
                tuple[dict[Any, Any] | list[Any], int | slice | str], Any,
            ]] = [
                (node, target[key])  # type: ignore
                for node, (target, key) in zip(nodes, filter_nodes)
                if (
                    key in target
                    if isinstance(target, dict) else
                    -len(target) <= key < len(target)  # type: ignore
                ) != negate_filter
            ]
            operator, end = _scan_query_operator(query, end)
            if operator is None:
                nodes = [node for node, _target in pairs]
            elif negate_filter:
                raise SyntaxError
            elif query[end:end + 1] != "@":
                value, end = self._scan_query_value(query, end)
                nodes = [
                    node for node, target in pairs if operator(target, value)
                ]
            else:
                filter2_nodes, end = self._run_select_query(
                    nodes, query, end, mapping=True, relative=True,
                )
                nodes = [
                    node
                    for (node, target), (target2, key) in zip(
                        pairs, filter2_nodes,
                    )
                    if (
                        key in target2
                        if isinstance(target2, dict) else
                        -len(target2) <= key < len(target2)  # type: ignore
                    ) and operator(target, target2[key])  # type: ignore
                ]

            if query[end:end + 2] != "&&":
                return nodes, end

            end += 2

    # pylint: disable-next=R0912, R0913
    def _run_select_query(  # noqa: C901, PLR0912, PLR0913
        self,
        nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]],
        query: str,
        end: int = 0,
        *,
        allow_slice: bool = False,
        relative: bool = False,
        mapping: bool = False,
    ) -> tuple[
        list[tuple[dict[Any, Any] | list[Any], int | slice | str]], int,
    ]:
        key: int | slice | str
        key, end = _scan_query_key(query)
        if relative and key != "@":
            raise SyntaxError

        if not relative and key != "$":
            raise SyntaxError

        while True:
            if (terminator := query[end:end + 1]) == ".":
                key, end = _scan_query_key(query, end + 1)
                nodes = [
                    (target, key)
                    for node in nodes
                    for target in _get_query_targets(node, mapping=mapping)
                ]
            elif terminator == "[":
                if match := _match_idx(query, end + 1):
                    idx, end = _get_query_idx(match)
                    if query[end:end + 1] != ":":
                        key = idx
                    elif match := _match_idx(query, end + 1):
                        idx2, end = _get_query_idx(match)
                        if query[end:end + 1] != ":":
                            key = slice(idx, idx2)
                        elif match := _match_int(query, end + 1):
                            step, end = int(match.group()), match.end()
                            key = slice(idx, idx2, step)
                        else:
                            raise SyntaxError
                    else:
                        raise SyntaxError

                    nodes = [
                        (target, key)
                        for node in nodes
                        for target in _get_query_targets(node, mapping=mapping)
                    ]
                elif mapping:
                    raise SyntaxError
                else:
                    nodes = [
                        (target, key)
                        for node in nodes
                        for target in _get_query_targets(node, mapping=True)
                        for key in (
                            target.keys()
                            if isinstance(target, dict) else
                            range(len(target))
                        )
                    ]
                    nodes, end = self._run_filter_query(nodes, query, end + 1)

                try:
                    terminator = query[end]
                except IndexError:
                    raise SyntaxError from None

                if terminator != "]":
                    raise SyntaxError

                end += 1
            else:
                for target, key in nodes:
                    _check_query_key(target, key, allow_slice=allow_slice)

                return nodes, end

    # pylint: disable-next=R0912, R0915, R0914
    def _apply_patch(  # noqa: C901, PLR0912
        self,
        root: list[Any], operations: list[dict[str, Any]],
    ) -> None:
        nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]] = [
            (root, 0),
        ]
        for operation in operations:
            op: str = operation["op"]

            # TODO(Nice Zombies): add copy operation
            # TODO(Nice Zombies): add move operation
            if op == "append":
                path: str = operation.get("path", "$")
                value: Any = operation["value"]
                for target, key in self.run_select_query(nodes, path):
                    list.append(target[key], value)  # type: ignore
            elif op == "assert":
                path = operation.get("path", "$")
                expr: str = operation["expr"]
                new_nodes: list[
                    tuple[dict[Any, Any] | list[Any], int | slice | str]
                ] = self.run_select_query(nodes, path)
                if new_nodes != self.run_filter_query(nodes, expr):
                    raise ValueError
            elif op == "clear":
                path = operation.get("path", "$")
                for target, key in self.run_select_query(nodes, path):
                    new_target: Any = target[key]  # type: ignore
                    if not isinstance(new_target, (dict, list)):
                        raise TypeError

                    new_target.clear()
            elif op == "del":
                path = operation["path"]

                # Reverse to preserve indices for queries
                for target, key in self.run_select_query(
                    nodes, path, allow_slice=True,
                )[::-1]:
                    if target is root:
                        raise ValueError

                    del target[key]  # type: ignore
            elif op == "extend":
                path = operation.get("path", "$")
                value = operation["value"]
                for target, key in self.run_select_query(nodes, path):
                    list.extend(target[key], value)  # type: ignore
            elif op == "insert":
                path = operation["path"]
                value = operation["value"]

                # Reverse to preserve indices for queries
                for target, key in self.run_select_query(nodes, path)[::-1]:
                    if target is root:
                        raise ValueError

                    list.insert(target, key, value)  # type: ignore
            elif op == "reverse":
                path = operation.get("path", "$")
                for target, key in self.run_select_query(nodes, path):
                    list.reverse(target[key])  # type: ignore
            elif op == "set":
                path = operation.get("path", "$")
                value = operation["value"]
                for target, key in self.run_select_query(
                    nodes, path, allow_slice=True,
                ):
                    target[key] = value  # type: ignore
            elif op == "sort":
                path = operation.get("path", "$")
                reverse: bool = operation.get("reverse", False)
                for target, key in self.run_select_query(
                    nodes, path, allow_slice=True,
                ):
                    list.sort(target[key], reverse=reverse)  # type: ignore
            elif op == "update":
                path = operation.get("path", "$")
                value = operation["value"]
                for target, key in self.run_select_query(nodes, path):
                    dict.update(target[key], value)  # type: ignore
            else:
                raise ValueError

    def load_query_value(self, s: str) -> Any:
        """Deserialize a JSON file to a Python object.

        :param s: a JSON query value
        :type s: str
        :raises SyntaxError: if the query value is invalid
        :return: a Python object
        :rtype: Any
        """
        obj, end = self._scan_query_value(s)
        if end < len(s):
            raise SyntaxError

        return obj

    def run_filter_query(
        self,
        nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]],
        query: str,
    ) -> list[tuple[dict[Any, Any] | list[Any], int | slice | str]]:
        """Run a JSON filter query on a list of nodes.

        :param nodes: a list of nodes
        :type nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]]
        :param query: a JSON filter query
        :type query: str
        :raises SyntaxError: if the filter query is invalid
        :return: the filtered list of nodes
        :rtype: list[tuple[dict[Any, Any] | list[Any], int | slice | str]]
        """
        nodes, end = self._run_filter_query(nodes, query, 0)
        if end < len(query):
            raise SyntaxError

        return nodes

    # pylint: disable-next=R0913
    def run_select_query(
        self,
        nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]],
        query: str,
        *,
        allow_slice: bool = False,
        mapping: bool = False,
        relative: bool = False,
    ) -> list[tuple[dict[Any, Any] | list[Any], int | slice | str]]:
        """Run a JSON select query on a list of nodes.

        :param nodes: a list of nodes
        :type nodes: list[tuple[dict[Any, Any] | list[Any], int | slice | str]]
        :param query: a JSON select query
        :type query: str
        :param allow_slice: allow slice, defaults to False
        :type allow_slice: bool, optional
        :param mapping: map every input node to a single output node, defaults
                        to False
        :type mapping: bool, optional
        :param relative: query must start with "@" instead of "$", defaults to
                         False
        :type relative: bool, optional
        :raises SyntaxError: if the select query is invalid
        :raises ValueError: if a value is invalid
        :return: the selected list of nodes
        :rtype: list[tuple[dict[Any, Any] | list[Any], int | slice | str]]
        """
        nodes, end = self._run_select_query(
            nodes,
            query,
            allow_slice=allow_slice,
            relative=relative,
            mapping=mapping,
        )
        if query[end:end + 1] == "?":
            end += 1
        elif not nodes:
            raise ValueError

        if end < len(query):
            raise SyntaxError

        return nodes

    def apply_patch(
        self, obj: Any, patch: dict[str, Any] | list[dict[str, Any]],
    ) -> Any:
        """Apply a JSON patch to a Python object.

        :param obj: a Python object
        :type obj: Any
        :param patch: a JSON patch
        :type patch: dict[str, Any] | list[dict[str, Any]]
        :raises SyntaxError: if the patch is invalid
        :raises TypeError: if a value has the wrong type
        :raises ValueError: if a value is invalid
        :return: the patched Python object
        :rtype: Any
        """
        root: list[Any] = [obj]
        if isinstance(patch, dict):
            patch = [patch]

        self._apply_patch(root, patch)
        return root[0]
