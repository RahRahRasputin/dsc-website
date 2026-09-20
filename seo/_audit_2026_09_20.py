# One-off on-page SEO scan of pages/. Prints a report to stdout.
from __future__ import annotations

import os
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(r"D:\dsc-website\pages")
SITE = "https://digitalsoulcraft.org"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.in_h = None
        self.h_parts: list[str] = []
        self.headings: list[tuple[int, str]] = []
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.imgs: list[dict[str, str]] = []
        self.scripts: list[str] = []
        self.jsonld = 0
        self.h1_count = 0
        self.lang_in_html = False

    def handle_starttag(self, tag, attrs):
        d = {k: (v or "") for k, v in attrs}
        if tag == "html" and "lang" in d:
            self.lang_in_html = True
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            self.metas.append(d)
        if tag == "link":
            self.links.append(d)
        if tag == "img":
            self.imgs.append(d)
        if tag == "script":
            src = d.get("src", "")
            self.scripts.append(src)
            if d.get("type") == "application/ld+json":
                self.jsonld += 1
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.in_h = int(tag[1])
            self.h_parts = []
            if tag == "h1":
                self.h1_count += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self.in_h:
            text = re.sub(r"\s+", " ", "".join(self.h_parts)).strip()
            self.headings.append((self.in_h, text))
            self.in_h = None
            self.h_parts = []

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self.in_h:
            self.h_parts.append(data)


def meta_by(metas, key, val):
    out = []
    for m in metas:
        if m.get(key, "").lower() == val.lower():
            out.append(m.get("content", ""))
    return out


def first_meta(metas, *pairs):
    for key, val in pairs:
        found = meta_by(metas, key, val)
        if found:
            return found[0]
    return ""


def page_url(rel: Path) -> str:
    posix = rel.as_posix()
    if posix == "index.html":
        return "/"
    if posix.endswith("/index.html"):
        return "/" + posix[: -len("index.html")]
    return "/" + posix


def exists_for_href(href: str, published: set[str]) -> bool | None:
    """Return True if known 200, False if likely 404, None if skip."""
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        return None
    path = urlparse(href).path
    if not path:
        return None
    path = unquote(path)
    if path.startswith("/"):
        path = path[1:]
    # asset extensions that exist as files
    if path.endswith("/"):
        cand = path + "index.html"
        return cand in published or path.rstrip("/") + "/index.html" in published
    if "." in Path(path).name:
        return path in published
    return (path + "/index.html") in published or (path + ".html") in published


def heading_skip(headings: list[tuple[int, str]]) -> bool:
    if not headings:
        return False
    last = headings[0][0]
    for level, _ in headings[1:]:
        if level > last + 1:
            return True
        last = level
    return False


def main():
    html_files = sorted(ROOT.rglob("*.html"))
    published = set()
    for p in ROOT.rglob("*"):
        if p.is_file():
            published.add(p.relative_to(ROOT).as_posix())

    rows = []
    missing_desc = []
    missing_robots = []
    missing_viewport = []
    missing_lang = []
    missing_canonical = []
    relative_canonical = []
    missing_og_title = []
    missing_og_desc = []
    missing_og_url = []
    missing_og_image = []
    og_name_not_property = []
    missing_twitter = []
    jsonld_pages = []
    no_h1 = []
    multi_h1 = []
    skip_h = []
    no_header = []
    missing_favicon_static = []
    title_lens = []
    desc_lens = []
    titles = defaultdict(list)
    descs = defaultdict(list)
    imgs_no_alt = []
    empty_alt = []
    broken = defaultdict(list)
    header_ok = 0
    robots_ok = 0
    desc_ok = 0
    canon_abs = 0
    og_title_ok = 0
    og_image_ok = 0
    jsonld_n = 0
    img_n = 0
    img_alt_ok = 0

    for p in html_files:
        rel = p.relative_to(ROOT)
        text = p.read_text(encoding="utf-8", errors="replace")
        parser = PageParser()
        try:
            parser.feed(text)
        except Exception as e:
            print("PARSE FAIL", rel, e)
            continue
        title = re.sub(r"\s+", " ", "".join(parser.title_parts)).strip()
        robots = first_meta(parser.metas, ("name", "robots"))
        desc = first_meta(parser.metas, ("name", "description"))
        viewport = first_meta(parser.metas, ("name", "viewport"))
        og_title = first_meta(parser.metas, ("property", "og:title"), ("name", "og:title"))
        og_desc = first_meta(parser.metas, ("property", "og:description"), ("name", "og:description"))
        og_url = first_meta(parser.metas, ("property", "og:url"), ("name", "og:url"))
        og_image = first_meta(parser.metas, ("property", "og:image"), ("name", "og:image"))
        og_type = first_meta(parser.metas, ("property", "og:type"), ("name", "og:type"))
        tw = first_meta(parser.metas, ("name", "twitter:card"))
        canon = ""
        icon = False
        for link in parser.links:
            rels = (link.get("rel") or "").lower().split()
            if "canonical" in rels:
                canon = link.get("href", "")
            if "icon" in rels or "shortcut" in rels or "apple-touch-icon" in rels:
                icon = True
        url = page_url(rel)
        has_header = any("dsc-header.js" in s for s in parser.scripts) or "<dsc-header" in text

        # og used name= instead of property=
        if re.search(r'<meta\s+name=["\']og:', text, re.I):
            og_name_not_property.append(url)

        title_lens.append((len(title), url, title))
        titles[title].append(url)
        if desc:
            desc_lens.append((len(desc), url, desc))
            descs[desc].append(url)
            desc_ok += 1
        else:
            missing_desc.append(url)
        if robots:
            robots_ok += 1
        else:
            missing_robots.append(url)
        if not viewport:
            missing_viewport.append(url)
        if not parser.lang_in_html:
            missing_lang.append(url)
        if canon:
            if canon.startswith("http"):
                canon_abs += 1
            else:
                relative_canonical.append((url, canon))
        else:
            missing_canonical.append(url)
        if og_title:
            og_title_ok += 1
        else:
            missing_og_title.append(url)
        if not og_desc:
            missing_og_desc.append(url)
        if not og_url:
            missing_og_url.append(url)
        if og_image:
            og_image_ok += 1
        else:
            missing_og_image.append(url)
        if not tw:
            missing_twitter.append(url)
        if parser.jsonld:
            jsonld_n += 1
            jsonld_pages.append(url)
        if parser.h1_count == 0:
            no_h1.append(url)
        elif parser.h1_count > 1:
            multi_h1.append((url, parser.h1_count))
        if heading_skip(parser.headings):
            skip_h.append((url, [f"h{lv}" for lv, _ in parser.headings[:12]]))
        if has_header:
            header_ok += 1
        else:
            no_header.append(url)
        if not icon:
            missing_favicon_static.append(url)

        for img in parser.imgs:
            img_n += 1
            alt = img.get("alt")
            src = img.get("src", "")
            if alt is None:
                imgs_no_alt.append((url, src))
            else:
                img_alt_ok += 1
                if alt.strip() == "":
                    empty_alt.append((url, src))

        # internal hrefs
        for m in re.finditer(r'''(?:href|src)=["']([^"']+)["']''', text, re.I):
            href = m.group(1)
            ok = exists_for_href(href, published)
            if ok is False:
                # ignore query/hash already stripped
                path = urlparse(href).path
                if path.endswith((".js", ".css", ".json", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".woff", ".woff2", ".md")):
                    broken["asset"].append((url, href))
                else:
                    broken["page"].append((url, href))

        rows.append(
            {
                "url": url,
                "title": title,
                "tlen": len(title),
                "dlen": len(desc) if desc else 0,
                "robots": robots,
                "canon": canon,
                "og_image": bool(og_image),
            }
        )

    print("=== COUNTS ===")
    print("html_files", len(html_files))
    print("robots_ok", robots_ok)
    print("missing_robots", len(missing_robots), missing_robots[:20])
    print("desc_ok", desc_ok)
    print("missing_desc", len(missing_desc))
    print("missing_viewport", len(missing_viewport), missing_viewport)
    print("missing_lang", len(missing_lang), missing_lang)
    print("canonical_abs", canon_abs)
    print("canonical_rel", len(relative_canonical), relative_canonical[:15])
    print("missing_canonical", len(missing_canonical))
    print("og_title_ok", og_title_ok)
    print("missing_og_title", len(missing_og_title))
    print("missing_og_desc", len(missing_og_desc))
    print("missing_og_url", len(missing_og_url))
    print("og_image_ok", og_image_ok)
    print("missing_og_image", len(missing_og_image))
    print("og_name_not_property", og_name_not_property)
    print("missing_twitter", len(missing_twitter))
    print("jsonld", jsonld_n, jsonld_pages)
    print("header_ok", header_ok)
    print("no_header", no_header)
    print("missing_favicon_static", len(missing_favicon_static))
    print("h1 none", no_h1)
    print("h1 multi", multi_h1)
    print("heading skips", len(skip_h))
    for item in skip_h:
        print("  SKIP", item[0], item[1])
    print("imgs", img_n, "with_alt_attr", img_alt_ok, "missing_alt", imgs_no_alt, "empty_alt", empty_alt)

    print("\n=== TITLE LENGTH ===")
    over60 = [x for x in title_lens if x[0] > 60]
    over70 = [x for x in title_lens if x[0] > 70]
    print("over60", len(over60), "over70", len(over70), "max", max(title_lens)[0] if title_lens else 0)
    for n, u, t in sorted(title_lens, reverse=True)[:15]:
        print(f"  {n:3d} {u} | {t}")

    print("\n=== DESC LENGTH ===")
    short = [x for x in desc_lens if x[0] < 70]
    longd = [x for x in desc_lens if x[0] > 160]
    print("short<70", len(short), "long>160", len(longd))
    for n, u, d in sorted(short)[:20]:
        print(f"  SHORT {n:3d} {u} | {d}")
    for n, u, d in sorted(longd, reverse=True)[:20]:
        print(f"  LONG  {n:3d} {u} | {d}")

    print("\n=== DUP TITLES ===")
    for t, urls in titles.items():
        if len(urls) > 1 and t:
            print(len(urls), t, urls)

    print("\n=== DUP DESCS ===")
    for d, urls in descs.items():
        if len(urls) > 1 and d:
            print(len(urls), d[:80], urls)

    print("\n=== MISSING DESC ===")
    for u in missing_desc:
        print(u)

    print("\n=== MISSING CANONICAL (first 80) ===")
    for u in missing_canonical[:80]:
        print(u)
    print("... total", len(missing_canonical))

    print("\n=== BROKEN PAGE LINKS ===")
    page_targets = Counter(h for _, h in broken["page"])
    print("broken page href instances", len(broken["page"]), "unique", len(page_targets))
    for href, n in page_targets.most_common(40):
        print(f"  {n:3d} {href}")
    print("broken asset instances", len(broken["asset"]))
    asset_targets = Counter(h for _, h in broken["asset"])
    for href, n in asset_targets.most_common(20):
        print(f"  {n:3d} {href}")

    # image file sizes
    print("\n=== LARGE IMAGES (>400KB) ===")
    big = []
    for p in ROOT.rglob("*"):
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"} and p.is_file():
            sz = p.stat().st_size
            if sz >= 400_000:
                big.append((sz, p.relative_to(ROOT).as_posix()))
    for sz, rel in sorted(big, reverse=True)[:30]:
        print(f"  {sz/1_048_576:5.2f}MB {rel}")
    print("large count", len(big))

    # apostrophe-clipped descriptions: content=' ... ' with a raw apostrophe
    print("\n=== POSSIBLE APOSTROPHE CLIP ===")
    clip = []
    for p in html_files:
        t = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"""<meta\s+name=['\"]description['\"]\s+content='([^']*)'""", t)
        # if using single quotes and page contains we'd etc in nearby text, already captured
        m2 = re.search(r"""name=["']description["']\s+content='([^']{0,80})""", t)
        if m2 and "content='" in t[t.find("name=") : t.find("name=") + 400]:
            # check if description likely truncated: ends mid word without period
            pass
        if re.search(r"""name=["']description["']\s+content='[^']*(?:We'd|It's|don't|doesn't|can't|won't)""", t):
            clip.append(page_url(p.relative_to(ROOT)))
        # content="..." is fine with apostrophes
        msq = re.search(r"""<meta[^>]*name=["']description["'][^>]*content='([^']*)'""", t)
        if msq:
            clip.append((page_url(p.relative_to(ROOT)), msq.group(1)[:90]))
    print(clip[:30], "count", len(clip))

    print("\n=== OG URL TRAILING SLASH MISMATCH ===")
    mismatches = []
    for p in html_files:
        t = p.read_text(encoding="utf-8", errors="replace")
        cu = re.search(r'rel=["\']canonical["\']\s+href=["\']([^"\']+)', t)
        if not cu:
            cu = re.search(r'href=["\']([^"\']+)["\']\s+rel=["\']canonical["\']', t)
        ou = re.search(r'property=["\']og:url["\']\s+content=["\']([^"\']+)', t)
        if not ou:
            ou = re.search(r'content=["\']([^"\']+)["\']\s+property=["\']og:url["\']', t)
        if cu and ou and cu.group(1) != ou.group(1):
            mismatches.append((page_url(p.relative_to(ROOT)), cu.group(1), ou.group(1)))
        # homepage og:url without trailing slash
    print("canon vs og:url mismatches", len(mismatches))
    for item in mismatches[:20]:
        print(" ", item)

    print("\n=== HOME OG URL ===")
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    print(re.findall(r'og:url[^>]+', home))
    print(re.findall(r'rel="canonical"[^>]+', home))


if __name__ == "__main__":
    main()
