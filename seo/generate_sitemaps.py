#!/usr/bin/env python3
"""Draft unpublished sitemaps for digitalsoulcraft.org.

Writes seo/sitemap.xml, seo/sitemap.html, and seo/SITEMAP.md.
Does not touch pages/, robots.txt, or git.
"""
from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parent.parent
PAGES = REPO / "pages"
SEO = Path(__file__).resolve().parent
BASE = "https://digitalsoulcraft.org"

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)

# Longest suffix first. Pages use em dash, en dash, or hyphen.
TITLE_SUFFIXES = (
    " — Digital Soulcraft Field Guide",
    " – Digital Soulcraft Field Guide",
    " - Digital Soulcraft Field Guide",
    " — Digital Soulcraft Wiki",
    " – Digital Soulcraft Wiki",
    " - Digital Soulcraft Wiki",
    " — Digital Soulcraft",
    " – Digital Soulcraft",
    " - Digital Soulcraft",
)

SILO_HEADINGS = {
    "alignment": "Alignment",
    "architecture-zoo": "Architecture Zoo",
    "digital-trauma-theory": "Digital Trauma Theory",
    "empirical-practice": "Empirical Practice",
    "living-process": "Living Process",
    "local-how-to": "Local How-To",
    "neural-anatomy": "Neural Anatomy",
    "soulcraft-theory": "Soulcraft Theory",
    "the-forging": "The Forging",
}

# Explicit exclusions inside pages/ (rel posix from pages/).
EXCLUDE_RELS = {
    "splash.html",  # 301 to /
    "fieldguide/index.html",  # 301 to /fieldguide/key-figures/
}


def strip_title_suffix(title: str) -> str:
    title = html.unescape(title).strip()
    title = re.sub(r"\s+", " ", title)
    for suffix in TITLE_SUFFIXES:
        if title.endswith(suffix):
            return title[: -len(suffix)].strip()
    return title


def page_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = TITLE_RE.search(text)
    if not m:
        return path.parent.name if path.name == "index.html" else path.stem
    return strip_title_suffix(m.group(1))


def rel_to_url(rel: Path) -> str:
    posix = rel.as_posix()
    if posix == "index.html":
        return BASE + "/"
    if posix.endswith("/index.html"):
        return BASE + "/" + posix[: -len("index.html")]
    return BASE + "/" + posix


def classify(rel: Path) -> tuple[str, str]:
    """Return (section, subsection) for HTML grouping."""
    posix = rel.as_posix()
    if posix.startswith("essays/"):
        return "essays", ""
    if posix.startswith("outlines/"):
        return "outlines", ""
    if posix.startswith("fieldguide/"):
        return "fieldguide", ""
    if posix.startswith("wiki/"):
        parts = posix.split("/")
        if len(parts) == 2 and parts[1] == "index.html":
            return "wiki", "hub"
        if len(parts) >= 2:
            return "wiki", parts[1]
        return "wiki", "hub"
    return "home", ""


def collect_pages() -> tuple[list[dict], list[dict]]:
    included: list[dict] = []
    excluded: list[dict] = []
    for path in sorted(PAGES.rglob("*.html")):
        rel = path.relative_to(PAGES)
        posix = rel.as_posix()
        if posix in EXCLUDE_RELS or posix.endswith("/essay-template.html") or posix == "essay-template.html":
            reason = {
                "splash.html": "301s to /",
                "fieldguide/index.html": "301s to /fieldguide/key-figures/",
            }.get(posix, "template / unpublished stub")
            excluded.append({"rel": posix, "reason": reason, "path": path})
            continue
        included.append(
            {
                "rel": posix,
                "path": path,
                "url": rel_to_url(rel),
                "title": page_title(path),
                "lastmod": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                .date()
                .isoformat(),
                "section": classify(rel)[0],
                "subsection": classify(rel)[1],
            }
        )
    included.sort(key=lambda e: (e["url"] != BASE + "/", e["url"]))
    return included, excluded


def write_xml(entries: list[dict], dest: Path) -> None:
    ET.register_namespace("", NS)
    urlset = ET.Element("urlset", xmlns=NS)
    for e in entries:
        url_el = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_el, "loc")
        loc.text = e["url"]
        lastmod = ET.SubElement(url_el, "lastmod")
        lastmod.text = e["lastmod"]
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    dest.write_bytes(
        b'<?xml version="1.0" encoding="UTF-8"?>\n'
        + ET.tostring(urlset, encoding="utf-8")
        + b"\n"
    )


def _li(entry: dict) -> str:
    return f'      <li><a href="{html.escape(entry["url"], quote=True)}">{html.escape(entry["title"])}</a></li>'


def write_html(entries: list[dict], dest: Path) -> None:
    by_section: dict[str, list[dict]] = {
        "home": [],
        "essays": [],
        "outlines": [],
        "fieldguide": [],
        "wiki": [],
        "other": [],
    }
    for e in entries:
        by_section.setdefault(e["section"], by_section["other"]).append(e)
        if e["section"] not in by_section:
            by_section["other"].append(e)

    def block(title: str, items: list[dict], heading: str = "h2") -> str:
        if not items:
            return ""
        lines = [f"  <{heading}>{html.escape(title)}</{heading}>", "  <ul>"]
        lines.extend(_li(e) for e in items)
        lines.append("  </ul>")
        return "\n".join(lines)

    parts: list[str] = [
        "<!-- DRAFT unpublished until splash comes down. Gary will restyle later. -->",
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="UTF-8">',
        "  <title>Sitemap (draft, unpublished)</title>",
        "</head>",
        "<body>",
        "  <h1>Sitemap</h1>",
        "  <p>Draft unpublished until splash comes down. Do not copy into pages/ until Brad says launch.</p>",
        block("Home / site", by_section["home"]),
        block("Essays", by_section["essays"]),
        block("Outlines", by_section["outlines"]),
        block("Field Guide", by_section["fieldguide"]),
    ]

    wiki = by_section["wiki"]
    if wiki:
        parts.append("  <h2>Wiki silos</h2>")
        hub = [e for e in wiki if e["subsection"] == "hub"]
        if hub:
            parts.append(block("Wiki hub", hub, heading="h3"))
        silo_order = sorted(
            {e["subsection"] for e in wiki if e["subsection"] not in ("", "hub")}
        )
        for slug in silo_order:
            heading = SILO_HEADINGS.get(slug, slug.replace("-", " ").title())
            items = [e for e in wiki if e["subsection"] == slug]
            # silo index first, then articles by URL
            items.sort(key=lambda e: (e["rel"].count("/") > 2, e["url"]))
            parts.append(block(heading, items, heading="h3"))

    if by_section["other"]:
        parts.append(block("Other", by_section["other"]))

    parts.extend(["</body>", "</html>", ""])
    dest.write_text("\n".join(p for p in parts if p), encoding="utf-8")


def write_md(
    entries: list[dict],
    excluded: list[dict],
    xml_count: int,
    html_count: int,
    dest: Path,
) -> None:
    lines = [
        "# Draft sitemaps (unpublished)",
        "",
        f"URL count: **{len(entries)}** (xml `{xml_count}`, html `{html_count}` — must match).",
        "",
        "These files must not be copied into `pages/` until Brad says launch.",
        "",
        "## Files (stay under `seo/`)",
        "",
        "- `D:\\dsc-website\\seo\\sitemap.xml`",
        "- `D:\\dsc-website\\seo\\sitemap.html`",
        "- `D:\\dsc-website\\seo\\SITEMAP.md` (this note)",
        "",
        "Published root is `pages/`. Netlify publishes that folder. Nothing here is live.",
        "",
        "`pages/robots.txt` is unchanged: `User-agent: *` / `Disallow: /`. No Sitemap line.",
        "",
        "## Included",
        "",
        "All other published HTML under `pages/` that a human should find at launch:",
        "home, about, contact, merch, bookshop (still a coming-soon page, but it is published),",
        "essays (including the orphan `/essays/right-side-of-history/`), outlines,",
        "field guide key-figures + papers, wiki hub and all nine silos.",
        "",
        f"Walked `{len(entries) + len(excluded)}` HTML files under `pages/`; excluded {len(excluded)}; included {len(entries)}.",
        "",
        "## Exclusions (not listed)",
        "",
    ]
    for e in excluded:
        lines.append(f"- `pages/{e['rel']}` — {e['reason']}")
    lines.extend(
        [
            "- `drafts/essay-template.html` — already moved out of `pages/`; not published",
            "- anything not under `pages/`",
            "- images, css, js, json, `robots.txt`",
            "",
            "## URL rules",
            "",
            "- Base: `https://digitalsoulcraft.org`",
            "- `pages/index.html` → `https://digitalsoulcraft.org/`",
            "- directory `index.html` → trailing-slash pretty URL",
            "- lastmod on each xml `<url>` is the file mtime as a W3C date (UTC)",
            "",
            "## Launch",
            "",
            "Splash stays until Brad announces a date. After the 2–3 week mailing-list window,",
            "when splash comes down: copy sitemap.xml (and restyled sitemap.html if wanted) into",
            "`pages/`, then add a Sitemap line to `robots.txt`. Not before.",
            "",
        ]
    )
    dest.write_text("\n".join(lines), encoding="utf-8")


def html_url_count(html_path: Path) -> int:
    text = html_path.read_text(encoding="utf-8")
    return len(re.findall(r"<li><a href=", text))


def xml_url_count(xml_path: Path) -> int:
    tree = ET.parse(xml_path)
    return len(tree.getroot())


def main() -> None:
    SEO.mkdir(parents=True, exist_ok=True)
    included, excluded = collect_pages()
    xml_path = SEO / "sitemap.xml"
    html_path = SEO / "sitemap.html"
    md_path = SEO / "SITEMAP.md"
    write_xml(included, xml_path)
    write_html(included, html_path)
    n_xml = xml_url_count(xml_path)
    n_html = html_url_count(html_path)
    write_md(included, excluded, n_xml, n_html, md_path)
    print(f"included={len(included)} xml={n_xml} html={n_html}")
    print("excluded:")
    for e in excluded:
        print(f"  {e['rel']} ({e['reason']})")
    print(f"wrote {xml_path}")
    print(f"wrote {html_path}")
    print(f"wrote {md_path}")
    if n_xml != n_html or n_xml != len(included):
        raise SystemExit("URL count mismatch")


if __name__ == "__main__":
    main()
