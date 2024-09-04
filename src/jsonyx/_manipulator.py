# Copyright (C) 2024 Nice Zombies
"""JSON manipulator."""
# TODO(Nice Zombies): add error messages
# TODO(Nice Zombies): raise JSONSyntaxError
# TODO(Nice Zombies): update schema ID
# TODO(Nice Zombies): write specification
from __future__ import annotations

__all__: list[str] = ["Manipulator"]

import re
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from math import isinf
from operator import eq, ge, gt, le, lt, ne
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from typing import TYPE_CHECKING, Any, Literal

from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container

    _AllowList = Container[Literal[
        "comments", "duplicate_keys", "missing_commas", "nan_and_infinity",
        "surrogates", "trailing_comma",
    ] | str]
    _Target = dict[Any, Any] | list[Any]
    _Key = int | slice | str
    _Node = tuple[_Target, _Key]


_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL

_match_idx: Callable[[str, int], Match[str] | None] = re.compile(
    r"-?0|-?[1-9]\d*", _FLAGS,
).match
_match_number: Callable[[str, int], Match[str] | None] = re.compile(
    r"""
    (-?0|-?[1-9]\d*) # integer
    (\.\d+)?         # [frac]
    ([eE][-+]?\d+)?  # [exp]
    """, _FLAGS,
).match
_match_slice: Callable[[str, int], Match[str] | None] = re.compile(
    r"""
    (-?0|-?[1-9]\d*)?       # [start]
    :                       # ":"
    (-?0|-?[1-9]\d*)?       # [stop]
    (?::(-?0|-?[1-9]\d*)?)? # [":" [step]]
    """, _FLAGS,
).match
_match_str_chunk: Callable[[str, int], Match[str] | None] = re.compile(
    r"[^'~]*", _FLAGS,
).match
_match_unquoted_key: Callable[[str, int], Match[str] | None] = re.compile(
    r"(?:\w+|[^\x00-\x7f]+)+", _FLAGS,
).match
_match_whitespace: Callable[[str, int], Match[str] | None] = re.compile(
    r"\ +", _FLAGS,
).match


def _check_query_key(
    target: _Target, key: _Key, *, allow_slice: bool = False,
) -> None:
    if isinstance(target, dict) and not isinstance(key, str):
        raise TypeError

    if isinstance(target, list):
        if allow_slice and isinstance(key, str):
            raise TypeError

        if not (allow_slice or isinstance(key, int)):
            raise TypeError


def _get_query_targets(node: _Node, *, mapping: bool = False) -> list[_Target]:
    target, key = node
    _check_query_key(target, key, allow_slice=not mapping)
    if isinstance(key, slice):
        targets: list[Any] = target[key]
    else:
        targets = [target[key]]  # type: ignore

    if not all(isinstance(target, (dict, list)) for target in targets):
        raise TypeError

    return targets


def _has_key(target: _Target, key: _Key) -> bool:
    if isinstance(target, dict):
        return key in target

    return -len(target) <= key < len(target)  # type: ignore


def _scan_query_operator(
    query: str, end: int,
) -> tuple[Callable[[Any, Any], Any] | None, int]:
    if query[end:end + 2] == "<=":
        operator, end = le, end + 2
    elif query[end:end + 1] == "<":
        operator, end = lt, end + 1
    elif query[end:end + 2] == "==":
        operator, end = eq, end + 2
    elif query[end:end + 2] == "!=":
        operator, end = ne, end + 2
    elif query[end:end + 2] == ">=":
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


class Manipulator:
    """A configurable JSON manipulator.

    :param allow: the allowed JSON deviations, defaults to
                  :data:`jsonyx.allow.NOTHING`
    :type allow: Container[str], optional
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`,
                        defaults to ``False``
    :type use_decimal: bool, optional

    .. versionadded:: 2.0
    """

    def __init__(
        self, *, allow: _AllowList = NOTHING, use_decimal: bool = False,
    ) -> None:
        """Create a new JSON manipulator."""
        self._allow_nan_and_infinity: bool = "nan_and_infinity" in allow
        self._parse_float: Callable[
            [str], Decimal | float,
        ] = Decimal if use_decimal else float
        self._use_decimal: bool = use_decimal

    def _scan_query_value(self, s: str, idx: int = 0) -> tuple[Any, int]:
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
        self, nodes: list[_Node], query: str, end: int,
    ) -> tuple[list[_Node], int]:
        while True:
            negate_filter: bool = query[end:end + 1] == "!"
            if negate_filter:
                end += 1

            filter_nodes, end = self._run_select_query(
                nodes, query, end, mapping=True, relative=True,
            )
            filtered_pairs: list[tuple[_Node, Any]] = [
                (node, filter_target[filter_key])  # type: ignore
                for node, (filter_target, filter_key) in zip(
                    nodes, filter_nodes, strict=True,
                )
                if _has_key(filter_target, filter_key) != negate_filter
            ]
            old_end: int = end
            if match := _match_whitespace(query, end):
                end = match.end()

            operator, end = _scan_query_operator(query, end)
            if operator is None:
                nodes = [node for node, _filter_target in filtered_pairs]
            elif negate_filter:
                raise SyntaxError
            else:
                if match := _match_whitespace(query, end):
                    end = match.end()

                if query[end:end + 1] != "@":
                    value, end = self._scan_query_value(query, end)
                    nodes = [
                        node
                        for node, filter_target in filtered_pairs
                        if operator(filter_target, value)
                    ]
                else:
                    filter2_nodes, end = self._run_select_query(
                        nodes, query, end, mapping=True, relative=True,
                    )
                    nodes = [
                        node
                        for (
                            (node, filter_target),
                            (filter2_target, filter2_key),
                        ) in zip(filtered_pairs, filter2_nodes, strict=True)
                        if _has_key(filter2_target, filter2_key) and operator(
                            filter_target,
                            filter2_target[filter2_key],  # type: ignore
                        )
                    ]

                old_end = end
                if match := _match_whitespace(query, end):
                    end = match.end()

            if query[end:end + 2] != "&&":
                return nodes, old_end

            end += 2
            if match := _match_whitespace(query, end):
                end = match.end()

    def _run_select_query(
        self,
        nodes: list[_Node],
        query: str,
        end: int = 0,
        *,
        allow_slice: bool = False,
        relative: bool = False,
        mapping: bool = False,
    ) -> tuple[list[_Node], int]:
        try:
            key: _Key = query[end]
        except IndexError:
            raise SyntaxError from None

        end += 1
        if relative and key != "@":
            raise SyntaxError

        if not relative and key != "$":
            raise SyntaxError

        while True:
            if (terminator := query[end:end + 1]) == ".":
                if (
                    match := _match_unquoted_key(query, end + 1)
                ) and match.group().isidentifier():
                    key, end = match.group(), match.end()
                else:
                    raise SyntaxError

                nodes = [
                    (target, key)
                    for node in nodes
                    for target in _get_query_targets(node, mapping=mapping)
                ]
            elif terminator == "[":
                end += 1
                if match := _match_slice(query, end):
                    (start, stop, step), end = match.groups(), match.end()
                    key = slice(
                        start and int(start), stop and int(stop),
                        step and int(step),
                    )
                    nodes = [
                        (target, key)
                        for node in nodes
                        for target in _get_query_targets(node, mapping=mapping)
                    ]
                elif match := _match_idx(query, end):
                    key, end = int(match.group()), match.end()
                    nodes = [
                        (target, key)
                        for node in nodes
                        for target in _get_query_targets(node, mapping=mapping)
                    ]
                elif query[end:end + 1] == "'":
                    key, end = _scan_query_string(query, end + 1)
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
                    nodes, end = self._run_filter_query(nodes, query, end)

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

    def _paste_values(
        self,
        current_nodes: list[_Node],
        operation: dict[str, Any],
        values: list[Any],
    ) -> None:
        if (mode := operation["mode"]) == "append":
            dst: str = operation.get("to", "@")
            dst_nodes: list[_Node] = self.run_select_query(
                current_nodes, dst, mapping=True, relative=True,
            )
            for (target, key), value in zip(dst_nodes, values, strict=True):
                list.append(target[key], value)  # type: ignore
        elif mode == "extend":
            dst = operation.get("to", "@")
            dst_nodes = self.run_select_query(
                current_nodes, dst, mapping=True, relative=True,
            )
            for (target, key), value in zip(dst_nodes, values, strict=True):
                list.extend(target[key], value)  # type: ignore
        elif mode == "insert":
            dst = operation["to"]
            dst_nodes = self.run_select_query(
                current_nodes, dst, mapping=True, relative=True,
            )

            # Reverse to preserve indices for queries
            for (current_target, _current_key), (target, key), value in zip(
                current_nodes[::-1],
                dst_nodes[::-1],
                values[::-1],
                strict=True,
            ):
                if target is current_target:
                    raise ValueError

                list.insert(target, key, value)  # type: ignore
        elif mode == "set":
            dst = operation.get("to", "@")
            dst_nodes = self.run_select_query(
                current_nodes,
                dst,
                allow_slice=True,
                mapping=True,
                relative=True,
            )
            for (target, key), value in zip(dst_nodes, values, strict=True):
                target[key] = value  # type: ignore
        elif mode == "update":
            dst = operation.get("to", "@")
            dst_nodes = self.run_select_query(
                current_nodes, dst, mapping=True, relative=True,
            )
            for (target, key), value in zip(dst_nodes, values, strict=True):
                dict.update(target[key], value)  # type: ignore
        else:
            raise ValueError

    def _apply_patch(
        self, root: list[Any], operations: list[dict[str, Any]],
    ) -> None:
        node: _Node = root, 0
        for operation in operations:
            if (op := operation["op"]) == "append":
                path: str = operation.get("path", "$")
                value: Any = operation["value"]
                for target, key in self.run_select_query(node, path):
                    list.append(target[key], value)  # type: ignore
            elif op == "assert":
                path = operation.get("path", "$")
                expr: str = operation["expr"]
                current_nodes: list[_Node] = self.run_select_query(node, path)
                if current_nodes != self.run_filter_query(current_nodes, expr):
                    raise AssertionError
            elif op == "clear":
                path = operation.get("path", "$")
                for target, key in self.run_select_query(node, path):
                    new_target: Any = target[key]  # type: ignore
                    if not isinstance(new_target, (dict, list)):
                        raise TypeError

                    new_target.clear()
            elif op == "copy":
                path = operation.get("path", "$")
                src: str = operation["from"]
                current_nodes = self.run_select_query(node, path)
                values: list[Any] = [
                    deepcopy(target[key])  # type: ignore
                    for target, key in self.run_select_query(
                        current_nodes,
                        src,
                        allow_slice=True,
                        mapping=True,
                        relative=True,
                    )
                ]
                self._paste_values(current_nodes, operation, values)
            elif op == "del":
                path = operation["path"]

                # Reverse to preserve indices for queries
                for target, key in self.run_select_query(
                    node, path, allow_slice=True,
                )[::-1]:
                    if target is root:
                        raise ValueError

                    del target[key]  # type: ignore
            elif op == "extend":
                path = operation.get("path", "$")
                value = operation["value"]
                for target, key in self.run_select_query(node, path):
                    list.extend(target[key], value)  # type: ignore
            elif op == "insert":
                path = operation["path"]
                value = operation["value"]

                # Reverse to preserve indices for queries
                for target, key in self.run_select_query(node, path)[::-1]:
                    if target is root:
                        raise ValueError

                    list.insert(target, key, value)  # type: ignore
            elif op == "move":
                path = operation.get("path", "$")
                src = operation["from"]
                current_nodes = self.run_select_query(node, path)
                src_nodes: list[_Node] = self.run_select_query(
                    current_nodes,
                    src,
                    allow_slice=True,
                    mapping=True,
                    relative=True,
                )
                values = []

                # Reverse to preserve indices for queries
                for (current_target, _current_key), (target, key) in zip(
                    current_nodes[::-1], src_nodes[::-1], strict=True,
                ):
                    if target is current_target:
                        raise ValueError

                    values.append(target[key])  # type: ignore
                    del target[key]  # type: ignore

                # Undo reverse
                self._paste_values(current_nodes, operation, values[::-1])
            elif op == "reverse":
                path = operation.get("path", "$")
                for target, key in self.run_select_query(node, path):
                    list.reverse(target[key])  # type: ignore
            elif op == "set":
                path = operation.get("path", "$")
                value = operation["value"]
                for target, key in self.run_select_query(
                    node, path, allow_slice=True,
                ):
                    target[key] = value  # type: ignore
            elif op == "sort":
                path = operation.get("path", "$")
                reverse: bool = operation.get("reverse", False)
                for target, key in self.run_select_query(
                    node, path, allow_slice=True,
                ):
                    list.sort(target[key], reverse=reverse)  # type: ignore
            elif op == "update":
                path = operation.get("path", "$")
                value = operation["value"]
                for target, key in self.run_select_query(node, path):
                    dict.update(target[key], value)  # type: ignore
            else:
                raise ValueError

    def apply_patch(
        self, obj: Any, patch: dict[str, Any] | list[dict[str, Any]],
    ) -> Any:
        """Apply a JSON patch to a Python object.

        :param obj: a Python object
        :type obj: Any
        :param patch: a JSON patch
        :type patch: dict[str, Any] | list[dict[str, Any]]
        :raises AssertionError: if an assertion fails
        :raises SyntaxError: if a query is invalid
        :raises TypeError: if a value has the wrong type
        :raises ValueError: if a value is invalid
        :return: the patched Python object
        :rtype: Any

        >>> import jsonyx as json
        >>> json.Manipulator().apply_patch([1, 2, 3], {'op': 'del', 'path': '$[1]'})
        [1, 3]

        .. tip::
            Using queries instead of indices is more robust.
        """
        root: list[Any] = [obj]
        if isinstance(patch, dict):
            patch = [patch]

        self._apply_patch(root, patch)
        return root[0]

    def run_select_query(
        self,
        nodes: _Node | list[_Node],
        query: str,
        *,
        allow_slice: bool = False,
        mapping: bool = False,
        relative: bool = False,
    ) -> list[_Node]:
        """Run a JSON select query on a node or a list of nodes.

        :param nodes: a node or a list of nodes
        :type nodes: _Node | list[_Node]
        :param query: a JSON select query
        :type query: str
        :param allow_slice: allow slice, defaults to ``False``
        :type allow_slice: bool, optional
        :param mapping: map every input node to a single output node, defaults
                        to ``False``
        :type mapping: bool, optional
        :param relative: query must start with ``"@"`` instead of ``"$"``,
                         defaults to ``False``
        :type relative: bool, optional
        :raises SyntaxError: if the select query is invalid
        :raises ValueError: if a value is invalid
        :return: the selected list of nodes
        :rtype: list[_Node]

        >>> import jsonyx as json
        >>> root = [[1, 2, 3, 4, 5, 6]]
        >>> node = root, 0
        >>> for target, key in json.Manipulator().run_select_query(node, "$[@ > 3]"):
        ...     target[key] = None
        ...
        >>> root[0]
        [1, 2, 3, None, None, None]

        .. tip::
            Using queries instead of indices is more robust.
        """
        if isinstance(nodes, tuple):
            nodes = [nodes]

        selected_nodes, end = self._run_select_query(
            nodes,
            query,
            allow_slice=allow_slice,
            relative=relative,
            mapping=mapping,
        )
        if query[end:end + 1] == "?":
            end += 1
        elif not selected_nodes and nodes:
            raise ValueError

        if end < len(query):
            raise SyntaxError

        return selected_nodes

    def run_filter_query(
        self, nodes: _Node | list[_Node], query: str,
    ) -> list[_Node]:
        """Run a JSON filter query on a node or a list of nodes.

        :param nodes: a node or a list of nodes
        :type nodes: _Node | list[_Node]
        :param query: a JSON filter query
        :type query: str
        :raises SyntaxError: if the filter query is invalid
        :return: the filtered list of nodes
        :rtype: list[_Node]

        >>> import jsonyx as json
        >>> node = [None], 0
        >>> assert json.Manipulator().run_filter_query(node, "@ == null")
        """
        if isinstance(nodes, tuple):
            nodes = [nodes]

        nodes, end = self._run_filter_query(nodes, query, 0)
        if end < len(query):
            raise SyntaxError

        return nodes

    def load_query_value(self, s: str) -> Any:
        """Deserialize a JSON query value to a Python object.

        :param s: a JSON query value
        :type s: str
        :raises SyntaxError: if the query value is invalid
        :return: a Python object
        :rtype: Any

        >>> import jsonyx as json
        >>> json.Manipulator().load_query_value("'~'foo'")
        "'foo"
        """
        obj, end = self._scan_query_value(s)
        if end < len(s):
            raise SyntaxError

        return obj


Manipulator.__module__ = "jsonyx"
