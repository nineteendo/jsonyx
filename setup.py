"""jsonyx setup."""
from __future__ import annotations

__all__: list[str] = []

from pathlib import Path

# pylint: disable-next=E0401
from setuptools import Extension, setup  # type: ignore

if __name__ == "__main__":
    setup(
        name="jsonyx",
        version="2.3.0",
        description="Customizable JSON library for Python",
        long_description=Path("README.md").read_text(encoding="utf-8"),
        long_description_content_type="text/markdown",
        author="Nice Zombies",
        author_email="nineteendo19d0@gmail.com",
        maintainer="Nice Zombies",
        maintainer_email="nineteendo19d0@gmail.com",
        packages=["jsonyx", "jsonyx.test"],
        ext_modules=[
            Extension("_jsonyx", ["src/jsonyx/_speedups.c"], optional=True),
        ],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: 3.14",
        ],
        license="GPL-3.0",
        keywords=["python", "json", "json-parser"],
        package_dir={"": "src"},
        # setuptools arguments
        entry_points={"console_scripts": ["jsonyx = jsonyx.__main__:main"]},
        python_requires=">=3.8",
        project_urls={
            "Homepage": "https://github.com/nineteendo/jsonyx",
            "Changelog": (
                "https://jsonyx.readthedocs.io/en/latest/changelog.html"
            ),
            "Documentation": "https://jsonyx.readthedocs.io",
            "Issues": "https://github.com/nineteendo/jsonyx/issues",
            "Sponser": "https://paypal.me/nineteendo",
        },
    )
