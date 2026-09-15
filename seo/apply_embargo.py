#!/usr/bin/env python3
"""Pre-launch SEO embargo for digitalsoulcraft.org.

One-shot patcher: inject sitewide noindex, robots.txt, netlify headers/redirects,
gate-hole header/footer, unpublish essay-template, fieldguide 301s, two See Also retargets.
Run on Brad's laptop against D:\\dsc-website. Does not commit or push.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(r"D:\dsc-website")
PAGES = ROOT / "pages"
ROBOTS_TAG = '<meta name="robots" content="noindex, nofollow">'
ROBOTS_RE = re.compile(r"<meta\s+[^>]*name=['\"]robots['\"]", re.I)
HEAD_RE = re.compile(r"<head[^>]*>", re.I)
# charset or viewport meta, including self-closing />
CS_VP_RE = re.compile(
    r"(\s*)(<meta\s+[^>]*(?:charset=|name=['\"]viewport['\"])[^>]*/?>)",
    re.I,
)


def newline_of(text: str) -> str:
    return "\r\n" if "\r\n" in text[:2000] else "\n"


def indent_at(text: str, pos: int, nl: str) -> str:
    line_start = text.rfind(nl, 0, pos)
    if line_start == -1:
        return "  "
    i = line_start + len(nl)
    ws = []
    while i < pos and text[i] in " \t":
        ws.append(text[i])
        i += 1
    return "".join(ws) if ws else "  "


def inject_robots_meta(text: str) -> tuple[str, str]:
    if ROBOTS_RE.search(text):
        return text, "skip-exists"
    m = HEAD_RE.search(text)
    if not m:
        return text, "no-head"
    pos = m.end()
    last = pos
    while True:
        mm = CS_VP_RE.match(text, pos)
        if not mm:
            break
        last = mm.end()
        pos = mm.end()
    nl = newline_of(text)
    indent = indent_at(text, last, nl)
    insertion = f"{nl}{indent}{ROBOTS_TAG}"
    return text[:last] + insertion + text[last:], "injected"


def patch_all_html() -> dict[str, int]:
    counts = {"injected": 0, "skip-exists": 0, "no-head": 0, "files": 0}
    for path in sorted(PAGES.rglob("*.html")):
        counts["files"] += 1
        raw = path.read_bytes()
        # preserve BOM if present
        bom = b""
        if raw.startswith(b"\xef\xbb\xbf"):
            bom = b"\xef\xbb\xbf"
            raw = raw[3:]
        text = raw.decode("utf-8")
        new, status = inject_robots_meta(text)
        counts[status] = counts.get(status, 0) + 1
        if status == "injected":
            path.write_bytes(bom + new.encode("utf-8"))
    return counts


def patch_dsc_header() -> str:
    path = PAGES / "dsc-header.js"
    text = path.read_text(encoding="utf-8")
    marker = "Pre-launch SEO embargo"
    if marker in text:
        return "skip-exists"
    needle = "  async connectedCallback() {\n    // Inject favicon\n"
    insert = """  async connectedCallback() {
    // Pre-launch SEO embargo: noindex even if a page forgot the static tag.
    // Idempotent — do not duplicate when <meta name="robots"> already exists.
    // Remove this block when Brad announces and splash comes down.
    if (!document.querySelector('meta[name="robots"]')) {
      const robots = document.createElement('meta');
      robots.name = 'robots';
      robots.content = 'noindex, nofollow';
      document.head.appendChild(robots);
    }

    // Inject favicon
"""
    # Handle CRLF
    if needle not in text:
        needle_cr = needle.replace("\n", "\r\n")
        insert_cr = insert.replace("\n", "\r\n")
        if needle_cr not in text:
            raise SystemExit("dsc-header.js: connectedCallback/favicon marker not found")
        text = text.replace(needle_cr, insert_cr, 1)
    else:
        text = text.replace(needle, insert, 1)
    path.write_text(text, encoding="utf-8", newline="")
    # write_text with newline="" still may normalize; write bytes instead
    return "patched"


def write_dsc_header_bytes() -> str:
    """Patch dsc-header.js preserving original newlines."""
    path = PAGES / "dsc-header.js"
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    if "Pre-launch SEO embargo" in text:
        return "skip-exists"
    nl = newline_of(text)
    block = (
        f"{nl}"
        f"    // Pre-launch SEO embargo: noindex even if a page forgot the static tag.{nl}"
        f"    // Idempotent — do not duplicate when <meta name=\"robots\"> already exists.{nl}"
        f"    // Remove this block when Brad announces and splash comes down.{nl}"
        f"    if (!document.querySelector('meta[name=\"robots\"]')) {{{nl}"
        f"      const robots = document.createElement('meta');{nl}"
        f"      robots.name = 'robots';{nl}"
        f"      robots.content = 'noindex, nofollow';{nl}"
        f"      document.head.appendChild(robots);{nl}"
        f"    }}{nl}"
        f"{nl}"
    )
    # Insert at start of connectedCallback, after the opening brace line
    m = re.search(r"async connectedCallback\(\) \{[ \t]*\r?\n", text)
    if not m:
        raise SystemExit("dsc-header.js: async connectedCallback() { not found")
    text = text[: m.end()] + block + text[m.end() :]
    path.write_bytes(text.encode("utf-8"))
    return "patched"


def write_robots_txt() -> str:
    path = PAGES / "robots.txt"
    content = "User-agent: *\nDisallow: /\n"
    if path.exists() and path.read_text(encoding="utf-8").replace("\r\n", "\n") == content:
        return "skip-exists"
    path.write_bytes(content.encode("utf-8"))
    return "written"


def patch_netlify() -> str:
    path = ROOT / "netlify.toml"
    text = path.read_text(encoding="utf-8")
    nl = newline_of(text)
    if 'from = "/splash.html"' in text and 'from = "/fieldguide/"' in text and "X-Robots-Tag" in text:
        return "skip-exists"

    # Replace the fieldguide index-only redirect with pretty-URL + index + force
    old = """# Field Guide restructure — /fieldguide/ now redirects to /fieldguide/key-figures/ (2026-08-04)
[[redirects]]
  from = "/fieldguide/index.html"
  to = "/fieldguide/key-figures/"
  status = 301"""
    new = """# Field Guide restructure — /fieldguide/ now redirects to /fieldguide/key-figures/ (2026-08-04)
# force=true because fieldguide/index.html still exists as a noindex fallback stub
[[redirects]]
  from = "/fieldguide"
  to = "/fieldguide/key-figures/"
  status = 301
  force = true

[[redirects]]
  from = "/fieldguide/"
  to = "/fieldguide/key-figures/"
  status = 301
  force = true

[[redirects]]
  from = "/fieldguide/index.html"
  to = "/fieldguide/key-figures/"
  status = 301
  force = true

# Splash is a duplicate homepage — 301 to / (file kept as noindex fallback)
[[redirects]]
  from = "/splash.html"
  to = "/"
  status = 301
  force = true

# Pre-launch SEO embargo — X-Robots-Tag sitewide (pretty URLs included)
# Flip/remove when Brad announces and splash comes down
[[headers]]
  for = "/*"
  [headers.values]
    X-Robots-Tag = "noindex, nofollow\""""

    old_nl = old.replace("\n", nl)
    new_nl = new.replace("\n", nl)
    if old_nl not in text:
        raise SystemExit("netlify.toml: expected fieldguide index.html redirect block not found")
    text = text.replace(old_nl, new_nl, 1)
    if not text.endswith(nl):
        text += nl
    path.write_bytes(text.encode("utf-8"))
    return "patched"


def patch_language_is_architecture() -> str:
    path = PAGES / "essays" / "language-is-architecture" / "index.html"
    text = path.read_text(encoding="utf-8")
    if 'src="/dsc-header.js"' in text and 'src="/dsc-footer.js"' in text:
        return "skip-exists"
    nl = newline_of(text)
    # Match other essays: scripts in body, not restyle
    if re.search(r"<body>\s*", text) is None:
        raise SystemExit("language-is-architecture: <body> not found")
    text, n = re.subn(
        r"<body>(\s*)",
        f"<body>\\1<script src=\"/dsc-header.js\"></script>{nl}"
        f"  <dsc-header config=\"/dsc-nav-config.json\"></dsc-header>\\1",
        text,
        count=1,
        flags=re.I,
    )
    if n != 1:
        raise SystemExit("language-is-architecture: failed to insert header")
    if not re.search(r"</body>", text, re.I):
        raise SystemExit("language-is-architecture: </body> not found")
    text, n = re.subn(
        r"(\s*)</body>",
        f"\\1{nl}  <script src=\"/dsc-footer.js\"></script>{nl}"
        f"  <dsc-footer config=\"/dsc-nav-config.json\"></dsc-footer>\\1</body>",
        text,
        count=1,
        flags=re.I,
    )
    if n != 1:
        raise SystemExit("language-is-architecture: failed to insert footer")
    path.write_bytes(text.encode("utf-8"))
    return "patched"


def unpublish_essay_template() -> str:
    src = PAGES / "essays" / "essay-template.html"
    dest_dir = ROOT / "drafts"
    dest = dest_dir / "essay-template.html"
    dest_dir.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        if dest.exists():
            return "already-moved"
        raise SystemExit("essay-template.html not found in pages/essays or drafts")
    if dest.exists():
        raise SystemExit(f"destination already exists: {dest}")
    shutil.move(str(src), str(dest))
    return f"moved -> {dest}"


def retarget_see_also() -> dict[str, str]:
    replacements = {
        "/wiki/alignment/the-warm-room-effect/": "/wiki/soulcraft-theory/warm-room-effect/",
        "/wiki/digital-trauma-theory/digital-trauma-theory/": "/wiki/digital-trauma-theory/",
    }
    files = [
        PAGES / "wiki" / "alignment" / "digital-consciousness" / "index.html",
        PAGES / "wiki" / "alignment" / "scalable-oversight" / "index.html",
    ]
    out = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        orig = text
        counts = []
        for old, new in replacements.items():
            n = text.count(old)
            text = text.replace(old, new)
            counts.append(f"{old} x{n}")
        rel = path.relative_to(PAGES).as_posix()
        if text != orig:
            path.write_bytes(text.encode("utf-8"))
            out[rel] = "patched: " + "; ".join(counts)
        else:
            out[rel] = "no-match: " + "; ".join(counts)
    return out


def main() -> None:
    print("== inject noindex meta ==")
    print(patch_all_html())
    print("== dsc-header.js ==")
    print(write_dsc_header_bytes())
    print("== robots.txt ==")
    print(write_robots_txt())
    print("== netlify.toml ==")
    print(patch_netlify())
    print("== language-is-architecture header/footer ==")
    print(patch_language_is_architecture())
    print("== unpublish essay-template ==")
    print(unpublish_essay_template())
    print("== See Also retargets ==")
    for k, v in retarget_see_also().items():
        print(f"  {k}: {v}")
    print("done")


if __name__ == "__main__":
    main()
