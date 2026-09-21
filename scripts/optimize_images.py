#!/usr/bin/env python3
"""Convert pages/ PNG/JPG to display-sized WebP and rewrite HTML/JS/CSS refs.

Keeps originals. Skips favicon.png (browsers still want PNG/ICO).
Re-run after James ships a new plate.

  python scripts/optimize_images.py
"""
from __future__ import annotations

import io
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "pages"
MAX_WIDTH = 1200
FEATURE_BUDGET = 200_000  # bytes
INLINE_BUDGET = 100_000
QUALITY_STEPS = (80, 75, 70, 65, 60, 55)
WIDTH_STEPS = (1200, 1000, 800)
SKIP_NAMES = {"favicon.png"}
RASTER = {".png", ".jpg", ".jpeg"}
REWRITE_SUFFIXES = {".html", ".js", ".css", ".json"}


def is_feature(path: Path) -> bool:
    name = path.stem.lower()
    return "feature" in name


def fit_width(im: Image.Image, max_w: int) -> Image.Image:
    w, h = im.size
    if w <= max_w:
        return im
    new_h = max(1, round(h * max_w / w))
    return im.resize((max_w, new_h), Image.Resampling.LANCZOS)


def prepare_mode(im: Image.Image) -> Image.Image:
    if im.mode in ("RGBA", "LA"):
        return im.convert("RGBA")
    if im.mode == "P":
        return im.convert("RGBA" if "transparency" in im.info else "RGB")
    if im.mode != "RGB":
        return im.convert("RGB")
    return im


def encode_webp(im: Image.Image, quality: int) -> bytes:
    buf = io.BytesIO()
    im.save(
        buf,
        format="WEBP",
        quality=quality,
        method=6,
    )
    return buf.getvalue()


def compress(im: Image.Image, budget: int) -> tuple[bytes, tuple[int, int], int]:
    """Return (bytes, size, quality) at or under budget when possible."""
    last = (b"", im.size, QUALITY_STEPS[-1])
    for max_w in WIDTH_STEPS:
        fitted = fit_width(im, min(max_w, im.width))
        for q in QUALITY_STEPS:
            data = encode_webp(fitted, q)
            last = (data, fitted.size, q)
            if len(data) <= budget:
                return last
    return last


def iter_rasters() -> list[Path]:
    out = []
    for p in PAGES.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in RASTER:
            continue
        if p.name.lower() in SKIP_NAMES:
            continue
        out.append(p)
    return sorted(out)


def convert_one(src: Path) -> dict:
    dest = src.with_suffix(".webp")
    with Image.open(src) as im:
        im.load()
        prepared = prepare_mode(im)
        orig_size = im.size
        budget = FEATURE_BUDGET if is_feature(src) else INLINE_BUDGET
        data, size, quality = compress(prepared, budget)
    dest.write_bytes(data)
    return {
        "src": src,
        "dest": dest,
        "orig_bytes": src.stat().st_size,
        "new_bytes": len(data),
        "orig_size": orig_size,
        "new_size": size,
        "quality": quality,
        "budget": budget,
        "over": len(data) > budget,
    }


def rewrite_refs(converted: list[Path]) -> int:
    """Replace basename.ext with basename.webp in published text files.

    Only rewrites names we actually converted, so code samples like
    path/to/image.jpg are left alone. Binary replace keeps Windows-1252 HTML intact.
    """
    names = {p.name.encode("ascii") for p in converted}
    webp_of = {p.name.encode("ascii"): p.with_suffix(".webp").name.encode("ascii") for p in converted}
    changed_files = 0
    for path in PAGES.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in REWRITE_SUFFIXES:
            continue
        raw = path.read_bytes()
        new = raw
        for name in names:
            if name in new:
                new = new.replace(name, webp_of[name])
        if new != raw:
            path.write_bytes(new)
            changed_files += 1
    return changed_files


def fmt_kb(n: int) -> str:
    return f"{n / 1000:7.1f} KB"


def main() -> int:
    rasters = iter_rasters()
    print(f"Converting {len(rasters)} images under {PAGES} (max width {MAX_WIDTH}px)")
    results = []
    for src in rasters:
        info = convert_one(src)
        results.append(info)
        flag = " OVER" if info["over"] else ""
        ow, oh = info["orig_size"]
        nw, nh = info["new_size"]
        print(
            f"{fmt_kb(info['orig_bytes'])} -> {fmt_kb(info['new_bytes'])}  q{info['quality']}"
            f"  {ow}x{oh}->{nw}x{nh}{flag}  {src.relative_to(PAGES).as_posix()}"
        )

    n_files = rewrite_refs([r["src"] for r in results])
    orig_total = sum(r["orig_bytes"] for r in results)
    new_total = sum(r["new_bytes"] for r in results)
    over = [r for r in results if r["over"]]
    print()
    print(f"Rewrote refs in {n_files} HTML/JS/CSS/JSON files")
    print(
        f"Payload if all used: {orig_total/1e6:.2f} MB -> {new_total/1e6:.2f} MB "
        f"({100 * (1 - new_total / orig_total):.0f}% smaller)"
    )
    if over:
        print(f"{len(over)} still over budget:")
        for r in over:
            print(f"  {fmt_kb(r['new_bytes'])} / {fmt_kb(r['budget'])}  {r['dest'].relative_to(PAGES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
