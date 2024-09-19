# Copyright (C) 2024 Nice Zombies
"""JSON run_filter_query tests."""
# TODO(Nice Zombies): add more tests
from __future__ import annotations

__all__: list[str] = []

from jsonyx import run_filter_query


def test_exist() -> None:
    """Test exist."""
    assert run_filter_query(([], 0), "@") == []


def test_not_exist() -> None:
    """Test not exist."""
    assert run_filter_query(([], 0), "!@") == [([], 0)]
