# Copyright (C) 2024 Nice Zombies
"""Configuration file for the Sphinx documentation builder."""
from __future__ import annotations

from os import environ, getenv
from typing import Any

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
    "sphinx.ext.viewcode",
    "sphinx_toggleprompt",
]

intersphinx_mapping: dict[str, tuple[str, None]] = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains: list[str] = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_context: dict[str, Any] = {
    "conf_py_path": "/docs/source/",
    "display_github": True,
    "github_user": "nineteendo",
    "github_repo": "jsonyx",
    "github_version": getenv("READTHEDOCS_GIT_IDENTIFIER", "main"),
    "slug": "jsonyx",
}
if "READTHEDOCS" in environ:
    html_context["READTHEDOCS"] = True

html_theme: str = "furo"
html_theme_options: dict[str, Any] = {
    "navigation_with_keys": True,
    "source_repository": "https://github.com/nineteendo/jsonyx/",
    "source_branch": getenv("READTHEDOCS_GIT_IDENTIFIER", "main"),
    "source_directory": "docs/source/",
}

# -- Options for EPUB output
epub_show_urls: str = "no"
