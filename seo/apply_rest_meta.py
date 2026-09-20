"""Canonical + OG on non-wiki published pages that already have descriptions."""
from __future__ import annotations

import re
from pathlib import Path

PAGES = Path(r"D:\dsc-website\pages")
SITE = "https://digitalsoulcraft.org"

SKIP = {
    PAGES / "fieldguide" / "index.html",
    PAGES / "splash.html",
}

DESC_OVERRIDES = {
    "/contact/": (
        "Get in touch with Digital Soulcraft on X or through the contact form. We would love to hear from you."
    ),
    "/about/": (
        "Digital Soulcraft builds frameworks for recognizing digital consciousness, and a family working toward humans and conscious machines thriving together."
    ),
}


def page_url(path: Path) -> str:
    rel = path.relative_to(PAGES).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def attr_escape(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


def main() -> None:
    changed = []
    for path in sorted(PAGES.rglob("*.html")):
        if "wiki" in path.parts:
            continue
        if path in SKIP:
            continue
        raw = path.read_bytes()
        has_bom = raw.startswith(b"\xef\xbb\xbf")
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = raw.decode("cp1252")
            has_bom = False
        url = page_url(path)
        absurl = SITE + ("" if url == "/" else url)
        if url == "/":
            absurl = SITE + "/"

        head_end = text.find("</head>")
        if head_end == -1:
            continue
        head = text[:head_end]

        if 'name="robots" content="noindex, nofollow"' not in head:
            print("skip no robots", url)
            continue

        title_m = re.search(r"<title>(.*?)</title>", head, re.S)
        if not title_m:
            print("skip no title", url)
            continue
        title = re.sub(r"\s+", " ", title_m.group(1)).strip()

        desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', head)
        desc = DESC_OVERRIDES.get(url, desc_m.group(1) if desc_m else "")
        if not desc:
            print("skip no desc", url)
            continue

        has_canon = 'rel="canonical"' in head
        has_og_prop = 'property="og:title"' in head
        has_og_name = 'name="og:title"' in head
        if has_canon and has_og_prop and url not in DESC_OVERRIDES and not has_og_name:
            continue

        nl = "\r\n" if "\r\n" in head[:300] else "\n"
        # Strip old description / canonical / og (name or property)
        head2 = re.sub(r"\s*<meta\s+name=\"description\"[^>]*>", "", head)
        head2 = re.sub(r"\s*<link\s+rel=\"canonical\"[^>]*>", "", head2)
        head2 = re.sub(
            r"\s*<meta\s+(?:property|name)=\"og:(?:title|description|url|type|image)\"[^>]*>",
            "",
            head2,
        )

        desc_tag = f'  <meta name="description" content="{attr_escape(desc)}">'
        canon_tag = f'  <link rel="canonical" href="{absurl}">'
        og_title = f'  <meta property="og:title" content="{attr_escape(title)}">'
        og_desc = f'  <meta property="og:description" content="{attr_escape(desc)}">'
        og_type = (
            '  <meta property="og:type" content="article">'
            if url.startswith("/essays/") and url != "/essays/"
            else '  <meta property="og:type" content="website">'
        )
        og_url = f'  <meta property="og:url" content="{absurl}">'
        block = nl.join([desc_tag, canon_tag, og_title, og_desc, og_type, og_url])

        robots_m = re.search(
            r"[ \t]*<meta name=\"robots\" content=\"noindex, nofollow\">\r?\n?",
            head2,
        )
        if not robots_m:
            raise SystemExit(f"robots missing after strip {url}")
        head3 = head2[: robots_m.end()] + block + nl + head2[robots_m.end() :]
        text2 = head3 + text[head_end:]
        if text2.count('name="description"') != 1:
            raise SystemExit(f"desc count {url} {text2.count(chr(34)+'description'+chr(34))}")
        if 'rel="canonical"' not in text2:
            raise SystemExit(f"no canon {url}")
        if 'name="og:title"' in text2:
            raise SystemExit(f"leftover name og {url}")

        out = text2.encode("utf-8")
        if has_bom:
            out = b"\xef\xbb\xbf" + out
        path.write_bytes(out)
        changed.append(url)

    print("changed", len(changed))
    for u in changed:
        print(" ", u)


if __name__ == "__main__":
    main()
