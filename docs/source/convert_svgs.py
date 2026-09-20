"""Convert svgs."""
from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


def _invert_color(match: re.Match[str]) -> str:
    hex_color: str = match.group(1)
    r: int = 255 - int(hex_color[0:2], 16)
    g: int = 255 - int(hex_color[2:4], 16)
    b: int = 255 - int(hex_color[4:6], 16)
    return f"#{r:02X}{g:02X}{b:02X}"


def _invert_svg(src_path: Path, dst_path: Path) -> None:
    if dst_path.exists() and dst_path.stat().st_mtime > src_path.stat().st_mtime:
        return

    content: str = Path(src_path).read_text(encoding="utf-8")
    inverted_content: str = re.sub(
        r"#([0-9a-fA-F]{6})", _invert_color, content,
    )
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    Path(dst_path).write_text(inverted_content, encoding="utf-8")


def _invert_svgs(src_dir: Path, dst_dir: Path) -> None:
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".svg"):
                src_path: Path = Path(root) / file
                relative_path: Path = src_path.relative_to(src_dir)
                dst_path: Path = dst_dir / relative_path
                _invert_svg(src_path, dst_path)


def _svg2pdf(src_path: Path) -> None:
    dst_path: Path = src_path.with_suffix(".pdf")
    if dst_path.exists() and dst_path.stat().st_mtime > src_path.stat().st_mtime:
        return

    subprocess.run([
        "inkscape",
        "--export-area-drawing",
        f"--export-filename={dst_path}",
        src_path,
    ], check=True)


def _svgs2pdfs(src_dir: Path) -> None:
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".svg"):
                _svg2pdf(Path(root) / file)


def _main() -> None:
    images_dir: Path = Path("_images")
    src_dir: Path = images_dir / "light"
    dst_dir: Path = images_dir / "dark"
    _invert_svgs(src_dir, dst_dir)
    _svgs2pdfs(src_dir)


if __name__ == "__main__":
    _main()
