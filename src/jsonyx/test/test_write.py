"""JSON write tests."""
from __future__ import annotations

__all__: list[str] = []

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING

import pytest

from jsonyx.allow import SURROGATES

if TYPE_CHECKING:
    from types import ModuleType


def test_value(json: ModuleType) -> None:
    """Test JSON value."""
    with TemporaryDirectory() as tmpdir:
        filename: Path = Path(tmpdir) / "file.json"
        json.write(0, filename, end="")
        assert filename.read_text("utf-8") == "0"


# ruff: ignore[PT014]
@pytest.mark.parametrize("s", ["\ud800", "\ud800$", "\udf48"])
def test_surrogates(json: ModuleType, s: str) -> None:
    """Test surrogates."""
    with TemporaryDirectory() as tmpdir:
        filename: Path = Path(tmpdir) / "file.json"
        json.write(s, filename, allow=SURROGATES, end="")
        assert filename.read_text("utf-8", "surrogatepass") == f'"{s}"'


# ruff: ignore[PT014]
@pytest.mark.parametrize("s", ["\ud800", "\ud800$", "\udf48"])
def test_surrogates_if_not_allowed(json: ModuleType, s: str) -> None:
    """Test surrogates."""
    with TemporaryDirectory() as tmpdir, \
            pytest.raises(json.TruncatedSyntaxError):
        json.write(s, Path(tmpdir) / "file.json")


def test_encoding(json: ModuleType) -> None:
    """Test encoding."""
    with TemporaryDirectory() as tmpdir:
        filename: Path = Path(tmpdir) / "file.json"
        json.write(0, filename, end="", encoding="utf-8-sig")
        assert filename.read_text("utf-8-sig") == "0"
