"""JSON dumps tests."""
from __future__ import annotations

__all__: list[str] = []

from collections import UserDict, UserList, UserString
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

import pytest

from jsonyx.allow import NAN_AND_INFINITY, SURROGATES

if TYPE_CHECKING:
    from types import ModuleType

_CIRCULAR_DICT: dict[str, object] = {}
_CIRCULAR_DICT[""] = _CIRCULAR_DICT
_CIRCULAR_LIST: list[object] = []
_CIRCULAR_LIST.append(_CIRCULAR_LIST)


# pylint: disable-next=R0903
class _MyBool:
    def __bool__(self) -> bool:
        return False


# pylint: disable-next=R0903
class _MyInt:
    def __int__(self) -> int:
        return 0


# pylint: disable-next=R0903
class _MyFloat:
    def __float__(self) -> float:
        return 0.0


class _FloatEnum(float, Enum):
    ZERO = 0.0


class _IntEnum(int, Enum):
    ZERO = 0


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


def test_bool_types(json: ModuleType) -> None:
    """Test bool_types."""
    assert json.dumps(_MyBool(), end="", types={"bool": _MyBool}) == "false"


@pytest.mark.parametrize("num", [0, 1])
@pytest.mark.parametrize("num_type", [Decimal, int])
def test_int(
    json: ModuleType, num: int, num_type: type[Decimal | int],
) -> None:
    """Test integer."""
    assert json.dumps(num_type(num), end="") == repr(num)


def test_int_types(json: ModuleType) -> None:
    """Test int_types."""
    assert json.dumps(_MyInt(), end="", types={"int": _MyInt}) == "0"


@pytest.mark.parametrize("num_type", [Decimal, float])
def test_rational_number(
    json: ModuleType, num_type: type[Decimal | float],
) -> None:
    """Test rational number."""
    assert json.dumps(num_type("0.0"), end="") == "0.0"


@pytest.mark.parametrize("num", ["NaN", "Infinity", "-Infinity"])
@pytest.mark.parametrize("num_type", [Decimal, float])
def test_nan_and_infinity(
    json: ModuleType, num: str, num_type: type[Decimal | float],
) -> None:
    """Test NaN and (negative) infinity."""
    assert json.dumps(num_type(num), allow=NAN_AND_INFINITY, end="") == num


@pytest.mark.parametrize("num", ["NaN", "Infinity", "-Infinity"])
@pytest.mark.parametrize("num_type", [Decimal, float])
def test_nan_and_infinity_not_allowed(
    json: ModuleType, num: str, num_type: type[Decimal | float],
) -> None:
    """Test NaN and (negative) infinity when not allowed."""
    with pytest.raises(ValueError, match="is not allowed"):
        json.dumps(num_type(num))


@pytest.mark.parametrize("num", ["NaN2", "-NaN", "-NaN2"])
def test_nan_payload(json: ModuleType, num: str) -> None:
    """Test NaN payload."""
    assert json.dumps(Decimal(num), allow=NAN_AND_INFINITY, end="") == "NaN"


@pytest.mark.parametrize("num", ["NaN2", "-NaN", "-NaN2"])
def test_nan_payload_not_allowed(json: ModuleType, num: str) -> None:
    """Test NaN payload when not allowed."""
    with pytest.raises(ValueError, match="is not allowed"):
        json.dumps(Decimal(num))


def test_signaling_nan(json: ModuleType) -> None:
    """Test signaling NaN."""
    with pytest.raises(ValueError, match="is not JSON serializable"):
        json.dumps(Decimal("sNaN"), allow=NAN_AND_INFINITY)


def test_float_types(json: ModuleType) -> None:
    """Test float_types."""
    assert json.dumps(_MyFloat(), end="", types={"float": _MyFloat}) == "0.0"


@pytest.mark.parametrize(("obj", "expected"), [
    (_IntEnum.ZERO, "0"),
    (_FloatEnum.ZERO, "0.0"),
])
def test_enum(json: ModuleType, obj: float, expected: str) -> None:
    """Test enum."""
    assert json.dumps(obj, end="") == expected


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


@pytest.mark.parametrize("obj", [
    # Empty string
    "",

    # One character
    "$",

    # Multiple characters
    "foo",
])
@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_ascii_string(
    json: ModuleType, obj: str, ensure_ascii: bool,  # noqa: FBT001
) -> None:
    """Test ascii string."""
    assert json.dumps(obj, end="", ensure_ascii=ensure_ascii) == f'"{obj}"'


@pytest.mark.parametrize(("obj", "expected"), [
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
    (r"foo\bar", r"foo\\bar"),
])
@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_control_characters(
    json: ModuleType,
    obj: str,
    ensure_ascii: bool,  # noqa: FBT001
    expected: str,
) -> None:
    """Test control characters."""
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


@pytest.mark.parametrize(("indent", "expected"), [
    # Integer
    (0, ""),
    (1, " "),

    # String
    ("\t", "\t"),
])
def test_list_indent(
    json: ModuleType, indent: int | str, expected: str,
) -> None:
    """Test list indent."""
    s: str = json.dumps([1, 2, 3], end="", indent=indent)
    assert s == f"[\n{expected}1,\n{expected}2,\n{expected}3\n]"


@pytest.mark.parametrize(("obj", "expected"), [
    ([1, 2, 3], "[1, 2, 3]"),
    ([[1, 2, 3]], "[\n [1, 2, 3]\n]"),
])
def test_list_indent_leaves(
    json: ModuleType, obj: list[object], expected: str,
) -> None:
    """Test list indent without indent_leaves."""
    assert json.dumps(obj, end="", indent=1, indent_leaves=False) == expected


def test_list_max_indent_level(json: ModuleType) -> None:
    """Test list indent with max_indent_level."""
    s: str = json.dumps([[1, 2, 3]], end="", indent=1, max_indent_level=1)
    assert s == "[\n [1, 2, 3]\n]"


def test_list_recursion(json: ModuleType) -> None:
    """Test list recursion."""
    obj: list[object] = []
    for _ in range(100_000):
        obj = [obj]

    with pytest.raises(RecursionError):
        json.dumps(obj)


def test_sequence_types(json: ModuleType) -> None:
    """Test sequence_types."""
    obj: UserList[object] = UserList([1, 2, 3])
    assert json.dumps(obj, end="", types={"sequence": UserList}) == "[1, 2, 3]"


@pytest.mark.parametrize(("obj", "expected"), [
    # Empty dict
    ({}, "{}"),

    # One value
    ({"": 0}, '{"": 0}'),

    # Multiple values
    ({"a": 1, "b": 2, "c": 3}, '{"a": 1, "b": 2, "c": 3}'),
])
def test_dict(
    json: ModuleType, obj: dict[str, object], expected: str,
) -> None:
    """Test dict."""
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
    s: str = json.dumps({key: 0}, end="", ensure_ascii=True, quoted_keys=False)
    assert s == f'{{"{expected}": 0}}'


@pytest.mark.parametrize(("key", "expected"), [
    # Empty string
    "",

    # First character
    " ", "!", "$", "0",

    # Remaining characters
    "A ", "A!", "A$",
])
@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_quoted_ascii_keys(
    json: ModuleType, key: str, ensure_ascii: bool,  # noqa: FBT001
) -> None:
    """Test quoted ascii keys."""
    assert json.dumps(
        {key: 0}, end="", ensure_ascii=ensure_ascii, quoted_keys=False,
    ) == f'{{"{key}": 0}}'


@pytest.mark.parametrize(("key", "expected"), [
    # First character
    ("\x00", r"\u0000"),

    # Remaining characters
    ("A\x00", r"A\u0000"),
])
@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_control_characters_key(
    json: ModuleType,
    key: str,
    ensure_ascii: bool,  # noqa: FBT001
    expected: str,
) -> None:
    """Test control characters in key."""
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
    0, Decimal(0), 0.0, Decimal("0.0"), (), True, False, None,

    # No JSON values
    b"", 0j, frozenset(), memoryview(b""), object(),
])  # type: ignore
def test_unserializable_key(json: ModuleType, key: object) -> None:
    """Test unserializable key."""
    with pytest.raises(TypeError, match="Keys must be str, not"):
        json.dumps({key: 0})


def test_sort_keys(json: ModuleType) -> None:
    """Test sort_keys."""
    s: str = json.dumps({"c": 3, "b": 2, "a": 1}, end="", sort_keys=True)
    assert s == '{"a": 1, "b": 2, "c": 3}'


@pytest.mark.parametrize(("indent", "expected"), [
    # Integer
    (0, ""),
    (1, " "),

    # String
    ("\t", "\t"),
])
def test_dict_indent(
    json: ModuleType, indent: int | str, expected: str,
) -> None:
    """Test dict indent."""
    obj: dict[str, object] = {"a": 1, "b": 2, "c": 3}
    s: str = json.dumps(obj, end="", indent=indent)
    assert s == (
        f'{{\n{expected}"a": 1,\n{expected}"b": 2,\n{expected}"c": 3\n}}'
    )


@pytest.mark.parametrize(("obj", "expected"), [
    ({"a": 1, "b": 2, "c": 3}, '{"a": 1, "b": 2, "c": 3}'),
    ({"": {"a": 1, "b": 2, "c": 3}}, '{\n "": {"a": 1, "b": 2, "c": 3}\n}'),
])
def test_dict_indent_leaves(
    json: ModuleType, obj: dict[str, object], expected: str,
) -> None:
    """Test dict indent without indent_leaves."""
    assert json.dumps(obj, end="", indent=1, indent_leaves=False) == expected


def test_dict_max_indent_level(json: ModuleType) -> None:
    """Test dict indent with max_indent_level."""
    obj: dict[str, object] = {"": {"a": 1, "b": 2, "c": 3}}
    s: str = json.dumps(obj, end="", indent=1, max_indent_level=1)
    assert s == '{\n "": {"a": 1, "b": 2, "c": 3}\n}'


def test_dict_recursion(json: ModuleType) -> None:
    """Test dict recursion."""
    obj: dict[str, object] = {}
    for _ in range(100_000):
        obj = {"": obj}

    with pytest.raises(RecursionError):
        json.dumps(obj)


def test_mapping_types(json: ModuleType) -> None:
    """Test mapping_types."""
    obj: UserDict[str, object] = UserDict({"a": 1, "b": 2, "c": 3})
    s: str = json.dumps(obj, end="", types={"mapping": UserDict})
    assert s == '{"a": 1, "b": 2, "c": 3}'


@pytest.mark.parametrize("obj", [
    b"", 0j, bytearray(), frozenset(), memoryview(b""), object(), range(0),
    set(), slice(0),
])  # type: ignore
def test_unserializable_value(json: ModuleType, obj: object) -> None:
    """Test unserializable value."""
    with pytest.raises(TypeError, match="is not JSON serializable"):
        json.dumps(obj)


@pytest.mark.parametrize(("obj", "expected"), [
    (UserString(""), '""'),
    ({UserString(""): 0}, '{"": 0}'),
])
def test_str_types(
    json: ModuleType, obj: UserString | dict[object, object], expected: str,
) -> None:
    """Test str_types."""
    assert json.dumps(obj, end="", types={"str": UserString}) == expected


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
def test_no_commas_indent(
    json: ModuleType,
    obj: dict[str, object] | list[object],
    expected: str,
    trailing_comma: bool,  # noqa: FBT001
) -> None:
    """Test no commas with indent."""
    assert json.dumps(
        obj, commas=False, end="", indent=1, trailing_comma=trailing_comma,
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
def test_trailing_comma_indent(
    json: ModuleType, obj: dict[str, object] | list[object], expected: str,
) -> None:
    """Test trailing_comma with indent."""
    assert json.dumps(obj, end="", indent=1, trailing_comma=True) == expected
