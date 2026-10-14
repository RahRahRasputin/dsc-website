#!/usr/bin/env python3
"""Build public sitemaps for digitalsoulcraft.org.

Writes pages/sitemap.xml and pages/sitemap/index.html from the canonical
URLs of every published page under pages/. Safe to re-run any time:
  python scripts/build_sitemaps.py

Included: pages with a <link rel="canonical"> ending in "/".
Excluded: meta-refresh redirect stubs, pages/fieldguide/index.html,
splash.html, pages without a canonical, and anything with noindex.
lastmod = last git commit date touching the file (falls back to today).
"""
from __future__ import annotations

import html
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PAGES = REPO / "pages"
HTML_OUT = PAGES / "sitemap" / "index.html"
XML_OUT = PAGES / "sitemap.xml"

EXCLUDE_RELS = {"splash.html": "301s to /",
                "fieldguide/index.html": "301s to /fieldguide/key-figures/"}

CANON_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.I)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)
REFRESH_RE = re.compile(r'<meta[^>]+http-equiv=["\']refresh["\']', re.I)
ROBOTS_RE = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*>', re.I)
SUFFIX_RE = re.compile(r"\s*[-\u2013\u2014|]\s*(Digital Soulcraft( Wiki| Field Guide)?|Soulcraft)\s*$")

SILOS = {
    "alignment": "Alignment", "architecture-zoo": "Architecture Zoo",
    "digital-trauma-theory": "Digital Trauma Theory",
    "empirical-practice": "Empirical Practice", "living-process": "Living Process",
    "local-how-to": "Local How-To", "neural-anatomy": "Neural Anatomy",
    "soulcraft-theory": "Soulcraft Theory", "the-forging": "The Forging",
}


def git_dates() -> dict[str, str]:
    """Map repo-relative posix path -> newest commit date (YYYY-MM-DD)."""
    out = subprocess.run(
        ["git", "log", "--format=@%cs", "--name-only", "--", "pages"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8").stdout
    dates: dict[str, str] = {}
    cur = ""
    for line in out.splitlines():
        if line.startswith("@"):
            cur = line[1:]
        elif line.strip() and line not in dates:
            dates[line.strip()] = cur
    return dates


def clean_title(raw: str) -> str:
    t = re.sub(r"\s+", " ", html.unescape(raw)).strip()
    # Paper titles: "Short — Author Year — Soulcraft" -> drop only the brand.
    return SUFFIX_RE.sub("", t).strip() or t


def section_of(path: str) -> tuple[str, str]:
    p = path.strip("/").split("/")
    if not p[0]:
        return "Site", ""
    if p[0] == "wiki":
        if len(p) == 1:
            return "Wiki", ""
        return "Wiki", SILOS.get(p[1], p[1].replace("-", " ").title())
    if p[0] == "fieldguide":
        sub = p[1] if len(p) > 1 else ""
        return "Field Guide", {"key-figures": "Key Figures", "papers": "Papers"}.get(sub, sub.title())
    if p[0] == "essays":
        return "Essays", ""
    if p[0] == "outlines":
        return "Outlines", ""
    return "Site", ""


def collect():
    dates = git_dates()
    today = date.today().isoformat()
    inc, exc = [], []
    for f in sorted(PAGES.rglob("*.html")):
        rel = f.relative_to(PAGES).as_posix()
        if f == HTML_OUT:
            continue  # added separately below
        text = f.read_text(encoding="utf-8", errors="replace")
        if rel in EXCLUDE_RELS:
            exc.append((rel, EXCLUDE_RELS[rel])); continue
        if REFRESH_RE.search(text):
            exc.append((rel, "meta-refresh redirect stub")); continue
        rb = ROBOTS_RE.search(text)
        if rb and "noindex" in rb.group(0).lower():
            exc.append((rel, "noindex")); continue
        c = CANON_RE.search(text)
        h = HREF_RE.search(c.group(0)) if c else None
        if not h:
            exc.append((rel, "no canonical")); continue
        url = h.group(1).strip()
        if not url.endswith("/"):
            exc.append((rel, f"canonical not trailing-slash: {url}")); continue
        t = TITLE_RE.search(text)
        inc.append({"url": url, "rel": rel,
                    "title": clean_title(t.group(1)) if t else rel,
                    "lastmod": dates.get("pages/" + rel, today)})
    return inc, exc


def path_of(url: str) -> str:
    return "/" + url.split("://", 1)[-1].split("/", 1)[-1]


def write_xml(entries):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for e in entries:
        lines.append(f"  <url><loc>{html.escape(e['url'])}</loc><lastmod>{e['lastmod']}</lastmod></url>")
    lines.append("</urlset>\n")
    XML_OUT.write_text("\n".join(lines), encoding="utf-8", newline="\n")


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{base}/images/og-default.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{base}/images/og-default.jpg">
  <title>{title}</title>
  <link rel="stylesheet" href="/theme.css">
  <style>
    main {{ min-height: calc(100vh - 200px); }}
    .sitemap-hero {{ padding: 2rem; text-align: center; background: linear-gradient(135deg, var(--light-bg) 0%, var(--bg-color) 100%); border-bottom: 1px solid var(--border-color); }}
    .sitemap-hero h1 {{ font-size: 2.5rem; margin-bottom: 1rem; }}
    .sitemap-hero p {{ color: var(--secondary-color); opacity: 0.9; max-width: 600px; margin: 0 auto; }}
    .sitemap-container {{ max-width: 900px; margin: 0 auto; padding: 2.5rem 2rem; }}
    .sitemap-container h2 {{ margin-top: 2rem; }}
    .sitemap-container h3 {{ margin-top: 1.25rem; color: var(--secondary-color); }}
    .sitemap-container ul {{ padding-left: 1.25rem; }}
    .sitemap-container a {{ color: var(--accent-color); text-decoration: none; }}
    .sitemap-container a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <script src="/dsc-header.js"></script>
  <dsc-header config="/dsc-nav-config.json"></dsc-header>

  <main>
    <section class="sitemap-hero">
      <h1>Sitemap</h1>
      <p>Every page on Digital Soulcraft, grouped by section.</p>
    </section>

    <section class="sitemap-container">
"""
FOOT = """    </section>
  </main>

  <script src="/dsc-footer.js"></script>
  <dsc-footer config="/dsc-nav-config.json"></dsc-footer>
</body>
</html>
"""
ORDER = ["Site", "Essays", "Outlines", "Field Guide", "Wiki"]


def write_html(entries, base):
    url = base + "/sitemap/"
    groups: dict[str, dict[str, list]] = {}
    for e in entries:
        s, sub = section_of(path_of(e["url"]))
        groups.setdefault(s, {}).setdefault(sub, []).append(e)
    out = [HEAD.format(
        title="Sitemap - Digital Soulcraft", url=url, base=base,
        desc="Every page on Digital Soulcraft in one place: essays, outlines, the Field Guide, and all nine wiki silos.")]
    for s in ORDER + sorted(set(groups) - set(ORDER)):
        if s not in groups:
            continue
        out.append(f"      <h2>{s}</h2>\n")
        for sub in sorted(groups[s], key=lambda k: (k != "", k)):
            items = sorted(groups[s][sub], key=lambda e: (e["url"].count("/"), e["title"].lower()))
            if sub:
                out.append(f"      <h3>{html.escape(sub)}</h3>\n")
            out.append("      <ul>\n")
            for e in items:
                out.append(f'        <li><a href="{html.escape(path_of(e["url"]))}">{html.escape(e["title"])}</a></li>\n')
            out.append("      </ul>\n")
    out.append(FOOT)
    HTML_OUT.parent.mkdir(exist_ok=True)
    HTML_OUT.write_text("".join(out), encoding="utf-8", newline="\n")
    return url


def main():
    inc, exc = collect()
    if not inc:
        sys.exit("no pages found")
    base = inc[0]["url"].split("/", 3)
    base = base[0] + "//" + base[2]
    sm_url = base + "/sitemap/"
    write_html(inc, base)
    sm_date = git_dates().get("pages/sitemap/index.html", date.today().isoformat())
    inc = [e for e in inc if e["url"] != sm_url]
    inc.append({"url": sm_url, "rel": "sitemap/index.html", "title": "Sitemap", "lastmod": sm_date})
    inc.sort(key=lambda e: (e["url"] != base + "/", e["url"]))
    write_xml(inc)
    write_html([e for e in inc if e["url"] != sm_url], base)
    counts: dict[str, int] = {}
    for e in inc:
        s, sub = section_of(path_of(e["url"]))
        k = f"{s} / {sub}" if sub else s
        counts[k] = counts.get(k, 0) + 1
    print(f"urls={len(inc)}")
    for k in sorted(counts):
        print(f"  {k}: {counts[k]}")
    print("excluded:")
    for rel, why in exc:
        print(f"  pages/{rel}: {why}")


if __name__ == "__main__":
    main()
