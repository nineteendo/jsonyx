# Copyright (C) 2024 Nice Zombies
"""JSON dumps tests."""
from __future__ import annotations

__all__: list[str] = []

from collections import UserDict, UserList
from decimal import Decimal
from typing import TYPE_CHECKING

import pytest

from jsonyx.allow import NAN_AND_INFINITY, SURROGATES
# pylint: disable-next=W0611
from jsonyx.test import get_json  # type: ignore # noqa: F401

if TYPE_CHECKING:
    from collections.abc import Sequence
    from types import ModuleType

_CIRCULAR_DICT: dict[str, object] = {}
_CIRCULAR_DICT[""] = _CIRCULAR_DICT
_CIRCULAR_LIST: list[object] = []
_CIRCULAR_LIST.append(_CIRCULAR_LIST)


class _BadDecimal(Decimal):
    def __str__(self) -> str:
        return f"_BadDecimal({super().__str__()})"


class _BadFloat(float):
    def __repr__(self) -> str:
        return f"_BadFloat({super().__repr__()})"


class _BadInt(int):
    def __repr__(self) -> str:
        return f"_BadInt({super().__repr__()})"


@pytest.mark.parametrize(("obj", "expected"), [
    (True, "true"),
    (False, "false"),
    (None, "null"),
])
def test_singletons(
    json: ModuleType, obj: bool | None, expected: str,  # noqa: FBT001
) -> None:
    """Test singletons."""
    assert json.dumps(obj, end="") == expected


@pytest.mark.parametrize("num", [0, 1])
@pytest.mark.parametrize("num_type", [_BadDecimal, _BadInt, Decimal, int])
def test_int(
    json: ModuleType, num: int, num_type: type[Decimal | int],
) -> None:
    """Test integer."""
    assert json.dumps(num_type(num), end="") == repr(num)


@pytest.mark.parametrize("num_type", [_BadDecimal, _BadFloat, Decimal, float])
def test_rational_number(
    json: ModuleType, num_type: type[Decimal | float],
) -> None:
    """Test rational number."""
    assert json.dumps(num_type("0.0"), end="") == "0.0"


@pytest.mark.parametrize("num", ["NaN", "Infinity", "-Infinity"])
@pytest.mark.parametrize("num_type", [_BadDecimal, _BadFloat, Decimal, float])
def test_nan_and_infinity(
    json: ModuleType, num: str, num_type: type[Decimal | float],
) -> None:
    """Test NaN and (negative) infinity."""
    assert json.dumps(num_type(num), allow=NAN_AND_INFINITY, end="") == num


@pytest.mark.parametrize("num", ["NaN", "Infinity", "-Infinity"])
@pytest.mark.parametrize("num_type", [_BadDecimal, _BadFloat, Decimal, float])
def test_nan_and_infinity_not_allowed(
    json: ModuleType, num: str, num_type: type[Decimal | float],
) -> None:
    """Test NaN and (negative) infinity when not allowed."""
    with pytest.raises(ValueError, match="is not allowed"):
        json.dumps(num_type(num))


@pytest.mark.parametrize("num", ["NaN2", "-NaN", "-NaN2"])
@pytest.mark.parametrize("num_type", [_BadDecimal, Decimal])
def test_nan_payload(
    json: ModuleType, num: str, num_type: type[Decimal],
) -> None:
    """Test NaN payload."""
    assert json.dumps(num_type(num), allow=NAN_AND_INFINITY, end="") == "NaN"


@pytest.mark.parametrize("num", ["NaN2", "-NaN", "-NaN2"])
@pytest.mark.parametrize("num_type", [_BadDecimal, Decimal])
def test_nan_payload_not_allowed(
    json: ModuleType, num: str, num_type: type[Decimal],
) -> None:
    """Test NaN payload when not allowed."""
    with pytest.raises(ValueError, match="is not allowed"):
        json.dumps(num_type(num))


@pytest.mark.parametrize("num_type", [_BadDecimal, Decimal])
def test_signaling_nan(json: ModuleType, num_type: type[Decimal]) -> None:
    """Test signaling NaN."""
    with pytest.raises(ValueError, match="is not JSON serializable"):
        json.dumps(num_type("sNaN"))


@pytest.mark.parametrize("obj", [
    # UTF-8
    "\xa3", "\u0418", "\u0939", "\u20ac", "\ud55c", "\U00010348", "\U001096b3",

    # Surrogates
    "\ud800", "\udf48",  # noqa: PT014
])
def test_string(json: ModuleType, obj: str) -> None:
    """Test string."""
    assert json.dumps(obj, end="") == f'"{obj}"'


@pytest.mark.parametrize(("obj", "expected"), [
    ("\xa3", r"\u00a3"),
    ("\u0418", r"\u0418"),
    ("\u0939", r"\u0939"),
    ("\u20ac", r"\u20ac"),
    ("\ud55c", r"\ud55c"),
    ("\U00010348", r"\ud800\udf48"),
    ("\U001096b3", r"\udbe5\udeb3"),
])
def test_string_ensure_ascii(
    json: ModuleType, obj: str, expected: str,
) -> None:
    """Test string with ensure_ascii."""
    assert json.dumps(obj, end="", ensure_ascii=True) == f'"{expected}"'


@pytest.mark.parametrize(("obj", "expected"), [
    # Empty string
    ("", ""),

    # One character
    ("$", "$"),

    # Control characters
    ("\x00", r"\u0000"),
    ("\x08", r"\b"),
    ("\t", r"\t"),
    ("\n", r"\n"),
    ("\x0c", r"\f"),
    ("\r", r"\r"),
    ('"', r"\""),
    ("\\", r"\\"),

    # Multiple characters
    ("foo", "foo"),
    (r"foo\bar", r"foo\\bar"),
])
@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_ascii_string(
    json: ModuleType,
    obj: str,
    ensure_ascii: bool,  # noqa: FBT001
    expected: str,
) -> None:
    """Test ascii string."""
    s: str = json.dumps(obj, end="", ensure_ascii=ensure_ascii)
    assert s == f'"{expected}"'


@pytest.mark.parametrize(("obj", "expected"), [
    ("\ud800", r"\ud800"),
    ("\udf48", r"\udf48"),
])
def test_surrogate_escapes(json: ModuleType, obj: str, expected: str) -> None:
    """Test surrogate escapes."""
    s: str = json.dumps(obj, allow=SURROGATES, end="", ensure_ascii=True)
    assert s == f'"{expected}"'


@pytest.mark.parametrize("obj", ["\ud800", "\udf48"])  # noqa: PT014
def test_surrogate_escapes_not_allowed(json: ModuleType, obj: str) -> None:
    """Test surrogate escapes when not allowed."""
    with pytest.raises(ValueError, match="Surrogates are not allowed"):
        json.dumps(obj, ensure_ascii=True)


@pytest.mark.parametrize(("obj", "expected"), [
    # Empty list
    ([], "[]"),

    # One value
    ([0], "[0]"),

    # Multiple values
    ([1, 2, 3], "[1, 2, 3]"),

    # Shadow copy
    ([[]] * 3, "[[], [], []]"),
    ([{}] * 3, "[{}, {}, {}]"),
])  # type: ignore
def test_list(json: ModuleType, obj: list[object], expected: str) -> None:
    """Test list."""
    assert json.dumps(obj, end="") == expected


@pytest.mark.parametrize(("obj", "expected"), [
    ([1, 2, 3], "[1, 2, 3]"),
    ([[1, 2, 3]], "[\n [1, 2, 3]\n]"),
])
def test_list_indent(
    json: ModuleType, obj: list[object], expected: str,
) -> None:
    """Test list indent."""
    assert json.dumps(obj, end="", indent=1) == expected


@pytest.mark.parametrize(("indent", "expected"), [
    (0, "[\n1,\n2,\n3\n]"),
    (1, "[\n 1,\n 2,\n 3\n]"),
    ("\t", "[\n\t1,\n\t2,\n\t3\n]"),
])
def test_list_indent_leaves(
    json: ModuleType, indent: int | str, expected: str,
) -> None:
    """Test list indent with indent_leaves."""
    s: str = json.dumps([1, 2, 3], end="", indent=indent, indent_leaves=True)
    assert s == expected


def test_list_recursion(json: ModuleType) -> None:
    """Test list recursion."""
    obj: list[object] = []
    for _ in range(100_000):
        obj = [obj]

    with pytest.raises(RecursionError):
        json.dumps(obj)


@pytest.mark.parametrize(
    "obj", [UserList([1, 2, 3]), range(1, 4), (1, 2, 3)],
)
def test_seq_types(json: ModuleType, obj: Sequence[object]) -> None:
    """Test seq_types."""
    s: str = json.dumps(obj, end="", seq_types=(UserList, range))
    assert s == "[1, 2, 3]"


@pytest.mark.parametrize(("obj", "expected"), [
    # Empty dict
    ({}, "{}"),

    # One value
    ({"": 0}, '{"": 0}'),

    # Multiple values
    ({"a": 1, "b": 2, "c": 3}, '{"a": 1, "b": 2, "c": 3}'),
])
def test_mapping(
    json: ModuleType, obj: dict[str, object], expected: str,
) -> None:
    """Test mapping."""
    assert json.dumps(obj, end="") == expected


@pytest.mark.parametrize("key", [
    # First character
    "\xb2", "\u0300", "\u037a", "\u0488",

    # Remaining characters
    "A\xb2", "A\u037a", "A\u0488",
])
def test_quoted_keys(json: ModuleType, key: str) -> None:
    """Test quoted keys."""
    assert json.dumps({key: 0}, end="", quoted_keys=False) == f'{{"{key}": 0}}'


@pytest.mark.parametrize(("key", "expected"), [
    # First character
    ("\xb2", r"\u00b2"),
    ("\u0300", r"\u0300"),
    ("\u037a", r"\u037a"),
    ("\u0488", r"\u0488"),
    ("\u16ee", r"\u16ee"),
    ("\u1885", r"\u1885"),
    ("\u2118", r"\u2118"),

    # Remaining characters
    ("A\xb2", r"A\u00b2"),
    ("A\u0300", r"A\u0300"),
    ("A\u037a", r"A\u037a"),
    ("A\u0488", r"A\u0488"),
    ("A\u2118", r"A\u2118"),
])
def test_quoted_keys_ensure_ascii(
    json: ModuleType, key: str, expected: str,
) -> None:
    """Test quoted keys with ensure_ascii."""
    assert json.dumps(
        {key: 0}, end="", ensure_ascii=True, quoted_keys=False,
    ) == f'{{"{expected}": 0}}'


@pytest.mark.parametrize(("key", "expected"), [
    # Empty string
    ("", ""),

    # First character
    ("\x00", r"\u0000"),
    (" ", " "),
    ("!", "!"),
    ("$", "$"),
    ("0", "0"),

    # Remaining characters
    ("A\x00", r"A\u0000"),
    ("A ", "A "),
    ("A!", "A!"),
    ("A$", "A$"),
])
@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_quoted_ascii_keys(
    json: ModuleType,
    key: str,
    ensure_ascii: bool,  # noqa: FBT001
    expected: str,
) -> None:
    """Test quoted ascii keys."""
    assert json.dumps(
        {key: 0}, end="", ensure_ascii=ensure_ascii, quoted_keys=False,
    ) == f'{{"{expected}": 0}}'


@pytest.mark.parametrize("key", [
    # First character
    "\u16ee", "\u1885", "\u2118",

    # Remaining characters
    "A\u0300", "A\u2118",
])
def test_unquoted_keys(json: ModuleType, key: str) -> None:
    """Test unquoted keys."""
    assert json.dumps({key: 0}, end="", quoted_keys=False) == f"{{{key}: 0}}"


@pytest.mark.parametrize("key", [
    # First character
    "A", "_",

    # Remaining characters
    "A0", "AA", "A_",
])
@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_unquoted_ascii_keys(
    json: ModuleType, key: str, ensure_ascii: bool,  # noqa: FBT001
) -> None:
    """Test unquoted ascii keys."""
    assert json.dumps(
        {key: 0}, end="", ensure_ascii=ensure_ascii, quoted_keys=False,
    ) == f"{{{key}: 0}}"


@pytest.mark.parametrize("key", [
    # JSON values
    0, Decimal(0), 0.0, Decimal("0.0"), True, False, None,

    # No JSON values
    b"", 0j, (), frozenset(), memoryview(b""), object(),
])  # type: ignore
def test_unserializable_key(json: ModuleType, key: object) -> None:
    """Test unserializable key."""
    with pytest.raises(TypeError, match="Keys must be str, not"):
        json.dumps({key: 0})


def test_sort_keys(json: ModuleType) -> None:
    """Test sort_keys."""
    s: str = json.dumps({"c": 3, "b": 2, "a": 1}, end="", sort_keys=True)
    assert s == '{"a": 1, "b": 2, "c": 3}'


@pytest.mark.parametrize(("obj", "expected"), [
    ({"a": 1, "b": 2, "c": 3}, '{"a": 1, "b": 2, "c": 3}'),
    ({"": {"a": 1, "b": 2, "c": 3}}, '{\n "": {"a": 1, "b": 2, "c": 3}\n}'),
])
def test_dict_indent(
    json: ModuleType, obj: dict[str, object], expected: str,
) -> None:
    """Test dict indent."""
    assert json.dumps(obj, end="", indent=1) == expected


@pytest.mark.parametrize(("indent", "expected"), [
    (0, '{\n"a": 1,\n"b": 2,\n"c": 3\n}'),
    (1, '{\n "a": 1,\n "b": 2,\n "c": 3\n}'),
    ("\t", '{\n\t"a": 1,\n\t"b": 2,\n\t"c": 3\n}'),
])
def test_dict_indent_leaves(
    json: ModuleType, indent: int | str, expected: str,
) -> None:
    """Test dict indent with indent_leaves."""
    obj: dict[str, object] = {"a": 1, "b": 2, "c": 3}
    s: str = json.dumps(obj, end="", indent=indent, indent_leaves=True)
    assert s == expected


def test_dict_recursion(json: ModuleType) -> None:
    """Test dict recursion."""
    obj: dict[str, object] = {}
    for _ in range(100_000):
        obj = {"": obj}

    with pytest.raises(RecursionError):
        json.dumps(obj)


@pytest.mark.parametrize("obj", [
    b"", 0j, bytearray(), frozenset(), memoryview(b""), object(), range(0),
    set(), slice(0),
])  # type: ignore
def test_unserializable_value(json: ModuleType, obj: object) -> None:
    """Test unserializable value."""
    with pytest.raises(TypeError, match="is not JSON serializable"):
        json.dumps(obj)


def test_mapping_types(json: ModuleType) -> None:
    """Test mapping_types."""
    assert json.dumps(
        UserDict({"a": 1, "b": 2, "c": 3}), end="", mapping_types=UserDict,
    ) == '{"a": 1, "b": 2, "c": 3}'


@pytest.mark.parametrize("obj", [_CIRCULAR_DICT, _CIRCULAR_LIST])
def test_circular_reference(
    json: ModuleType, obj: dict[str, object] | list[object],
) -> None:
    """Test circular reference."""
    with pytest.raises(ValueError, match="Unexpected circular reference"):
        json.dumps(obj)


@pytest.mark.parametrize(("obj", "expected"), [
    ([1, 2, 3], "[1, 2, 3]"),
    ({"a": 1, "b": 2, "c": 3}, '{"a": 1, "b": 2, "c": 3}'),
])
def test_no_commas(
    json: ModuleType, obj: dict[str, object] | list[object], expected: str,
) -> None:
    """Test no commas."""
    assert json.dumps(obj, commas=False, end="") == expected


@pytest.mark.parametrize(("obj", "expected"), [
    ([1, 2, 3], "[\n 1\n 2\n 3\n]"),
    ({"a": 1, "b": 2, "c": 3}, '{\n "a": 1\n "b": 2\n "c": 3\n}'),
])
@pytest.mark.parametrize("trailing_comma", [True, False])
def test_no_commas_indent_leaves(
    json: ModuleType,
    obj: dict[str, object] | list[object],
    expected: str,
    trailing_comma: bool,  # noqa: FBT001
) -> None:
    """Test no commas with indent and indent_leaves."""
    assert json.dumps(
        obj,
        commas=False,
        end="",
        indent=1,
        indent_leaves=True,
        trailing_comma=trailing_comma,
    ) == expected


def test_default_end(json: ModuleType) -> None:
    """Test default end."""
    assert json.dumps(0) == "0\n"


def test_custom_end(json: ModuleType) -> None:
    """Test custom end."""
    assert json.dumps(0, end="") == "0"


@pytest.mark.parametrize(("obj", "expected"), [
    ([1, 2, 3], "[1,2,3]"),
    ({"a": 1, "b": 2, "c": 3}, '{"a":1,"b":2,"c":3}'),
])
def test_separators(
    json: ModuleType, obj: dict[str, object] | list[object], expected: str,
) -> None:
    """Test separators."""
    assert json.dumps(obj, end="", separators=(",", ":")) == expected


@pytest.mark.parametrize(("obj", "expected"), [
    ([1, 2, 3], "[1, 2, 3]"),
    ({"a": 1, "b": 2, "c": 3}, '{"a": 1, "b": 2, "c": 3}'),
])
def test_trailing_comma(
    json: ModuleType, obj: dict[str, object] | list[object], expected: str,
) -> None:
    """Test trailing_comma."""
    assert json.dumps(obj, end="", trailing_comma=True) == expected


@pytest.mark.parametrize(("obj", "expected"), [
    ([1, 2, 3], "[\n 1,\n 2,\n 3,\n]"),
    ({"a": 1, "b": 2, "c": 3}, '{\n "a": 1,\n "b": 2,\n "c": 3,\n}'),
])
def test_trailing_comma_indent_leaves(
    json: ModuleType, obj: dict[str, object] | list[object], expected: str,
) -> None:
    """Test trailing_comma with indent and indent_leaves."""
    assert json.dumps(
        obj, end="", indent=1, indent_leaves=True, trailing_comma=True,
    ) == expected
