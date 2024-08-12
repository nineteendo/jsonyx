# TODO(Nice Zombies): add error messages
# TODO(Nice Zombies): add type annotations
# TODO(Nice Zombies): export API
# TODO(Nice Zombies): raise JSONSyntaxError
# TODO(Nice Zombies): update command line options
# TODO(Nice Zombies): write documentation
# TODO(Nice Zombies): write tests
import re
from math import isinf
from operator import eq, ge, gt, le, lt, ne
from re import DOTALL, MULTILINE, VERBOSE
from sys import maxsize

from jsonyx import dump

input_json = []
patch_json = [
    {
        "op": "insert",
        "path": "$[0]",
        "value": "value",
    },
]

_FLAGS = VERBOSE | MULTILINE | DOTALL

_match_idx = re.compile(r"end|-?(?:0|[1-9]\d*)", _FLAGS).match
_match_key_chunk = re.compile(r"[^!&.<=>[\]~]*", _FLAGS).match
_match_number = re.compile(
    r"(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?", _FLAGS,
).match
_match_str_chunk = re.compile(r"[^'~]*", _FLAGS).match


def _get_key(s, end=0):
    chunks = []
    append_chunk = chunks.append
    while True:
        if match := _match_key_chunk(s, end):
            end = match.end()
            append_chunk(match.group())

        if s[end:end + 1] != "~":
            return "".join(chunks), end

        end += 1
        try:
            esc = s[end]
        except IndexError:
            raise SyntaxError from None

        if esc not in {"!", "&", ".", "<", "=", ">", "[", "]", "~"}:
            raise SyntaxError

        end += 1
        append_chunk(esc)


def _get_targets(node):
    target, key = node
    if isinstance(target, dict) and not isinstance(key, str):
        raise TypeError

    if isinstance(target, list) and isinstance(key, str):
        raise TypeError

    targets = target[key] if isinstance(key, slice) else [target[key]]
    if not all(isinstance(target, (dict, list)) for target in targets):
        raise TypeError

    return targets


def _get_idx(match):
    if (group := match.group()) == "end":
        idx = maxsize
    else:
        idx = int(group)

    return idx, match.end()


def _get_operator(s, end):
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


def _get_str(s, end):
    chunks = []
    append_chunk = chunks.append
    while True:
        if match := _match_str_chunk(s, end):
            end = match.end()
            append_chunk(match.group())

        try:
            terminator = s[end]
        except IndexError:
            raise SyntaxError from None

        if terminator == "'":
            return "".join(chunks), end + 1

        end += 1
        try:
            esc = s[end]
        except IndexError:
            raise SyntaxError from None

        if esc not in {"'", "~"}:
            raise SyntaxError

        end += 1
        append_chunk(esc)


# TODO(Nice Zombies): allow_nan_and_infinity=False
# TODO(Nice Zombies): use_decimal=True
def _get_value(s, idx):
    try:
        nextchar = s[idx]
    except IndexError:
        raise SyntaxError from None

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
    elif nextchar == "N" and s[idx:idx + 3] == "NaN":
        value, end = float("NaN"), idx + 3
    elif nextchar == "I" and s[idx:idx + 8] == "Infinity":
        value, end = float("Infinity"), idx + 8
    elif nextchar == "-" and s[idx:idx + 9] == "-Infinity":
        value, end = float("-Infinity"), idx + 9
    else:
        raise SyntaxError

    return value, end


def _run_query(nodes, path, end):
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
        key, end = _get_key(path, end)
        if key == "?":
            negate_filter = False
        elif key == "!":
            negate_filter = True
        else:
            raise SyntaxError

        filter_nodes, end = _traverse(nodes, path, end, single=True)
        pairs = [
            (node, target[key])
            for node, (target, key) in zip(nodes, filter_nodes, strict=True)
            if (
                key in target
                if isinstance(target, dict) else
                -len(target) <= key < len(target)
            ) != negate_filter
        ]

        operator, end = _get_operator(path, end)
        if operator is None:
            nodes = [node for node, _target in pairs]
        elif negate_filter:
            raise SyntaxError
        else:
            value, end = _get_value(path, end)
            nodes = [node for node, target in pairs if operator(target, value)]

        if path[end:end + 2] != "&&":
            return nodes, end

        end += 2


def _traverse(nodes, path, end, *, single=False):
    while True:
        if (terminator := path[end:end + 1]) == ".":
            key, end = _get_key(path, end + 1)
            nodes = [
                (target, key)
                for node in nodes
                for target in _get_targets(node)
            ]
        elif terminator == "[":
            if match := _match_idx(path, end + 1):
                idx, end = _get_idx(match)
                if path[end:end + 1] != ":":
                    key = idx
                elif single:
                    raise SyntaxError
                elif match := _match_idx(path, end + 1):
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
                nodes, end = _run_query(nodes, path, end + 1)

            try:
                terminator = path[end]
            except IndexError:
                raise SyntaxError from None

            if terminator != "]":
                raise SyntaxError

            end += 1
        else:
            return nodes, end


def _traverser(nodes, path):
    key, end = _get_key(path)
    if key != "$":
        raise SyntaxError

    nodes, end = _traverse(nodes, path, end)
    if end < len(path):
        raise SyntaxError

    return nodes


def patch(obj, operations):
    root = [obj]
    nodes = [(root, 0)]
    for operation in operations:
        op = operation["op"]
        path = operation["path"]
        if op == "del":
            # Reverse to preserve indices for queries
            for target, key in reversed(_traverser(nodes, path)):
                if target is root:
                    raise ValueError

                if isinstance(target, dict) and not isinstance(key, str):
                    raise TypeError

                if isinstance(target, list) and isinstance(key, str):
                    raise TypeError

                del target[key]
        elif op == "insert":
            value = operation["value"]
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

                target[key] = value
        else:
            raise ValueError

    return root[0]


dump(patch(input_json, patch_json), indent=4)
