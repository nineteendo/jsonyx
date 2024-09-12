# Copyright (C) 2024 Nice Zombies
"""Configuration file for the Sphinx documentation builder."""
# TODO(Nice Zombies): update version
from __future__ import annotations

from os import environ, getenv
from typing import Any

# -- Project information

project: str = "jsonyx"
# pylint: disable-next=W0622
copyright: str = "2024, Nice Zombies"  # noqa: A001
author: str = "Nice Zombies"

release: str = "2.0"
version: str = "latest"

# -- General configuration

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinxext.opengraph",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_inline_tabs",
    "sphinx_issues",
    "sphinx_last_updated_by_git",
    "sphinx_sitemap",
]

intersphinx_mapping: dict[str, tuple[str, None]] = {
    "multidict": ("https://multidict.aio-libs.org/en/stable", None),
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
intersphinx_disabled_domains: list[str] = ["std"]
nitpicky: bool = True
nitpick_ignore: list[tuple[str, str]] = [
    ("py:class", "_Node"),
    ("py:class", "jsonyx._decoder._SupportsRead"),
    ("py:class", "jsonyx._differ._Operation"),
    ("py:class", "jsonyx._encoder._SupportsWrite"),
    ("py:class", "jsonyx._manipulator._Operation"),
    ("py:class", "jsonyx._Operation"),
    ("py:class", "jsonyx._SupportsRead"),
    ("py:class", "jsonyx._SupportsWrite"),
]
templates_path = ["_templates"]

# -- Options for HTML output

html_baseurl: str = "http://jsonyx.readthedocs.io/"
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

html_css_files = ["custom.css"]
html_static_path = ["_static"]
html_theme: str = "furo"
html_theme_options: dict[str, Any] = {
    "navigation_with_keys": True,
    "source_repository": "https://github.com/nineteendo/jsonyx/",
    "source_branch": getenv("READTHEDOCS_GIT_IDENTIFIER", "main"),
    "source_directory": "docs/source/",
}

# -- Options for EPUB output
epub_show_urls: str = "no"

# -- Options for PDF output

latex_engine: str = "xelatex"

# -- Options for autodoc

autodoc_preserve_defaults: bool = True
autodoc_type_aliases: dict[str, str] = {
    name: name for name in ["_Node", "_Operation", "_StrPath"]
}
autodoc_typehints: str = "none"

# -- Options for sphinx_autodoc_typehints

always_use_bars_union: bool = True
typehints_defaults: str | None = "comma"
typehints_use_rtype: bool = False

# -- Options for sphinx_copybutton

copybutton_exclude: str = ".linenos, .gp, .go"

# -- Options for sphinx_issues

issues_github_path: str = "nineteendo/jsonyx"

# -- Options for sphinxext.opengraph

ogp_enable_meta_description: bool = True
