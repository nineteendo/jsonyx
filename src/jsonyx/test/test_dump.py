# Copyright (C) 2024 Nice Zombies
"""JSON dump tests."""
from __future__ import annotations

__all__: list[str] = []

from contextlib import redirect_stdout
from io import StringIO
from typing import TYPE_CHECKING

# pylint: disable-next=W0611
from jsonyx.test import get_json  # type: ignore # noqa: F401

if TYPE_CHECKING:
    from types import ModuleType


def test_file(json: ModuleType) -> None:
    """Test write to file."""
    io: StringIO = StringIO()
    json.dump(0, io, end="")
    assert io.getvalue() == "0"


def test_stdout(json: ModuleType) -> None:
    """Test write to stdout."""
    io: StringIO = StringIO()
    with redirect_stdout(io):
        json.dump(0, end="")
        assert io.getvalue() == "0"
