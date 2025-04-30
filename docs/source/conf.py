"""Configuration file for the Sphinx documentation builder."""
from __future__ import annotations

from datetime import datetime, timezone
from os import environ, getenv
from typing import Any

# -- Project information

branch: str = getenv("READTHEDOCS_GIT_IDENTIFIER", "main")
year: int = datetime.now(tz=timezone.utc).year

author: str = "Nice Zombies"
# pylint: disable-next=W0622
copyright: str = f"{year}, Nice Zombies"  # noqa: A001
release: str = "2.2"  # 2.2.1
project: str = "jsonyx"
version: str = "latest" if branch == "main" else branch

# -- General configuration

extensions: list[str] = [
    "notfound.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
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
    "numpy": ("https://numpy.org/doc/stable", None),
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}
intersphinx_disabled_domains: list[str] = ["std"]
nitpicky: bool = True
nitpick_ignore: list[tuple[str, str]] = [
    ("py:class", "jsonyx._decoder._SupportsRead"),
    ("py:class", "jsonyx._encoder._SupportsWrite"),
    ("py:class", "jsonyx._SupportsRead"),
    ("py:class", "jsonyx._SupportsWrite"),
]
templates_path = ["_templates"]

# -- Options for HTML output

html_baseurl: str = environ.get(
    "READTHEDOCS_CANONICAL_URL", "http://jsonyx.readthedocs.io/en/latest/",
)
html_context: dict[str, Any] = {
    "breadcrumb_include_page": True,
    "conf_py_path": "/docs/source/",
    "display_github": True,
    "github_user": "nineteendo",
    "github_repo": "jsonyx",
    "github_version": branch,
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
    "source_branch": branch,
    "source_directory": "docs/source/",
}

# -- Options for EPUB output

epub_show_urls: str = "no"

# -- Options for PDF output

latex_documents: list[tuple[str, str, str, str, str]] = [
    (
        "contents",
        f"{project}.tex",
        f"{project} Documentation",
        author,
        "manual",
    ),
]
latex_engine: str = "xelatex"
latex_use_xindy: bool = False

# -- Options for sphinx.ext.autodoc

autodoc_preserve_defaults: bool = True
autodoc_type_aliases: dict[str, str] = {
    name: name for name in ["_Hook", "_Node", "_Operation", "_StrPath"]
}
autodoc_typehints: str = "none"

# -- Options for sphinx.ext.todo

todo_include_todos: bool = True

# -- Options for sphinx_autodoc_typehints

always_use_bars_union: bool = True
typehints_defaults: str | None = "comma"
typehints_document_rtype_none: bool = False
typehints_use_rtype: bool = False

# -- Options for sphinx_copybutton

copybutton_exclude: str = ".linenos, .gp, .go"
copybutton_line_continuation_character: str = "\\"

# -- Options for sphinx_issues

issues_github_path: str = "nineteendo/jsonyx"

# -- Options for sphinxext.opengraph

ogp_enable_meta_description: bool = True

# -- Options for sphinx_sitemap

sitemap_excludes: list[str] = [
    "_modules", "contents.html", "forword.html", "genindex.html",
    "py-modindex.html", "search.html",
]
sitemap_url_scheme: str = "{link}"
