from __future__ import annotations
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse, unquote, urljoin

ROOT = Path(r"D:\dsc-website\pages")
published = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}


def page_url(rel: Path) -> str:
    posix = rel.as_posix()
    if posix == "index.html":
        return "/"
    if posix.endswith("/index.html"):
        return "/" + posix[: -len("index.html")]
    return "/" + posix


def file_exists(url_path: str) -> bool:
    path = unquote(url_path)
    if path.startswith("/"):
        path = path[1:]
    if not path:
        return "index.html" in published
    if path.endswith("/"):
        return (path + "index.html") in published
    name = Path(path).name
    if "." in name:
        return path in published
    return (path + "/index.html") in published or (path + ".html") in published


def resolve(current_url: str, href: str) -> str | None:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        return None
    # drop query/hash
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    base = "https://digitalsoulcraft.org" + current_url
    if not current_url.endswith("/"):
        base += "/"
    joined = urljoin(base, href)
    path = urlparse(joined).path
    return path or "/"


broken_page = Counter()
broken_asset = Counter()
from_pages = defaultdict(list)
skip_ext = {".css", ".js", ".json", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".woff", ".woff2", ".md", ".txt"}

for p in sorted(ROOT.rglob("*.html")):
    rel = p.relative_to(ROOT)
    url = page_url(rel)
    text = p.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'''(?:href|src)=["']([^"']+)["']''', text, re.I):
        href = m.group(1)
        path = resolve(url, href)
        if path is None:
            continue
        ok = file_exists(path)
        if ok:
            continue
        ext = Path(path).suffix.lower()
        if ext in skip_ext or path.startswith("/Logos/") or "/images/" in path:
            broken_asset[path] += 1
            from_pages[path].append(url)
        else:
            broken_page[path] += 1
            from_pages[path].append(url)

print("broken page unique", len(broken_page), "instances", sum(broken_page.values()))
for path, n in broken_page.most_common(60):
    srcs = sorted(set(from_pages[path]))[:6]
    print(f"  {n:3d} {path}  from {srcs}")

print("\nbroken asset unique", len(broken_asset), "instances", sum(broken_asset.values()))
for path, n in broken_asset.most_common(30):
    srcs = sorted(set(from_pages[path]))[:6]
    print(f"  {n:3d} {path}  from {srcs}")
