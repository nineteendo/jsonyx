# Copyright (C) 2024 Nice Zombies
"""JSONYX extension modules."""
from __future__ import annotations

__all__: list[str] = []

# pylint: disable-next=E0401
from setuptools import Extension, setup  # type: ignore

if __name__ == "__main__":
    setup(ext_modules=[
        Extension("_jsonyx.__init__", ["src/_jsonyx/__init__.c"]),
    ])
