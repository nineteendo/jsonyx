"""JSON load_query_value tests."""
from __future__ import annotations

__all__: list[str] = []

from decimal import MAX_EMAX, Decimal

import pytest

from jsonyx import JSONSyntaxError, load_query_value
from jsonyx.allow import NAN_AND_INFINITY
from jsonyx.test import check_syntax_err


@pytest.mark.parametrize(("s", "expected"), [
    ("true", True),
    ("false", False),
    ("null", None),
])
def test_literal_names(s: str, expected: bool | None) -> None:
    """Test literal names."""
    assert load_query_value(s) is expected


@pytest.mark.parametrize("s", ["Infinity", "-Infinity"])
@pytest.mark.parametrize("use_decimal", [True, False])
def test_infinity(s: str, use_decimal: bool) -> None:
    """Test infinity."""
    obj: object = load_query_value(
        s, allow=NAN_AND_INFINITY, use_decimal=use_decimal,
    )
    expected_type: type[Decimal | float] = Decimal if use_decimal else float
    assert isinstance(obj, expected_type)
    assert obj == expected_type(s)


@pytest.mark.parametrize("s", ["Infinity", "-Infinity"])
@pytest.mark.parametrize("use_decimal", [True, False])
def test_infinity_not_allowed(s: str, use_decimal: bool) -> None:
    """Test infinity when not allowed."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(s, use_decimal=use_decimal)

    check_syntax_err(exc_info, f"{s} is not allowed", 1, len(s) + 1)


@pytest.mark.parametrize("s", [
    # Sign
    "-1",

    # Integer
    "0", "1", "10", "11",
])
def test_int(s: str) -> None:
    """Test integer."""
    obj: object = load_query_value(s)
    assert isinstance(obj, int)
    assert obj == int(s)


def test_too_big_int(big_num: str) -> None:
    """Test too big integer."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(big_num)

    check_syntax_err(exc_info, "Invalid number", 1, len(big_num) + 1)


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
@pytest.mark.parametrize("use_decimal", [True, False])
def test_rational_number(s: str, use_decimal: bool) -> None:
    """Test rational number."""
    obj: object = load_query_value(s, use_decimal=use_decimal)
    expected_type: type[Decimal | float] = Decimal if use_decimal else float
    assert isinstance(obj, expected_type)
    assert obj == expected_type(s)


@pytest.mark.parametrize("s", [f"1e{MAX_EMAX + 1}", f"-1e{MAX_EMAX + 1}"])
def test_too_big_number(s: str) -> None:
    """Test too big JSON number."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(s, use_decimal=True)

    check_syntax_err(exc_info, "Invalid number", 1, len(s) + 1)


@pytest.mark.parametrize("s", ["1\uff10", "0.\uff10", "0e\uff10"])
def test_invalid_number(s: str) -> None:
    """Test invalid number."""
    with pytest.raises(JSONSyntaxError):
        load_query_value(s)


@pytest.mark.parametrize("s", [
    # Empty string
    "",

    # One character
    "$",

    # Multiple characters
    "foo",
])
def test_string(s: str) -> None:
    """Test JSON string."""
    assert load_query_value(f"'{s}'") == s


@pytest.mark.parametrize(("s", "expected"), [
    # Tilde escapes
    ("~'", "'"),
    ("~~", "~"),

    # Multiple characters
    ("foo~~bar", "foo~bar"),
])
def test_string_escapes(s: str, expected: str) -> None:
    """Test string escapes."""
    assert load_query_value(f"'{s}'") == expected


@pytest.mark.parametrize(("s", "msg", "colno", "end_colno"), [
    ("'foo", "Unterminated string", 1, 5),
    ("'~", "Expecting escaped character", 3, -1),
    ("'~a'", "Invalid tilde escape", 2, 4),
])
def test_invalid_string(s: str, msg: str, colno: int, end_colno: int) -> None:
    """Test invalid JSON string."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(s)

    check_syntax_err(exc_info, msg, colno, end_colno)


@pytest.mark.parametrize("s", ["", "NaN"])
def test_expecting_value(s: str) -> None:
    """Test expecting JSON value."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value(s)

    check_syntax_err(exc_info, "Expecting value")


def test_end_of_file() -> None:
    """Test end of file."""
    with pytest.raises(JSONSyntaxError) as exc_info:
        load_query_value("1 2 3")

    check_syntax_err(exc_info, "Expecting end of file", 2)
