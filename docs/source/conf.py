# Copyright (C) 2024 Nice Zombies
"""Configuration file for the Sphinx documentation builder."""
from __future__ import annotations

# -- Project information

project: str = "jsonyx"
# pylint: disable-next=W0622
copyright: str = "2024, Nice Zombies"  # noqa: A001
author: str = "Nice Zombies"

release: str = "2.0"
version: str = "2.0.0"

# -- General configuration

extensions: list[str] = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping: dict[str, tuple[str, None]] = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains: list[str] = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme: str = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls: str = "footnote"
