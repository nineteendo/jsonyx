"""JSON manipulator."""
from __future__ import annotations

__all__: list[str] = ["Manipulator"]

import re
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from operator import eq, ge, gt, le, lt, ne
from re import DOTALL, MULTILINE, VERBOSE, Match, RegexFlag
from typing import TYPE_CHECKING, Any

from jsonyx import JSONSyntaxError
from jsonyx.allow import NOTHING

if TYPE_CHECKING:
    from collections.abc import Callable, Container

    _Target = dict[Any, Any] | list[Any]
    _Node = tuple[_Target, Any]
    _MatchFunc = Callable[[str, int], Match[str] | None]
    _Operation = dict[str, Any]
    _Operator = Callable[[Any, Any], Any]


_FLAGS: RegexFlag = VERBOSE | MULTILINE | DOTALL

_match_idx: _MatchFunc = re.compile(r"-?0|-?[1-9][0-9]*", _FLAGS).match
_match_number: _MatchFunc = re.compile(
    r"""
    (-?0|-?[1-9][0-9]*) # integer
    (\.[0-9]+)?         # [frac]
    ([eE][-+]?[0-9]+)?  # [exp]
    """, _FLAGS,
).match
_match_slice: _MatchFunc = re.compile(
    r"""
    (-?0|-?[1-9][0-9]*)?       # [start]
    :                          # ":"
    (-?0|-?[1-9][0-9]*)?       # [stop]
    (?::(-?0|-?[1-9][0-9]*)?)? # [":" [step]]
    """, _FLAGS,
).match
_match_str_chunk: _MatchFunc = re.compile(r"[^'~]*", _FLAGS).match
_match_unquoted_key: _MatchFunc = re.compile(
    r"(?:\w+|[^\x00-\x7f]+)+", _FLAGS,
).match
_match_whitespace: _MatchFunc = re.compile(r"\ +", _FLAGS).match


def _errmsg(msg: str, query: str, start: int, end: int = 0) -> JSONSyntaxError:
    return JSONSyntaxError(msg, "<query>", query, start, end)


def _check_query_key(
    target: _Target, key: Any, *, allow_slice: bool = False,
) -> None:
    if isinstance(target, dict):
        if not isinstance(key, str):
            msg: str = f"Dict key must be str, not {type(key).__name__}"
            raise TypeError(msg)
    elif allow_slice:
        if isinstance(key, str):
            msg = f"List index must be int or slice, not {type(key).__name__}"
            raise TypeError(msg)
    elif not isinstance(key, int):
        msg = f"List index must be int, not {type(key).__name__}"
        raise TypeError(msg)


def _get_query_targets(
    node: _Node, *, relative: bool = False,
) -> list[_Target]:
    target, key = node
    _check_query_key(target, key, allow_slice=not relative)
    if isinstance(key, slice):
        new_targets: list[Any] = target[key]
    else:
        new_targets = [target[key]]

    for new_target in new_targets:
        if not isinstance(new_target, (dict, list)):
            msg: str = (
                f"Target must be dict or list, not {type(new_target).__name__}"
            )
            raise TypeError(msg)

    return new_targets


def _has_key(target: _Target, key: Any) -> bool:
    if isinstance(target, dict):
        return key in target

    return -len(target) <= key < len(target)  # type: ignore


def _scan_query_operator(query: str, end: int) -> tuple[_Operator | None, int]:
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
    str_idx: int = end - 1
    while True:
        if match := _match_str_chunk(s, end):
            end = match.end()
            append_chunk(match.group())

        try:
            terminator: str = s[end]
        except IndexError:
            msg: str = "Unterminated string"
            raise _errmsg(msg, s, str_idx, end) from None

        if terminator == "'":
            return "".join(chunks), end + 1

        end += 1
        try:
            esc: str = s[end]
        except IndexError:
            msg = "Expecting escaped character"
            raise _errmsg(msg, s, end) from None

        if esc not in {"'", "~"}:
            msg = "Invalid tilde escape"
            raise _errmsg(msg, s, end - 1, end + 1)

        end += 1
        append_chunk(esc)


def _asc_range(r: range) -> range:
    return r if r.step > 0 else r[::-1]


class Manipulator:
    """A configurable JSON manipulator.

    .. versionadded:: 2.0

    :param allow: the JSON deviations from :mod:`jsonyx.allow`
    :param use_decimal: use :class:`decimal.Decimal` instead of :class:`float`
    """

    def __init__(
        self, *, allow: Container[str] = NOTHING, use_decimal: bool = False,
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
            msg: str = "Expecting value"
            raise _errmsg(msg, s, idx) from None

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
            if not frac and not exp:
                try:
                    value = int(integer)
                except ValueError:
                    msg = "Invalid number"
                    raise _errmsg(msg, s, idx, end) from None
            else:
                try:
                    value = self._parse_float(
                        integer + (frac or "") + (exp or ""),
                    )
                except InvalidOperation:
                    msg = "Invalid number"
                    raise _errmsg(msg, s, idx, end) from None
        elif nextchar == "I" and s[idx:idx + 8] == "Infinity":
            if not self._allow_nan_and_infinity:
                msg = "Infinity is not allowed"
                raise _errmsg(msg, s, idx, idx + 8)

            value, end = self._parse_float("Infinity"), idx + 8
        elif nextchar == "-" and s[idx:idx + 9] == "-Infinity":
            if not self._allow_nan_and_infinity:
                msg = "-Infinity is not allowed"
                raise _errmsg(msg, s, idx, idx + 9)

            value, end = self._parse_float("-Infinity"), idx + 9
        else:
            msg = "Expecting value"
            raise _errmsg(msg, s, idx)

        return value, end

    def _apply_filter(
        self, nodes: list[_Node], query: str, end: int,
    ) -> tuple[list[_Node], int]:
        while True:
            negate_filter: bool = query[end:end + 1] == "!"
            if negate_filter:
                end += 1

            filter_nodes, end = self._select_nodes(
                nodes, query, end, relative=True,
            )
            filtered_pairs: list[tuple[_Node, _Node]] = [
                (node, (filter_target, filter_key))
                for node, (filter_target, filter_key) in zip(
                    nodes, filter_nodes,
                )
                if _has_key(filter_target, filter_key) != negate_filter
            ]
            old_end: int = end
            if match := _match_whitespace(query, end):
                end = match.end()

            operator_idx: int = end
            operator, end = _scan_query_operator(query, end)
            if operator is None:
                nodes = [node for node, _filter_node in filtered_pairs]
            elif negate_filter:
                msg: str = "Unexpected operator"
                raise _errmsg(msg, query, operator_idx, end)
            else:
                if match := _match_whitespace(query, end):
                    end = match.end()

                value, end = self._scan_query_value(query, end)
                nodes = [
                    node
                    for node, (filter_target, filter_key) in filtered_pairs
                    if operator(filter_target[filter_key], value)
                ]
                old_end = end
                if match := _match_whitespace(query, end):
                    end = match.end()

            if query[end:end + 2] != "&&":
                return nodes, old_end

            end += 2
            if match := _match_whitespace(query, end):
                end = match.end()

    def _select_nodes(
        self,
        nodes: list[_Node],
        query: str,
        end: int = 0,
        *,
        allow_slice: bool = False,
        relative: bool = False,
    ) -> tuple[list[_Node], int]:
        if relative:
            if query[end:end + 1] != "@":
                msg: str = "Expecting a relative query"
                raise _errmsg(msg, query, end)
        elif query[end:end + 1] != "$":
            msg = "Expecting an absolute query"
            raise _errmsg(msg, query, end)

        end += 1
        while True:
            key: Any
            if query[end:end + 1] == "?":
                if relative:
                    msg = "Optional markers are not allowed in relative query"
                    raise _errmsg(msg, query, end, end + 1)

                end += 1
                for target, key in nodes:
                    _check_query_key(target, key, allow_slice=True)

                nodes = [
                    (target, key)
                    for (target, key) in nodes
                    if isinstance(key, slice) or _has_key(target, key)
                ]

            if (terminator := query[end:end + 1]) == ".":
                end += 1
                if (
                    match := _match_unquoted_key(query, end)
                ) and match.group().isidentifier():
                    key, end = match.group(), match.end()
                else:
                    msg = "Expecting property"
                    raise _errmsg(msg, query, end)

                nodes = [
                    (target, key)
                    for node in nodes
                    for target in _get_query_targets(node, relative=relative)
                ]
            elif terminator == "{":
                end += 1
                nodes = [
                    (target, new_key)
                    for target, key in nodes
                    for new_key in (
                        _asc_range(range(len(target))[key])
                        if isinstance(key, slice) else
                        [key]
                    )
                ]
                if relative:
                    msg = "Conditions are not allowed in relative query"
                    raise _errmsg(msg, query, end)

                nodes, end = self._apply_filter(nodes, query, end)
                if query[end:end + 1] != "}":
                    msg = "Expecting a closing bracket"
                    raise _errmsg(msg, query, end)

                end += 1
            elif terminator == "[":
                end += 1
                targets: list[_Target] = [
                    target
                    for node in nodes
                    for target in _get_query_targets(node, relative=relative)
                ]
                if match := _match_slice(query, end):
                    (start, stop, step), end = match.groups(), match.end()
                    try:
                        if start is not None:
                            start = int(start)
                    except ValueError:
                        msg = "Start is too big"
                        raise _errmsg(
                            msg, query, match.start(1), match.end(1),
                        ) from None

                    try:
                        if stop is not None:
                            stop = int(stop)
                    except ValueError:
                        msg = "Stop is too big"
                        raise _errmsg(
                            msg, query, match.start(2), match.end(2),
                        ) from None

                    try:
                        if step is not None:
                            step = int(step)
                    except ValueError:
                        msg = "Step is too big"
                        raise _errmsg(
                            msg, query, match.start(3), match.end(3),
                        ) from None

                    key = slice(start, stop, step)
                    nodes = [(target, key) for target in targets]
                elif match := _match_idx(query, end):
                    end = match.end()
                    try:
                        key = int(match.group())
                    except ValueError:
                        msg = "Index is too big"
                        raise _errmsg(msg, query, match.start(), end) from None

                    nodes = [(target, key) for target in targets]
                elif query[end:end + 1] == "'":
                    key, end = _scan_query_string(query, end + 1)
                    nodes = [(target, key) for target in targets]
                elif relative:
                    msg = "Filters are not allowed in relative query"
                    raise _errmsg(msg, query, end)
                else:
                    nodes = [
                        (target, key)
                        for target in targets
                        for key in (
                            target.keys()
                            if isinstance(target, dict) else
                            range(len(target))
                        )
                    ]
                    nodes, end = self._apply_filter(nodes, query, end)

                if query[end:end + 1] != "]":
                    msg = "Expecting a closing bracket"
                    raise _errmsg(msg, query, end)

                end += 1
            else:
                for target, key in nodes:
                    _check_query_key(target, key, allow_slice=allow_slice)

                return nodes, end

    def _paste_values(
        self,
        current_nodes: list[_Node],
        values: list[Any],
        operation: _Operation,
    ) -> None:
        if (mode := operation["mode"]) == "append":
            dst: str = operation.get("to", "@")
            dst_nodes: list[_Node] = self.select_nodes(
                current_nodes, dst, relative=True,
            )
            for (target, key), value in zip(dst_nodes, values):
                list.append(target[key], value)  # type: ignore
        elif mode == "extend":
            dst = operation.get("to", "@")
            dst_nodes = self.select_nodes(current_nodes, dst, relative=True)
            for (target, key), value in zip(dst_nodes, values):
                list.extend(target[key], value)  # type: ignore
        elif mode == "insert":
            dst = operation["to"]
            dst_nodes = self.select_nodes(current_nodes, dst, relative=True)

            # Future proofing: Reverse to preserve indices for filters
            for (current_target, _current_key), (target, key), value in zip(
                current_nodes[::-1], dst_nodes[::-1], values[::-1],
            ):
                if target is current_target:
                    msg: str = "Can not insert at current object"
                    raise ValueError(msg)

                list.insert(target, key, value)  # type: ignore
        elif mode == "set":
            dst = operation.get("to", "@")
            dst_nodes = self.select_nodes(
                current_nodes, dst, allow_slice=True, relative=True,
            )
            for (target, key), value in zip(dst_nodes, values):
                target[key] = value
        elif mode == "update":
            dst = operation.get("to", "@")
            dst_nodes = self.select_nodes(current_nodes, dst, relative=True)
            for (target, key), value in zip(dst_nodes, values):
                dict.update(target[key], value)  # type: ignore
        else:
            msg = "Unknown mode"
            raise ValueError(msg)

    def _apply_patch(
        self, root: list[Any], operations: list[_Operation],
    ) -> None:
        node: _Node = root, 0
        for operation in operations:
            if (op := operation["op"]) == "append":
                path: str = operation.get("path", "$")
                value: Any = operation["value"]
                for target, key in self.select_nodes(node, path):
                    list.append(target[key], deepcopy(value))  # type: ignore
            elif op == "assert":
                path = operation.get("path", "$")
                expr: str = operation["expr"]
                msg: str = operation.get("msg", f"Path {path}: {expr}")
                current_nodes: list[_Node] = self.select_nodes(node, path)
                if current_nodes != self.apply_filter(current_nodes, expr):
                    raise AssertionError(msg)
            elif op == "clear":
                path = operation.get("path", "$")
                for target, key in self.select_nodes(node, path):
                    new_target: Any = target[key]
                    if not isinstance(new_target, (dict, list)):
                        msg = (
                            "Target must be dict or list, not "
                            f"{type(new_target).__name__}"
                        )
                        raise TypeError(msg)

                    new_target.clear()
            elif op == "copy":
                path = operation.get("path", "$")
                src: str = operation["from"]
                current_nodes = self.select_nodes(node, path)
                values: list[Any] = [
                    deepcopy(target[key])
                    for target, key in self.select_nodes(
                        current_nodes, src, allow_slice=True, relative=True,
                    )
                ]
                self.paste_values(current_nodes, values, operation)
            elif op == "del":
                path = operation["path"]

                # Reverse to preserve indices for filters
                for target, key in self.select_nodes(
                    node, path, allow_slice=True,
                )[::-1]:
                    if target is root:
                        msg = "Can not delete root"
                        raise ValueError(msg)

                    del target[key]
            elif op == "extend":
                path = operation.get("path", "$")
                values = operation["values"]
                for target, key in self.select_nodes(node, path):
                    list.extend(target[key], deepcopy(values))  # type: ignore
            elif op == "insert":
                path = operation["path"]
                value = operation["value"]

                # Reverse to preserve indices for filters
                for target, key in self.select_nodes(node, path)[::-1]:
                    if target is root:
                        msg = "Can not insert at root"
                        raise ValueError(msg)

                    list.insert(target, key, deepcopy(value))  # type: ignore
            elif op == "move":
                path = operation.get("path", "$")
                src = operation["from"]
                current_nodes = self.select_nodes(node, path)
                src_nodes: list[_Node] = self.select_nodes(
                    current_nodes, src, allow_slice=True, relative=True,
                )
                values = []

                # Future proofing: Reverse to preserve indices for filters
                for (current_target, _current_key), (target, key) in zip(
                    current_nodes[::-1], src_nodes[::-1],
                ):
                    if target is current_target:
                        msg = "Can not move current object"
                        raise ValueError(msg)

                    values.append(target[key])
                    del target[key]

                # Undo reverse
                self.paste_values(current_nodes, values[::-1], operation)
            elif op == "reverse":
                path = operation.get("path", "$")
                for target, key in self.select_nodes(node, path):
                    list.reverse(target[key])  # type: ignore
            elif op == "set":
                path = operation.get("path", "$")
                value = operation["value"]
                for target, key in self.select_nodes(
                    node, path, allow_slice=True,
                ):
                    target[key] = deepcopy(value)
            elif op == "sort":
                path = operation.get("path", "$")
                reverse: bool = operation.get("reverse", False)
                for target, key in self.select_nodes(node, path):
                    list.sort(target[key], reverse=reverse)  # type: ignore
            elif op == "update":
                path = operation.get("path", "$")
                properties: dict[Any, Any] = operation["properties"]
                for target, key in self.select_nodes(node, path):
                    dict.update(  # type: ignore
                        target[key], deepcopy(properties),
                    )
            else:
                msg = "Unknown operation"
                raise ValueError(msg)

    def apply_patch(
        self, obj: Any, patch: _Operation | list[_Operation],
    ) -> Any:
        """Apply a JSON patch to a Python object.

        :param obj: a Python object
        :param patch: a :doc:`JSON patch </json-patch-spec>`
        :raises AssertionError: if an assertion fails
        :raises IndexError: if an index is out of range
        :raises JSONSyntaxError: if a query is invalid
        :raises KeyError: if a key is not found
        :raises TypeError: if a value has the wrong type
        :raises ValueError: if a value is invalid
        :return: the patched Python object

        Example:
            >>> import jsonyx as json
            >>> manipulator = json.Manipulator()
            >>> manipulator.apply_patch([1, 2, 3], {"op": "del", "path": "$[1]"})
            [1, 3]

        .. tip:: Using a :ref:`filter` instead of an index is more robust.

        """
        root: list[Any] = [obj]
        if isinstance(patch, dict):
            patch = [patch]

        self._apply_patch(root, patch)
        return root[0]

    def paste_values(
        self,
        current_nodes: _Node | list[_Node],
        values: Any | list[Any],
        operation: _Operation,
    ) -> None:
        """Paste value to a node or values to a list of nodes.

        :param current_nodes: a node or a list of nodes
        :param values: a value or a list of values
        :param operation: a JSON :ref:`copy` or :ref:`move` operation
        :raises IndexError: if an index is out of range
        :raises JSONSyntaxError: if a query is invalid
        :raises KeyError: if a key is not found
        :raises TypeError: if a value has the wrong type
        :raises ValueError: if a value is invalid

        Example:
            >>> import jsonyx as json
            >>> manipulator = json.Manipulator()
            >>> obj = [1, 2, 3]
            >>> root = [obj]
            >>> node = root, 0  # pointer to obj
            >>> manipulator.paste_values(node, 4, {"mode": "append"})
            >>> root[0]
            [1, 2, 3, 4]

        """
        if isinstance(current_nodes, tuple):
            current_nodes = [current_nodes]
            values = [values]

        self._paste_values(current_nodes, values, operation)

    def select_nodes(
        self,
        nodes: _Node | list[_Node],
        query: str,
        *,
        allow_slice: bool = False,
        relative: bool = False,
    ) -> list[_Node]:
        """Select nodes from a node or a list of nodes.

        :param nodes: a node or a list of nodes
        :param query: a :ref:`JSON select query <query>`
        :param allow_slice: allow slice
        :param relative: query must start with ``"@"`` instead of ``"$"``
        :raises IndexError: if an index is out of range
        :raises JSONSyntaxError: if the select query is invalid
        :raises KeyError: if a key is not found
        :raises TypeError: if a value has the wrong type
        :return: the selected list of nodes

        Example:
            >>> import jsonyx as json
            >>> manipulator = json.Manipulator()
            >>> obj = [1, 2, 3, 4, 5, 6]
            >>> root = [obj]
            >>> node = root, 0  # pointer to obj
            >>> for target, key in manipulator.select_nodes(node, "$[@ > 3]"):
            ...     target[key] = None
            ...
            >>> root[0]
            [1, 2, 3, None, None, None]

        """
        if isinstance(nodes, tuple):
            nodes = [nodes]

        nodes, end = self._select_nodes(
            nodes,
            query,
            allow_slice=allow_slice,
            relative=relative,
        )

        if end < len(query):
            msg: str = "Expecting end of file"
            raise _errmsg(msg, query, end)

        return nodes

    def apply_filter(
        self, nodes: _Node | list[_Node], query: str,
    ) -> list[_Node]:
        """Apply a JSON filter query to a node or a list of nodes.

        :param nodes: a node or a list of nodes
        :param query: a :ref:`JSON filter query <filter>`
        :raises IndexError: if an index is out of range
        :raises JSONSyntaxError: if the filter query is invalid
        :raises KeyError: if a key is not found
        :raises TypeError: if a value has the wrong type
        :return: the filtered list of nodes

        Example:
            >>> import jsonyx as json
            >>> manipulator = json.Manipulator()
            >>> obj = None
            >>> root = [obj]
            >>> node = root, 0  # pointer to obj
            >>> assert manipulator.apply_filter(node, "@ == null")

        """
        if isinstance(nodes, tuple):
            nodes = [nodes]

        nodes, end = self._apply_filter(nodes, query, 0)
        if end < len(query):
            msg: str = "Expecting end of file"
            raise _errmsg(msg, query, end)

        return nodes

    def load_query_value(self, s: str) -> Any:
        """Deserialize a JSON query value to a Python object.

        :param s: a :ref:`JSON query value <query_value>`
        :raises JSONSyntaxError: if the query value is invalid
        :return: a Python object

        Example:
            >>> import jsonyx as json
            >>> manipulator = json.Manipulator()
            >>> manipulator.load_query_value("'~'foo'")
            "'foo"

        """
        obj, end = self._scan_query_value(s)
        if end < len(s):
            msg: str = "Expecting end of file"
            raise _errmsg(msg, s, end)

        return obj


Manipulator.__module__ = "jsonyx"
