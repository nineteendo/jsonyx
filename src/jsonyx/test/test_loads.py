"""JSON loads tests."""
from __future__ import annotations

__all__: list[str] = []

from collections import UserString
from dataclasses import dataclass
from decimal import MAX_EMAX, Decimal
from math import isnan
from typing import TYPE_CHECKING, Any

import pytest

from jsonyx.allow import (
    COMMENTS, MISSING_COMMAS, NAN_AND_INFINITY, SURROGATES, TRAILING_COMMA,
    UNQUOTED_KEYS,
)
from jsonyx.test import check_syntax_err

if TYPE_CHECKING:
    from types import ModuleType


# pylint: disable-next=R0903
@dataclass
class _MyBool:
    value: Any

    def __bool__(self) -> bool:
        return bool(self.value)


@pytest.mark.parametrize(
    "string", ["\ud800", "\ud800$", "\udf48"],  # noqa: PT014
)
def test_surrogate(json: ModuleType, string: str) -> None:
    """Test surrogate."""
    b: bytes = f'"{string}"'.encode(errors="surrogatepass")
    assert json.loads(b, allow=SURROGATES) == string


@pytest.mark.parametrize(
    "string", ["\ud800", "\ud800$", "\udf48"],  # noqa: PT014
)
def test_surrogate_not_allowed(json: ModuleType, string: str) -> None:
    """Test surrogate when not allowed."""
    b: bytes = f'"{string}"'.encode(errors="surrogatepass")
    with pytest.raises(json.TruncatedSyntaxError):
        json.loads(b)


def test_utf8_bom(json: ModuleType) -> None:
    """Test UTF-8 BOM."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads("\ufeff0")

    check_syntax_err(exc_info, "Unexpected UTF-8 BOM", 1, 2)


def test_null(json: ModuleType) -> None:
    """Test null."""
    assert json.loads("null") is None


@pytest.mark.parametrize(("s", "expected"), [
    ("true", True),
    ("false", False),
])
@pytest.mark.parametrize("bool_type", [_MyBool, bool])
def test_bool(
    json: ModuleType, s: str, expected: bool, bool_type: type,
) -> None:
    """Test bool."""
    obj: object = json.loads(s, hooks={"bool": bool_type})
    assert isinstance(obj, bool_type)
    assert obj == bool_type(expected)


@pytest.mark.parametrize("s", ["NaN", "Infinity", "-Infinity"])
@pytest.mark.parametrize("float_type", [Decimal, float])
def test_nan_and_infinity(json: ModuleType, s: str, float_type: type) -> None:
    """Test NaN and infinity."""
    obj: object = json.loads(
        s, allow=NAN_AND_INFINITY, hooks={"float": float_type},
    )
    expected: Any = float_type(s)
    expected = float_type(expected)
    assert isinstance(obj, float_type)
    if isnan(expected):
        assert isnan(obj)  # type: ignore[arg-type]
    else:
        assert obj == expected


@pytest.mark.parametrize("s", ["NaN", "Infinity", "-Infinity"])
def test_nan_and_infinity_not_allowed(json: ModuleType, s: str) -> None:
    """Test NaN and infinity when not allowed."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s)

    check_syntax_err(exc_info, f"{s} is not allowed", 1, len(s) + 1)


@pytest.mark.parametrize("s", [
    # Sign
    "-1",

    # Integer
    "0", "1", "10", "11",
])
@pytest.mark.parametrize("int_type", [Decimal, int])
def test_int(json: ModuleType, s: str, int_type: type) -> None:
    """Test integer."""
    obj: object = json.loads(s, hooks={"int": int_type})
    assert isinstance(obj, int_type)
    assert obj == int_type(s)


def test_too_big_int(json: ModuleType, big_num: str) -> None:
    """Test too big integer."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(big_num)

    check_syntax_err(exc_info, "Invalid number", 1, len(big_num) + 1)


def test_int_type(json: ModuleType) -> None:
    """Test int_type."""
    obj: object = json.loads("0", hooks={"int": Decimal})
    assert isinstance(obj, Decimal)
    assert obj == Decimal(0)


@pytest.mark.parametrize("s", [
    # Sign
    "-1.0",

    # Fraction
    "1.0", "1.01", "1.1", "1.11",

    # Fraction with trailing zeros
    "1.00", "1.10",

    # Exponent e
    "1E1",

    # Exponent sign
    "1e-1", "1e+1",

    # Exponent power
    "1e0", "1e1", "1e10", "1e11",

    # Exponent power with leading zeros
    "1e00", "1e01",

    # Parts
    "1.1e1", "-1e1", "-1.1", "-1.1e1",

    # Big exponent
    "1e400", "-1e400",
])
@pytest.mark.parametrize("float_type", [Decimal, float])
def test_rational_number(json: ModuleType, s: str, float_type: type) -> None:
    """Test rational number."""
    obj: object = json.loads(s, hooks={"float": float_type})
    assert isinstance(obj, float_type)
    assert obj == float_type(s)


@pytest.mark.parametrize("s", [f"1e{MAX_EMAX + 1}", f"-1e{MAX_EMAX + 1}"])
def test_too_big_number(json: ModuleType, s: str) -> None:
    """Test too big JSON number."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s, hooks={"float": Decimal})

    check_syntax_err(exc_info, "Invalid number", 1, len(s) + 1)


@pytest.mark.parametrize("s", ["1\uff10", "0.\uff10", "0e\uff10"])
def test_invalid_number(json: ModuleType, s: str) -> None:
    """Test invalid number."""
    with pytest.raises(json.JSONSyntaxError):
        json.loads(s)


@pytest.mark.parametrize("s", [
    # Empty string
    "",

    # UTF-8
    "$", "\xa3", "\u0418", "\u0939", "\u20ac", "\ud55c", "\U00010348",
    "\U001096b3",

    # Surrogates
    "\ud800", "\ud800$", "\udf48",  # noqa: PT014

    # Multiple characters
    "foo",
])
def test_string(json: ModuleType, s: str) -> None:
    """Test JSON string."""
    assert json.loads(f'"{s}"') == s


@pytest.mark.parametrize(("s", "expected"), [
    # Backslash escapes
    (r"\"", '"'),
    (r"\\", "\\"),
    (r"\/", "/"),
    (r"\b", "\b"),
    (r"\f", "\f"),
    (r"\n", "\n"),
    (r"\r", "\r"),
    (r"\t", "\t"),

    # Unicode escape sequences
    (r"\u0024", "$"),
    (r"\u00a3", "\xa3"),
    (r"\u0418", "\u0418"),
    (r"\u0939", "\u0939"),
    (r"\u20ac", "\u20ac"),
    (r"\ud55c", "\ud55c"),
    (r"\ud800\udf48", "\U00010348"),
    (r"\udbe5\udeb3", "\U001096b3"),

    # Multiple characters
    (r"foo\\bar", r"foo\bar"),
])
def test_string_escapes(json: ModuleType, s: str, expected: str) -> None:
    """Test string escapes."""
    assert json.loads(f'"{s}"') == expected


@pytest.mark.parametrize(("s", "expected"), [
    (r"\ud800", "\ud800"),
    (r"\ud800\u0024", "\ud800$"),
    (r"\udf48", "\udf48"),
])
def test_surrogate_escape(json: ModuleType, s: str, expected: str) -> None:
    """Test surrogate escape."""
    assert json.loads(f'"{s}"', allow=SURROGATES) == expected


@pytest.mark.parametrize(("s", "msg", "colno", "end_colno"), [
    ('"foo', "Unterminated string", 1, 5),
    ('"foo\n', "Unterminated string", 1, 5),
    ('"foo\r', "Unterminated string", 1, 5),
    ('"foo\r\n', "Unterminated string", 1, 5),
    ('"\b"', "Unescaped control character", 2, 3),
    ('"\\', "Expecting escaped character", 3, -1),
    ('"\\\n', "Expecting escaped character", 3, -1),
    ('"\\\r', "Expecting escaped character", 3, -1),
    ('"\\\r\n', "Expecting escaped character", 3, -1),
    (r'"\a"', "Invalid backslash escape", 2, 4),
    (r'"\ud800"', "Surrogates are not allowed", 2, 8),
    (r'"\ud800\u0024"', "Surrogates are not allowed", 2, 8),
    (r'"\udf48"', "Surrogates are not allowed", 2, 8),
])
def test_invalid_string(
    json: ModuleType, s: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid JSON string."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s)

    check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize(("s", "colno", "end_colno"), [
    # Single
    (r'"\u"', 4, 5),
    (r'"\u0xff"', 4, 8),  # Hex prefix
    # pylint: disable-next=C0209
    (r'"\u{}"'.format("\uff10" * 4), 4, 8),  # Unicode digits
    (r'"\u 000"', 4, 8),  # Surrounded by whitespace
    (r'"\u-000"', 4, 8),  # Negative number
    (r'"\u+000"', 4, 8),  # Positive number
    (r'"\u0_00"', 4, 8),  # Underscore between digits
    (r'"\u????"', 4, 8),

    # After high surrogate
    (r'"\ud800\u"', 10, 11),
    (r'"\ud800\u0xff"', 10, 14),  # Hex prefix
    # pylint: disable-next=C0209
    (r'"\ud800\u{}"'.format("\uff10" * 4), 10, 14),  # Unicode digits
    (r'"\ud800\u 000"', 10, 14),  # Surrounded by whitespace
    (r'"\ud800\u-000"', 10, 14),  # Negative number
    (r'"\ud800\u+000"', 10, 14),  # Positive number
    (r'"\ud800\u0_00"', 10, 14),  # Underscore between digits
    (r'"\ud800\u????"', 10, 14),
])
def test_invalid_unicode_escape(
    json: ModuleType, s: str, colno: int, end_colno: int,
) -> None:
    """Test invalid unicode escape."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s)

    check_syntax_err(exc_info, "Expecting 4 hex digits", colno, end_colno)


def test_str_type(json: ModuleType) -> None:
    """Test str_type."""
    obj: object = json.loads('""', hooks={"str": UserString})
    assert isinstance(obj, UserString)
    assert not obj


@pytest.mark.parametrize(("s", "expected"), [
    # Empty array
    ("[]", []),

    # One value
    ("[0]", [0]),

    # Multiple values
    ("[1, 2, 3]", [1, 2, 3]),
])
@pytest.mark.parametrize("array_type", [list, tuple])
def test_array(
    json: ModuleType, s: str, expected: list[object], array_type: type,
) -> None:
    """Test JSON array."""
    types: dict[str, type] = {"array": array_type}
    assert json.loads(s, hooks=types) == array_type(expected)


@pytest.mark.parametrize(("s", "expected"), [
    # No whitespace
    ("[]", []),
    ("[1,2,3]", [1, 2, 3]),

    # In empty array
    ("[ ]", []),

    # Before first element
    ("[ 1,2,3]", [1, 2, 3]),

    # Before commas
    ("[1 ,2 ,3]", [1, 2, 3]),

    # After commas
    ("[1, 2, 3]", [1, 2, 3]),

    # After last element
    ("[1,2,3 ]", [1, 2, 3]),
])
def test_array_whitespace(
    json: ModuleType, s: str, expected: list[object],
) -> None:
    """Test whitespace in JSON array."""
    assert json.loads(s) == expected


@pytest.mark.parametrize(("s", "expected"), [
    # In empty array
    ("[/**/]", []),

    # Before first element
    ("[/**/1,2,3]", [1, 2, 3]),

    # Before commas
    ("[1/**/,2/**/,3]", [1, 2, 3]),

    # After commas
    ("[1,/**/2,/**/3]", [1, 2, 3]),

    # After last element
    ("[1,2,3/**/]", [1, 2, 3]),
])
def test_array_comments(
    json: ModuleType, s: str, expected: list[object],
) -> None:
    """Test comments in JSON array."""
    assert json.loads(s, allow=COMMENTS) == expected


@pytest.mark.parametrize(("s", "msg", "colno", "end_colno"), [
    ("[", "Unterminated array", 1, 2),
    ("[0", "Unterminated array", 1, 3),
    ("[1-2-3]", "Expecting comma", 3, -1),
    ("[1 2 3]", "Missing commas are not allowed", 3, -1),
    ("[0,", "Unterminated array", 1, 4),
    ("[0,]", "Trailing comma is not allowed", 3, 4),
])
def test_invalid_array(
    json: ModuleType, s: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid JSON array."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s)

    check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize(("s", "expected"), [
    # Empty object
    ("{}", []),

    # One value
    ('{"": 0}', [("", 0)]),

    # Multiple values
    ('{"a": 1, "b": 2, "c": 3}', [("a", 1), ("b", 2), ("c", 3)]),

    # Duplicate keys
    ('{"a": 1, "a": 2, "a": 3}', [("a", 1), ("a", 2), ("a", 3)]),
])
@pytest.mark.parametrize("object_type", [dict, list])
def test_object(
    json: ModuleType, s: str, expected: list[tuple[str, object]],
    object_type: type,
) -> None:
    """Test JSON object."""
    types: dict[str, type] = {"object": object_type}
    assert json.loads(s, hooks=types) == object_type(expected)


@pytest.mark.parametrize(("s", "expected"), [
    # No whitespace
    ("{}", {}),
    ('{"a":1,"b":2,"c":3}', {"a": 1, "b": 2, "c": 3}),

    # In empty object
    ("{ }", {}),

    # Before first element
    ('{ "a":1,"b":2,"c":3}', {"a": 1, "b": 2, "c": 3}),

    # Before colon
    ('{"a" :1,"b" :2,"c" :3}', {"a": 1, "b": 2, "c": 3}),

    # After colon
    ('{"a": 1,"b": 2,"c": 3}', {"a": 1, "b": 2, "c": 3}),

    # Before comma
    ('{"a":1 ,"b":2 ,"c":3}', {"a": 1, "b": 2, "c": 3}),

    # After comma
    ('{"a":1, "b":2, "c":3}', {"a": 1, "b": 2, "c": 3}),

    # After last element
    ('{"a":1,"b":2,"c":3 }', {"a": 1, "b": 2, "c": 3}),
])
def test_object_whitespace(
    json: ModuleType, s: str, expected: dict[str, object],
) -> None:
    """Test whitespace in JSON object."""
    assert json.loads(s) == expected


@pytest.mark.parametrize(("s", "expected"), [
    # In empty object
    ("{/**/}", {}),

    # Before first element
    ('{/**/"a":1,"b":2,"c":3}', {"a": 1, "b": 2, "c": 3}),

    # Before colon
    ('{"a"/**/:1,"b"/**/:2,"c"/**/:3}', {"a": 1, "b": 2, "c": 3}),

    # After colon
    ('{"a":/**/1,"b":/**/2,"c":/**/3}', {"a": 1, "b": 2, "c": 3}),

    # Before comma
    ('{"a":1/**/,"b":2/**/,"c":3}', {"a": 1, "b": 2, "c": 3}),

    # After comma
    ('{"a":1,/**/"b":2,/**/"c":3}', {"a": 1, "b": 2, "c": 3}),

    # After last element
    ('{"a":1,"b":2,"c":3/**/}', {"a": 1, "b": 2, "c": 3}),
])
def test_object_comments(
    json: ModuleType, s: str, expected: dict[str, object],
) -> None:
    """Test comments in JSON object."""
    assert json.loads(s, allow=COMMENTS) == expected


@pytest.mark.parametrize("key", [
    # First character
    "A", "_", "\u16ee", "\u1885", "\u2118",

    # Remaining characters
    "A0", "AA", "A_", "A\u0300", "A\u2118",
])
def test_unquoted_key(json: ModuleType, key: str) -> None:
    """Test unquoted key."""
    assert json.loads(f"{{{key}: 0}}", allow=UNQUOTED_KEYS) == {key: 0}


@pytest.mark.parametrize("key", [
    # First character
    "A", "_", "\u16ee", "\u1885", "\u2118",

    # Remaining characters
    "A0", "AA", "A_", "A\u0300", "A\u2118",
])
def test_unquoted_key_not_allowed(json: ModuleType, key: str) -> None:
    """Test unquoted key when not allowed."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(f"{{{key}: 0}}")

    msg: str = "Unquoted keys are not allowed"
    check_syntax_err(exc_info, msg, 2, 2 + len(key))


@pytest.mark.parametrize("key", [
    # First character
    "\x00", "!", "$", "0", "\xb2", "\u0300", "\u037a", "\u0488",

    # Remaining characters
    "A\x00", "A!", "A$", "A\xb2", "A\u037a", "A\u0488",
])
def test_invalid_unquoted_key(json: ModuleType, key: str) -> None:
    """Test invalid unquoted key."""
    with pytest.raises(json.JSONSyntaxError):
        json.loads(f"{{{key}: 0}}", allow=UNQUOTED_KEYS)


@pytest.mark.parametrize(("s", "msg", "colno", "end_colno"), [
    ("{", "Unterminated object", 1, 2),
    ('{""}', "Expecting colon", 4, -1),
    ('{"": 0', "Unterminated object", 1, 7),
    ('{"a": 1"b": 2"c": 3}', "Expecting comma", 8, -1),
    ('{"a": 1 "b": 2 "c": 3}', "Missing commas are not allowed", 8, -1),
    ('{"": 0,', "Unterminated object", 1, 8),
    ('{"": 0,}', "Trailing comma is not allowed", 7, 8),
])
def test_invalid_object(
    json: ModuleType, s: str, msg: str, colno: int, end_colno: int,
) -> None:
    """Test invalid JSON object."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s)

    check_syntax_err(exc_info, msg, colno, end_colno)


def test_repeated_keys(json: ModuleType) -> None:
    """Test repeated keys."""
    assert id(b"abc".decode()) != id("abc")
    s: str = '[{"abc": 1}, {"abc": 2}, {"abc": 3}]'
    dcts: list[dict[str, int]] = json.loads(s)
    assert len({id(key) for dct in dcts for key in dct}) == 3


def test_repeated_keys_cache_keys(json: ModuleType) -> None:
    """Test repeated keys with cache_keys."""
    assert id(b"abc".decode()) != id("abc")
    s: str = '[{"abc": 1}, {"abc": 2}, {"abc": 3}]'
    dcts: list[dict[str, int]] = json.loads(s, cache_keys=True)
    assert len({id(key) for dct in dcts for key in dct}) == 1


@pytest.mark.parametrize("s", ["", "-", "foo"])
def test_expecting_value(json: ModuleType, s: str) -> None:
    """Test expecting JSON value."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s)

    check_syntax_err(exc_info, "Expecting value")


@pytest.mark.parametrize(("s", "expected"), [
    ("[1 2 3]", [1, 2, 3]),
    ('{"a": 1 "b": 2 "c": 3}', {"a": 1, "b": 2, "c": 3}),
])
def test_missing_comma(
    json: ModuleType, s: str, expected: dict[str, object] | list[object],
) -> None:
    """Test missing comma."""
    assert json.loads(s, allow=MISSING_COMMAS) == expected


@pytest.mark.parametrize(("s", "expected"), [
    ("[0,]", [0]),
    ('{"": 0,}', {"": 0}),
])
def test_trailing_comma(
    json: ModuleType, s: str, expected: dict[str, object] | list[object],
) -> None:
    """Test trailing comma."""
    assert json.loads(s, allow=TRAILING_COMMA) == expected


@pytest.mark.parametrize(("start", "msg"), [
    ("[", "Array is too deeply nested"),
    ('{"":', "Object is too deeply nested"),
])
def test_recursion(json: ModuleType, start: str, msg: str) -> None:
    """Test recursion."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(start * 100_000)

    assert exc_info.value.msg == msg


@pytest.mark.parametrize("s", [
    # No whitespace
    "0",

    # Before value
    " 0",

    # After value
    "0 ",
])
def test_value_whitespace(json: ModuleType, s: str) -> None:
    """Test whitespace around JSON value."""
    assert json.loads(s) == 0


@pytest.mark.parametrize("s", [
    # Before value
    "/**/0",

    # After value
    "0/**/",
])
def test_value_comments(json: ModuleType, s: str) -> None:
    """Test comments around JSON value."""
    assert json.loads(s, allow=COMMENTS) == 0


@pytest.mark.parametrize("s", [
    # One character
    "0 ", "0\t", "0\n", "0\r",

    # Multiple characters
    "0   ",
])
def test_whitespace(json: ModuleType, s: str) -> None:
    """Test whitespace."""
    assert json.loads(s) == 0


@pytest.mark.parametrize("s", [
    # One comment
    "//\n0", "//\r0", "//\r\n0",
    "//line comment\n0", "//line comment\r0", "//line comment\r\n0",
    "/*block comment*/0",

    # Multiple comments
    "//comment 1\n//comment 2\n//comment 3\n0",
    "//comment 1\r//comment 2\r//comment 3\n0",
    "//comment 1\r\n//comment 2\r\n//comment 3\r\n0",
    "/*comment 1*//*comment 2*//*comment 3*/0",

    # Whitespace
    " //comment 1\n //comment 2\n //comment 3\n 0",
    " //comment 1\r //comment 2\r //comment 3\r 0",
    " //comment 1\r\n //comment 2\r\n //comment 3\r\n 0",
    " /*comment 1*/ /*comment 2*/ /*comment 3*/ 0",
])
def test_comments(json: ModuleType, s: str) -> None:
    """Test comments."""
    assert json.loads(s, allow=COMMENTS) == 0


def test_invalid_comment(json: ModuleType) -> None:
    """Test invalid comment."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads("/*unterminated comment", allow=COMMENTS)

    check_syntax_err(exc_info, "Unterminated comment", 1, 23)


@pytest.mark.parametrize(("s", "end_colno"), [
    ("//line comment\n0", 15),
    ("//line comment\r0", 15),
    ("//line comment\r\n0", 15),
    ("/*block comment*/0", 18),
    ("/*unterminated comment", 23),
])
def test_comments_not_allowed(
    json: ModuleType, s: str, end_colno: int,
) -> None:
    """Test comments when not allowed."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads(s)

    check_syntax_err(exc_info, "Comments are not allowed", 1, end_colno)


def test_end_of_file(json: ModuleType) -> None:
    """Test end of file."""
    with pytest.raises(json.JSONSyntaxError) as exc_info:
        json.loads("1 2 3")

    check_syntax_err(exc_info, "Expecting end of file", 3)
