"""JSON tests."""
from __future__ import annotations

__all__: list[str] = []

from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

import pytest

from jsonyx import JSONSyntaxError, detect_encoding, format_syntax_error

if TYPE_CHECKING:
    from types import ModuleType


@pytest.mark.parametrize(("s", "encoding"), [
    # JSON must start with ASCII character (not NULL)
    # Strings can't contain control characters (including NULL)

    # Empty string
    ("", "utf-8"),

    # utf-8
    ("XX", "utf-8"),  # 1 ASCII character
    ("XX XX", "utf-8"),  # 2 ASCII characters
    ("XX XX XX", "utf-8"),  # 3 ASCII characters
    ("XX XX XX XX", "utf-8"),  # 4 ASCII characters

    # utf-8-sig
    ("ef bb bf", "utf-8-sig"),  # Empty JSON with BOM
    ("ef bb bf XX", "utf-8-sig"),  # BOM + 1 ASCII character

    # utf-16-be
    ("00 XX", "utf-16-be"),  # 1 ASCII character (BE)
    ("00 XX 00 XX", "utf-16-be"),  # 2 ASCII characters (BE)
    ("00 XX XX 00", "utf-16-be"),  # 1 ASCII + 1 Unicode character (BE)
    ("00 XX XX XX", "utf-16-be"),  # 1 ASCII + 1 Unicode character (BE)

    # utf-16-le
    ("XX 00", "utf-16-le"),  # 1 ASCII character (LE)
    ("XX 00 00 XX", "utf-16-le"),  # 1 ASCII + 1 Unicode character (LE)
    ("XX 00 XX 00", "utf-16-le"),  # 2 ASCII characters (LE)
    ("XX 00 XX XX", "utf-16-le"),  # 1 ASCII + 1 Unicode character (LE)

    # utf-16
    ("fe ff", "utf-16"),  # Empty JSON with BOM (BE)
    ("fe ff 00 XX", "utf-16"),  # BOM + 1 ASCII character (BE)
    ("ff fe", "utf-16"),  # Empty JSON with BOM (LE)
    ("ff fe XX 00", "utf-16"),  # BOM + 1 ASCII character (LE)

    # utf-32-be
    ("00 00 00 XX", "utf-32-be"),  # 1 ASCII character (BE)

    # utf-32-le
    ("XX 00 00 00", "utf-32-le"),  # 1 ASCII character (LE)

    # utf-32
    ("00 00 fe ff", "utf-32"),  # Empty JSON with BOM (BE)
    ("00 00 fe ff 00 00 00 XX", "utf-32"),  # BOM + 1 ASCII character (BE)
    ("ff fe 00 00", "utf-32"),  # Empty JSON with BOM (LE)
    ("ff fe 00 00 XX 00 00 00", "utf-32"),  # BOM + 1 ASCII character (LE)
])
def test_detect_encoding(s: str, encoding: str) -> None:
    """Test detect JSON encoding."""
    assert detect_encoding(bytes.fromhex(s.replace("XX", "01"))) == encoding


@pytest.mark.parametrize(("doc", "end", "line_range", "column_range"), [
    ("line 1", 5, "1", "6"),
    #      ^
    ("line 1", 6, "1", "6-7"),
    #      ^
    ("line 1\nline 2", 12, "1-2", "6"),
    #      ^^^^^^^^
    ("line 1\nline 2", 13, "1-2", "6-7"),
    #      ^^^^^^^^^
])
def test_format_syntax_error(
    doc: str, end: int, line_range: str, column_range: str,
) -> None:
    """Test format_syntax_error."""
    exc: JSONSyntaxError = JSONSyntaxError("", "<string>", doc, 5, end)
    assert format_syntax_error(exc)[0] == (
        f'  File "<string>", line {line_range}, column {column_range}\n'
    )


def test_load(json: ModuleType) -> None:
    """Test JSON load."""
    assert json.load(StringIO("0")) == 0


def test_read(json: ModuleType) -> None:
    """Test JSON read."""
    with TemporaryDirectory() as tmpdir:
        filename: Path = Path(tmpdir) / "file.json"
        filename.write_text("0", "utf-8")
        assert json.read(filename) == 0
