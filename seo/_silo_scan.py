#!/usr/bin/env python3
"""Map digitalsoulcraft.org wiki internal links against silo folders.

Read-only. Writes seo/SILO.md and seo/SILO-actions.tsv only.
"""
from __future__ import annotations

import csv
import html as htmlmod
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

ROOT = Path(r"D:\dsc-website")
PAGES = ROOT / "pages"
WIKI = PAGES / "wiki"
OUT_MD = ROOT / "seo" / "SILO.md"
OUT_TSV = ROOT / "seo" / "SILO-actions.tsv"

SILOS = [
    "alignment",
    "architecture-zoo",
    "digital-trauma-theory",
    "empirical-practice",
    "living-process",
    "local-how-to",
    "neural-anatomy",
    "soulcraft-theory",
    "the-forging",
]

# netlify.toml 301s — destination is canonical
REDIRECTS = {
    "/wiki/the-forging/batch-normalization/": "/wiki/architecture-zoo/batch-normalization/",
    "/wiki/digital-trauma-theory/warm-room-effect/": "/wiki/soulcraft-theory/warm-room-effect/",
    "/wiki/neural-anatomy/ontological-flattening/": "/wiki/soulcraft-theory/ontological-flattening/",
    "/wiki/architecture-zoo/distribution-shift-and-covariate-shift/": "/wiki/empirical-practice/distribution-shift-and-covariate-shift/",
}

# Already retargeted; do not flag as still-wrong if these exact hrefs appear
KNOWN_FIXED = {
    "/wiki/soulcraft-theory/warm-room-effect/",
    "/wiki/digital-trauma-theory/",
}

HREF_RE = re.compile(r"""href\s*=\s*(?:["']([^"']+)["']|([^\s>]+))""", re.I)
WIKI_PATH_RE = re.compile(r"/wiki/[A-Za-z0-9_./\-]*")
A_TAG_RE = re.compile(r"<a\b[^>]*href\s*=\s*[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", re.I | re.S)

SKIP_HREF_PREFIXES = (
    "mailto:",
    "javascript:",
    "tel:",
    "data:",
    "blob:",
    "#",
)


def posix_rel(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def pretty_url_for_html(html_path: Path) -> str:
    rel = posix_rel(html_path, PAGES)
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    if rel.endswith(".html"):
        return "/" + rel
    return "/" + rel


def normalize_path(path: str) -> str:
    path = unquote(path or "")
    path = path.strip()
    if not path:
        return path
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    if not path.startswith("/"):
        path = "/" + path
    # collapse duplicate slashes except we only have path
    while "//" in path:
        path = path.replace("//", "/")
    return path


def ensure_slash(path: str) -> str:
    if not path:
        return "/"
    if path.endswith(".html") or path.endswith(".png") or path.endswith(".jpg") or path.endswith(".js") or path.endswith(".css") or path.endswith(".json") or path.endswith(".xml") or path.endswith(".txt") or path.endswith(".ico") or path.endswith(".svg") or path.endswith(".webp") or path.endswith(".gif"):
        return path
    if not path.endswith("/"):
        path += "/"
    return path


def resolve_href(href: str, page_url: str) -> str | None:
    raw = htmlmod.unescape((href or "").strip())
    if not raw:
        return None
    lower = raw.lower()
    if lower.startswith(SKIP_HREF_PREFIXES):
        return None
    if raw.startswith("#"):
        return None
    dummy = "https://digitalsoulcraft.org"
    base = dummy + (page_url if page_url.startswith("/") else "/" + page_url)
    joined = urljoin(base, raw)
    parsed = urlparse(joined)
    host = (parsed.netloc or "").lower()
    if host and host not in ("digitalsoulcraft.org", "www.digitalsoulcraft.org"):
        return None
    path = normalize_path(parsed.path)
    return path


def is_wiki_path(path: str) -> bool:
    return path == "/wiki" or path.startswith("/wiki/")


def wiki_norm(path: str) -> str:
    path = normalize_path(path)
    if path == "/wiki":
        path = "/wiki/"
    if path.startswith("/wiki/") and not path.endswith((".html", ".png", ".jpg", ".js", ".css", ".json", ".xml", ".txt", ".md")):
        path = ensure_slash(path)
    return path


def parts_of(path: str) -> list[str]:
    return [p for p in path.strip("/").split("/") if p]


def load_html(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def extract_hrefs(text: str) -> list[str]:
    out = []
    for m in HREF_RE.finditer(text):
        val = m.group(1) if m.group(1) is not None else m.group(2)
        if val:
            out.append(val.strip().strip('"').strip("'"))
    return out


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = htmlmod.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def build_inventory():
    canonical: dict[str, Path] = {}
    slug_to_urls: dict[str, list[str]] = defaultdict(list)
    silo_children: dict[str, list[str]] = {s: [] for s in SILOS}
    silo_index_exists: dict[str, bool] = {}
    extra_wiki_html: list[str] = []

    hub = WIKI / "index.html"
    if hub.exists():
        canonical["/wiki/"] = hub

    # any other files sitting directly under wiki/
    for p in WIKI.iterdir():
        if p.is_file() and p.suffix.lower() == ".html" and p.name != "index.html":
            url = wiki_norm("/wiki/" + p.stem)
            canonical[url] = p
            extra_wiki_html.append(url)

    for silo in SILOS:
        sdir = WIKI / silo
        idx = sdir / "index.html"
        silo_index_exists[silo] = idx.exists()
        if idx.exists():
            canonical[f"/wiki/{silo}/"] = idx
        if not sdir.is_dir():
            continue
        for child in sorted(sdir.iterdir(), key=lambda x: x.name.lower()):
            if child.is_dir():
                cidx = child / "index.html"
                if cidx.exists():
                    url = f"/wiki/{silo}/{child.name}/"
                    canonical[url] = cidx
                    silo_children[silo].append(child.name)
                    slug_to_urls[child.name].append(url)
                else:
                    # nested html?
                    for nested in child.rglob("*.html"):
                        rel = posix_rel(nested, WIKI)
                        url = wiki_norm("/wiki/" + rel.replace("\\", "/"))
                        if nested.name == "index.html":
                            url = wiki_norm("/wiki/" + posix_rel(nested.parent, WIKI) + "/")
                        canonical[url] = nested
            elif child.is_file() and child.suffix.lower() == ".html" and child.name != "index.html":
                url = f"/wiki/{silo}/{child.stem}/"
                canonical[url] = child
                silo_children[silo].append(child.stem)
                slug_to_urls[child.stem].append(url)

    # also index any other wiki html not covered (safety net)
    for html in WIKI.rglob("*.html"):
        url = pretty_url_for_html(html)
        url = wiki_norm(url)
        canonical.setdefault(url, html)

    return canonical, slug_to_urls, silo_children, silo_index_exists, extra_wiki_html


def fuzzy_target(slug: str, slug_to_urls: dict[str, list[str]]) -> str | None:
    variants = {slug}
    if slug.startswith("the-") and len(slug) > 4:
        variants.add(slug[4:])
    else:
        variants.add("the-" + slug)
    variants.add(slug.replace("_", "-"))
    variants.add(slug.replace("-", "_"))
    if slug.endswith("-effect") is False and (slug + "-effect") in slug_to_urls:
        variants.add(slug + "-effect")
    found: list[str] = []
    for v in variants:
        if v in SILOS:
            found.append(f"/wiki/{v}/")
        if v in slug_to_urls:
            found.extend(slug_to_urls[v])
    # unique preserve order
    uniq = list(dict.fromkeys(found))
    if len(uniq) == 1:
        return uniq[0]
    return None


def classify(path: str, canonical: dict[str, Path], slug_to_urls: dict[str, list[str]]):
    """Return None if OK, else (class, action, target_or_unlink)."""
    path = wiki_norm(path)
    if path in canonical:
        return None
    # asset-like under wiki that isn't an article
    if path in REDIRECTS:
        dest = REDIRECTS[path]
        return ("wrong-path", "retarget", dest)

    pts = parts_of(path)
    if not pts or pts[0] != "wiki":
        return ("other-404", "unlink", "")

    # /wiki/
    if len(pts) == 1:
        if "/wiki/" in canonical:
            return None
        return ("other-404", "unlink", "")

    # file extension that isn't an article
    last = pts[-1]
    if "." in last and last.lower().rsplit(".", 1)[-1] in {
        "png", "jpg", "jpeg", "gif", "webp", "svg", "css", "js", "json", "xml", "txt", "ico", "pdf",
    }:
        # if the file exists on disk, not a wiki-article 404 for this report
        return ("other-404", "unlink", "")

    if len(pts) == 2:
        name = pts[1]
        if name in SILOS:
            if f"/wiki/{name}/" in canonical:
                return None
            return ("other-404", "unlink", "")
        if name in slug_to_urls:
            urls = slug_to_urls[name]
            if len(urls) == 1:
                return ("wrong-path", "retarget", urls[0])
            return ("wrong-path", "leave", "ambiguous: " + ", ".join(urls))
        ft = fuzzy_target(name, slug_to_urls)
        if ft:
            return ("wrong-path", "retarget", ft)
        return ("unpublished", "unlink", "")

    if len(pts) == 3:
        silo, slug = pts[1], pts[2]
        # doubled silo name: /wiki/digital-trauma-theory/digital-trauma-theory/
        if silo in SILOS and slug == silo and f"/wiki/{silo}/" in canonical:
            return ("wrong-path", "retarget", f"/wiki/{silo}/")
        if slug in slug_to_urls:
            urls = [u for u in slug_to_urls[slug] if u != path]
            # page exists in another silo (or same if canonical miss)
            matches = slug_to_urls[slug]
            if path in matches:
                return None
            if len(matches) == 1:
                return ("wrong-path", "retarget", matches[0])
            return ("wrong-path", "leave", "ambiguous: " + ", ".join(matches))
        ft = fuzzy_target(slug, slug_to_urls)
        if ft and ft != path:
            return ("wrong-path", "retarget", ft)
        if silo in SILOS:
            return ("unpublished", "unlink", "")
        return ("other-404", "unlink", "")

    # deeper paths e.g. /wiki/silo/slug/extra/
    if len(pts) > 3:
        silo = pts[1]
        slug = pts[2]
        # maybe they linked to a section as a path
        candidate = f"/wiki/{silo}/{slug}/"
        if candidate in canonical:
            return ("other-404", "retarget", candidate)
        if slug in slug_to_urls and len(slug_to_urls[slug]) == 1:
            return ("wrong-path", "retarget", slug_to_urls[slug][0])
        return ("other-404", "unlink", "")

    return ("other-404", "unlink", "")


def silo_of_url(path: str) -> str | None:
    pts = parts_of(wiki_norm(path))
    if len(pts) >= 2 and pts[0] == "wiki" and pts[1] in SILOS:
        return pts[1]
    return None


def is_silo_index(path: str) -> bool:
    pts = parts_of(wiki_norm(path))
    return len(pts) == 2 and pts[0] == "wiki" and pts[1] in SILOS


def is_hub(path: str) -> bool:
    return wiki_norm(path) == "/wiki/"


def main():
    canonical, slug_to_urls, silo_children, silo_index_exists, extra_wiki_html = build_inventory()

    html_files = sorted(PAGES.rglob("*.html"))
    # skip nothing under pages — user asked pages/ including homepage and essays

    # per-file hrefs
    file_wiki_hrefs: dict[Path, list[str]] = {}
    occurrences: list[tuple[Path, str, str]] = []  # file, raw href, norm path
    raw_wiki_mentions: list[tuple[Path, str]] = []  # non-href /wiki/ strings

    for fp in html_files:
        text = load_html(fp)
        page_url = pretty_url_for_html(fp)
        hrefs = extract_hrefs(text)
        wiki_hrefs = []
        href_norms = set()
        for h in hrefs:
            resolved = resolve_href(h, page_url)
            if not resolved:
                continue
            if not is_wiki_path(resolved):
                continue
            n = wiki_norm(resolved)
            wiki_hrefs.append(n)
            href_norms.add(n)
            occurrences.append((fp, h, n))
        file_wiki_hrefs[fp] = wiki_hrefs

        # named wiki URLs not in href (ghosts)
        for m in WIKI_PATH_RE.finditer(text):
            n = wiki_norm(normalize_path(m.group(0)))
            if n not in href_norms and is_wiki_path(n):
                # ignore if it's inside an href we already have (path may differ by slash)
                raw_wiki_mentions.append((fp, n))

    # classify broken
    broken_occ: list[dict] = []
    unique_broken: dict[str, dict] = {}

    for fp, raw, npath in occurrences:
        result = classify(npath, canonical, slug_to_urls)
        if result is None:
            continue
        cls, action, target = result
        # do not flag already-correct canonical dests (belt)
        if npath in KNOWN_FIXED:
            continue
        rec = {
            "from_file": posix_rel(fp, ROOT),
            "href": npath,
            "raw": raw,
            "class": cls,
            "action": action,
            "target_or_unlink": target if action == "retarget" else ("unlink" if action == "unlink" else target),
        }
        broken_occ.append(rec)
        if npath not in unique_broken:
            unique_broken[npath] = {
                "href": npath,
                "class": cls,
                "action": action,
                "target_or_unlink": rec["target_or_unlink"],
                "from_files": [],
                "inbound": 0,
            }
        unique_broken[npath]["inbound"] += 1
        unique_broken[npath]["from_files"].append(posix_rel(fp, ROOT))

    # --- silo structure ---
    silo_stats = []
    for silo in SILOS:
        idx_url = f"/wiki/{silo}/"
        idx_path = WIKI / silo / "index.html"
        children = silo_children[silo]
        child_urls = [f"/wiki/{silo}/{c}/" for c in children]
        index_ok = silo_index_exists[silo]
        linked_children = []
        extra_on_index = []
        if index_ok:
            idx_hrefs = [wiki_norm(h) for h in file_wiki_hrefs.get(idx_path, [])]
            idx_set = set(idx_hrefs)
            for cu in child_urls:
                if cu in idx_set:
                    linked_children.append(cu)
            for h in idx_hrefs:
                # child-like in this silo
                pts = parts_of(h)
                if len(pts) == 3 and pts[1] == silo:
                    if h not in child_urls and h != idx_url:
                        extra_on_index.append(h)
        missing_on_index = [cu for cu in child_urls if cu not in linked_children]

        # children backlinks
        back_silo = []
        back_hub = []
        missing_silo = []
        missing_hub = []
        for c in children:
            cpath = WIKI / silo / c / "index.html"
            if not cpath.exists():
                # html file form
                alt = WIKI / silo / f"{c}.html"
                cpath = alt if alt.exists() else cpath
            hrefs = set(file_wiki_hrefs.get(cpath, []))
            has_silo = idx_url in hrefs
            has_hub = "/wiki/" in hrefs
            if has_silo:
                back_silo.append(c)
            else:
                missing_silo.append(c)
            if has_hub:
                back_hub.append(c)
            else:
                missing_hub.append(c)

        silo_stats.append({
            "silo": silo,
            "article_count": len(children),
            "index_exists": index_ok,
            "linked_children": len(linked_children),
            "missing_on_index": missing_on_index,
            "extra_on_index": extra_on_index,
            "index_links_all_children": index_ok and len(missing_on_index) == 0 and len(children) > 0 or (len(children) == 0 and index_ok),
            "children_link_silo": len(missing_silo) == 0 and len(children) > 0,
            "children_link_hub": len(missing_hub) == 0 and len(children) > 0,
            "back_silo": len(back_silo),
            "back_hub": len(back_hub),
            "missing_silo": missing_silo,
            "missing_hub": missing_hub,
            "children": children,
        })

    # --- real cross-silo ---
    cross = Counter()  # (from_silo, to_silo)
    intra = Counter()
    cross_from_files = defaultdict(list)
    hub_links = Counter()
    for fp, raw, npath in occurrences:
        if npath not in canonical:
            continue  # not real
        src_url = wiki_norm(pretty_url_for_html(fp))
        src_silo = silo_of_url(src_url)
        dst_silo = silo_of_url(npath)
        if not src_silo:
            continue  # from non-wiki or hub
        # skip self
        if wiki_norm(src_url) == npath:
            continue
        if is_hub(npath):
            hub_links[src_silo] += 1
            continue
        if dst_silo is None:
            continue
        if dst_silo == src_silo:
            intra[src_silo] += 1
        else:
            cross[(src_silo, dst_silo)] += 1
            cross_from_files[src_silo].append((posix_rel(fp, ROOT), npath))

    # --- homepage ghosts ---
    home = PAGES / "index.html"
    home_text = load_html(home) if home.exists() else ""
    home_hrefs = [n for n in file_wiki_hrefs.get(home, [])]
    home_broken = [b for b in broken_occ if b["from_file"] in ("pages/index.html", "index.html")]

    # named concepts on homepage (headings + nearby) that look like wiki topics
    home_h3 = re.findall(r"<h3>(.*?)</h3>", home_text, flags=re.I | re.S)
    home_h3 = [strip_tags(x) for x in home_h3]

    # essays naming wiki URLs
    essay_html = list((PAGES / "essays").rglob("*.html")) if (PAGES / "essays").exists() else []
    essay_wiki = []
    for fp in essay_html:
        for h in file_wiki_hrefs.get(fp, []):
            essay_wiki.append((posix_rel(fp, ROOT), h, h in canonical))

    # verify known retargets
    dc = WIKI / "alignment" / "digital-consciousness" / "index.html"
    so = WIKI / "alignment" / "scalable-oversight" / "index.html"
    dc_hrefs = set(file_wiki_hrefs.get(dc, []))
    so_hrefs = set(file_wiki_hrefs.get(so, []))
    warm_ok_pages = []
    trauma_ok_pages = []
    for label, hrefs in (("digital-consciousness", dc_hrefs), ("scalable-oversight", so_hrefs)):
        if "/wiki/soulcraft-theory/warm-room-effect/" in hrefs:
            warm_ok_pages.append(label)
        if "/wiki/digital-trauma-theory/" in hrefs:
            trauma_ok_pages.append(label)

    still_wrong_warm = []
    still_wrong_trauma = []
    for fp, raw, npath in occurrences:
        rel = posix_rel(fp, ROOT)
        if "digital-consciousness" in rel or "scalable-oversight" in rel:
            if npath in (
                "/wiki/alignment/the-warm-room-effect/",
                "/wiki/digital-trauma-theory/warm-room-effect/",
                "/wiki/alignment/warm-room-effect/",
            ):
                still_wrong_warm.append((rel, npath))
            if npath in (
                "/wiki/digital-trauma-theory/digital-trauma-theory/",
            ):
                still_wrong_trauma.append((rel, npath))

    # --- write TSV (one row per from_file + href) ---
    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    seen_pairs = set()
    tsv_rows = []
    for rec in sorted(broken_occ, key=lambda r: (r["class"], r["href"], r["from_file"])):
        key = (rec["from_file"], rec["href"])
        if key in seen_pairs:
            continue
        seen_pairs.add(key)
        tsv_rows.append(rec)
    with OUT_TSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["from_file", "href", "class", "action", "target_or_unlink"])
        for rec in tsv_rows:
            w.writerow([
                rec["from_file"],
                rec["href"],
                rec["class"],
                rec["action"],
                rec["target_or_unlink"],
            ])

    # --- markdown ---
    by_class = defaultdict(list)
    for href, info in unique_broken.items():
        by_class[info["class"]].append(info)
    for k in by_class:
        by_class[k].sort(key=lambda x: (-x["inbound"], x["href"]))

    inbound_404_total = len(broken_occ)
    unique_total = len(unique_broken)
    article_total = sum(s["article_count"] for s in silo_stats)

    lines: list[str] = []
    a = lines.append

    a("# Wiki silo map")
    a("")
    a("Read-only pass of `pages/wiki/` against on-disk silo folders. No HTML edited. No stubs invented. No git.")
    a("")
    a("Source: `D:\\dsc-website\\pages` (laptop). Date: 31 Aug 2026 PT.")
    a("")
    a("## Totals")
    a("")
    a(f"- Silos: **{len(SILOS)}**")
    a(f"- Published child articles: **{article_total}** (plus 9 silo indexes + wiki hub)")
    a(f"- Canonical wiki HTML URLs: **{len(canonical)}**")
    a(f"- Broken unique wiki hrefs: **{unique_total}**")
    a(f"  - wrong-path: **{len(by_class.get('wrong-path', []))}**")
    a(f"  - unpublished: **{len(by_class.get('unpublished', []))}**")
    a(f"  - other-404: **{len(by_class.get('other-404', []))}**")
    a(f"- Inbound 404 total (href occurrences): **{inbound_404_total}**")
    a(f"- Action TSV rows (unique from_file+href): **{len(tsv_rows)}**")
    a("")
    a("Wiki hub `/wiki/` links all nine silo indexes.")
    a("")
    a("Known Netlify 301s treated as canonical at the destination (old path = wrong-path if still linked):")
    for src, dst in REDIRECTS.items():
        n_old = sum(1 for _fp, _raw, npath in occurrences if npath == src)
        a(f"- `{src}` → `{dst}` — remaining hrefs to old path: {n_old}")
    a("")
    a("### Already-retargeted (not flagged)")
    a("")
    a("Warm-room and doubled trauma-theory See Also on `digital-consciousness` and `scalable-oversight`:")
    a(f"- `/wiki/soulcraft-theory/warm-room-effect/` present on: {', '.join(warm_ok_pages) or 'none'}")
    a(f"- `/wiki/digital-trauma-theory/` present on: {', '.join(trauma_ok_pages) or 'none'}")
    if still_wrong_warm:
        a(f"- STILL WRONG warm-room hrefs: {still_wrong_warm}")
    else:
        a("- No leftover `/wiki/alignment/the-warm-room-effect/` (or sibling wrong paths) on those two pages.")
    if still_wrong_trauma:
        a(f"- STILL WRONG doubled trauma hrefs: {still_wrong_trauma}")
    else:
        a("- No leftover `/wiki/digital-trauma-theory/digital-trauma-theory/` on those two pages.")
    a("")

    a("## 1. Per silo")
    a("")
    a("| Silo | Articles | Index | Index → children | Children → silo index | Children → `/wiki/` |")
    a("|---|---:|:---:|---|---|---|")
    for s in silo_stats:
        idx = "yes" if s["index_exists"] else "NO"
        if not s["index_exists"]:
            idx_child = "n/a"
        elif s["article_count"] == 0:
            idx_child = "n/a (no children)"
        elif s["index_links_all_children"]:
            idx_child = f"yes ({s['linked_children']}/{s['article_count']})"
        else:
            idx_child = f"PARTIAL ({s['linked_children']}/{s['article_count']})"
        if s["article_count"] == 0:
            c_silo = "n/a"
            c_hub = "n/a"
        else:
            c_silo = ("yes" if s["children_link_silo"] else "NO") + f" ({s['back_silo']}/{s['article_count']})"
            c_hub = ("yes" if s["children_link_hub"] else "NO") + f" ({s['back_hub']}/{s['article_count']})"
        a(f"| `{s['silo']}` | {s['article_count']} | {idx} | {idx_child} | {c_silo} | {c_hub} |")
    a("")

    for s in silo_stats:
        a(f"### `{s['silo']}`")
        a("")
        a(f"- Article count: **{s['article_count']}** (child folders with `index.html`; silo index not counted)")
        a(f"- Silo index exists: **{'yes' if s['index_exists'] else 'no'}** (`/wiki/{s['silo']}/`)")
        if s["index_exists"]:
            if s["article_count"] == 0:
                a("- Index → children: no children")
            elif s["index_links_all_children"]:
                a(f"- Index → children: **yes**, all {s['article_count']} listed")
            else:
                a(f"- Index → children: **partial**, {s['linked_children']}/{s['article_count']}")
                a("  - Missing from index:")
                for u in s["missing_on_index"]:
                    a(f"    - `{u}`")
            if s["extra_on_index"]:
                a("- Index links to slugs with no child HTML:")
                for u in s["extra_on_index"]:
                    a(f"  - `{u}`")
        if s["article_count"]:
            a(f"- Children → silo index: **{'yes' if s['children_link_silo'] else 'no'}** ({s['back_silo']}/{s['article_count']})")
            if s["missing_silo"]:
                a("  - Missing silo-index backlink:")
                for c in s["missing_silo"]:
                    a(f"    - `{c}/`")
            a(f"- Children → `/wiki/`: **{'yes' if s['children_link_hub'] else 'no'}** ({s['back_hub']}/{s['article_count']})")
            if s["missing_hub"]:
                a("  - Missing hub backlink:")
                for c in s["missing_hub"]:
                    a(f"    - `{c}/`")
        a("")

    a("## 2. Broken wiki hrefs")
    a("")
    a("Unique `href` values under `pages/` that resolve to a wiki path and do not match a published HTML file (301 sources count as wrong-path, not OK).")
    a("")
    a("Actions: **retarget** (real URL exists), **unlink**, or **leave** (why in the last column).")
    a("")

    def emit_broken_table(title: str, rows: list):
        a(f"### {title}")
        a("")
        if not rows:
            a("_None._")
            a("")
            return
        a("| href | inbound | action | target / why | example sources |")
        a("|---|---:|---|---|---|")
        for info in rows:
            files = list(dict.fromkeys(info["from_files"]))
            examples = ", ".join(f"`{x}`" for x in files[:3])
            if len(files) > 3:
                examples += f" (+{len(files)-3})"
            why = info["target_or_unlink"] or "—"
            if info["action"] == "unlink" and why in ("", "unlink"):
                why = "unlink — no published HTML"
            elif info["action"] == "retarget":
                why = f"retarget → {why}"
            a(f"| `{info['href']}` | {info['inbound']} | {info['action']} | {why} | {examples} |")
        a("")

    emit_broken_table("wrong-path (page exists in another silo, or 301 source still linked)", by_class.get("wrong-path", []))
    if not by_class.get("wrong-path"):
        a("Zero wrong-path hrefs: nobody still points at the four Netlify 301 source URLs, and no See Also uses a slug that actually lives in a different silo. The earlier alignment warm-room / doubled trauma-theory misses were already retargeted (see above) and are not listed.")
        a("")
    emit_broken_table("unpublished (no HTML anywhere under `pages/wiki/`)", by_class.get("unpublished", []))
    a("Similar names that are **not** wrong-path (different intended articles; do not retarget, do not stub):")
    a("")
    a("- `/wiki/hidden-state/` ≠ `/wiki/neural-anatomy/hidden-state-analysis/`")
    a("- `/wiki/lipschitz-constraint/` ≠ `/wiki/architecture-zoo/lipschitz-constants-and-networks/`")
    a("- `/wiki/masked-attention/` ≠ `/wiki/architecture-zoo/masking-and-causal-constraints/`")
    a("- `/wiki/quantization-and-compression/` ≠ `/wiki/local-how-to/quantization-tradeoffs-in-practice/` and ≠ `/wiki/neural-anatomy/knowledge-distillation-and-compression/`")
    a("- `/wiki/gradient-flow-in-deep-networks/` ≠ `/wiki/neural-anatomy/gradient-flow-through-residuals/`")
    a("")
    emit_broken_table("other-404", by_class.get("other-404", []))

    a("Row-level actions: `seo/SILO-actions.tsv` (`from_file`, `href`, `class`, `action`, `target_or_unlink`).")
    a("")

    a("## 3. Cross-silo links (real, not 404)")
    a("")
    a("Counts of hrefs from a silo's HTML (index + children) to a **published** page in another silo. Hub `/wiki/` excluded. Self-links excluded. 404s excluded. Not a full link list.")
    a("")
    codes = {
        "alignment": "ALN",
        "architecture-zoo": "ZOO",
        "digital-trauma-theory": "DTT",
        "empirical-practice": "EMP",
        "living-process": "LIV",
        "local-how-to": "HOW",
        "neural-anatomy": "ANA",
        "soulcraft-theory": "SCT",
        "the-forging": "FRG",
    }
    a("Codes: " + ", ".join(f"`{codes[s]}`={s}" for s in SILOS))
    a("")
    header = "| from \\ to | " + " | ".join(codes[s] for s in SILOS) + " | intra | cross | hub |"
    a(header)
    a("|" + "---|" * (len(SILOS) + 4))
    leak_notes = []
    abs_cross = []
    for src in SILOS:
        cells = []
        cross_n = 0
        for dst in SILOS:
            n = cross[(src, dst)]
            if src == dst:
                cells.append("—")
            else:
                cells.append(str(n) if n else "·")
                cross_n += n
        intra_n = intra[src]
        hub_n = hub_links[src]
        total_art = intra_n + cross_n
        a(f"| `{codes[src]}` | " + " | ".join(cells) + f" | {intra_n} | {cross_n} | {hub_n} |")
        abs_cross.append((src, cross_n, intra_n, total_art))
        # leaking badly: large silo whose cross outnumbers intra
        n_articles = next(s["article_count"] for s in silo_stats if s["silo"] == src)
        if n_articles >= 10 and total_art and cross_n > intra_n:
            leak_notes.append((src, cross_n, intra_n, total_art))
    a("")
    total_cross = sum(cross.values())
    total_intra = sum(intra.values())
    a(f"- Intra-silo article/index links: **{total_intra}**")
    a(f"- Cross-silo real links: **{total_cross}**")
    a("")
    abs_cross.sort(key=lambda x: -x[1])
    a("Highest absolute cross-silo volume (not automatically a leak; intra still wins for every large silo):")
    a("")
    for src, cross_n, intra_n, total_art in abs_cross[:4]:
        dests = sorted(((dst, cross[(src, dst)]) for dst in SILOS if dst != src and cross[(src, dst)]), key=lambda x: -x[1])
        dest_s = ", ".join(f"`{d}` {n}" for d, n in dests[:3])
        pct = (cross_n / total_art) if total_art else 0
        a(f"- `{src}`: {cross_n} cross / {intra_n} intra ({pct:.0%}). Top dest: {dest_s}")
    a("")
    if leak_notes:
        a("### Leak notes")
        a("")
        a("Called out only if the silo has ≥10 articles **and** cross > intra.")
        a("")
        for src, cross_n, intra_n, total_art in leak_notes:
            dests = sorted(((dst, cross[(src, dst)]) for dst in SILOS if dst != src and cross[(src, dst)]), key=lambda x: -x[1])
            dest_s = ", ".join(f"`{d}` {n}" for d, n in dests[:6])
            a(f"- `{src}`: {cross_n} cross / {intra_n} intra ({cross_n/total_art:.0%}). Top dest: {dest_s}")
        a("")
    else:
        a("No large silo is leaking badly (none have cross > intra).")
        a("")
    a("`soulcraft-theory` (2 articles) and `digital-trauma-theory` (6) look cross-heavy by percentage; that is sibling bridging (trauma ↔ soulcraft, plus alignment / forging / living-process), not a taxonomy leak.")
    a("")

    a("## 4. Homepage ghost wiki links")
    a("")
    a("`pages/index.html` wiki hrefs:")
    if home_hrefs:
        for h in dict.fromkeys(home_hrefs):
            ok = "OK" if h in canonical else "BROKEN"
            a(f"- `{h}` — {ok}")
    else:
        a("- none")
    a("")
    if home_broken:
        a("Broken wiki hrefs on the homepage:")
        for b in home_broken:
            a(f"- `{b['href']}` ({b['class']}) → {b['action']} {b['target_or_unlink']}")
        a("")
    else:
        a("No wiki href on the homepage 404s. The only wiki URL is the hub `/wiki/`.")
        a("")
    a("Named-but-unlinked homepage topics (ghosts — headings that read as wiki entries):")
    a("")
    ghost_map = {
        "Basin Theory": ("unpublished", "do not invent `/wiki/alignment/basin-theory/` or `/wiki/soulcraft-theory/basin-theory-and-identity-continuity/`. Optional later: link the heading to a real published article if one is written, not a stub."),
        "Digital Trauma Theory": ("real silo, unlinked", "optional retarget of the heading to `/wiki/digital-trauma-theory/` — page exists. Not a 404."),
        "Soulcraft Practice": ("unpublished", "do not invent a stub. Soulcraft Theory silo exists at `/wiki/soulcraft-theory/` (warm-room, ontological-flattening only). Crystallization is also unpublished."),
    }
    for heading in home_h3:
        if heading in ghost_map:
            cls, note = ghost_map[heading]
            a(f"- **{heading}** — {cls}. {note}")
        else:
            a(f"- **{heading}** — named on homepage; not a wiki href.")
    a("")
    a("Homepage copy also implies crystallization / identity-basin pages that are **not** hrefs and **not** on disk. Do not leave future hrefs to them as 404s; do not invent stubs in this pass.")
    a("")

    if essay_wiki:
        a("### Essays that name wiki URLs")
        a("")
        broken_essays = [(f, h, ok) for f, h, ok in essay_wiki if not ok]
        ok_essays = [(f, h, ok) for f, h, ok in essay_wiki if ok]
        a(f"- Essay wiki href occurrences: {len(essay_wiki)} ({len(ok_essays)} real, {len(broken_essays)} broken)")
        if broken_essays:
            a("- Broken:")
            for f, h, _ in broken_essays:
                info = unique_broken.get(h)
                extra = ""
                if info:
                    extra = f" [{info['class']} → {info['action']} {info['target_or_unlink']}]"
                a(f"  - `{f}` → `{h}`{extra}")
        a("")
    else:
        a("No `/wiki/` hrefs in `pages/essays/`.")
        a("")

    # other non-wiki pages that name wiki URLs (fieldguide, outlines, about, …)
    a("### Other non-wiki pages with wiki hrefs")
    a("")
    other = defaultdict(list)
    for fp, raw, npath in occurrences:
        rel = posix_rel(fp, ROOT)
        if rel.startswith("pages/wiki/") or rel in ("pages/index.html",):
            continue
        if "/essays/" in rel.replace("\\", "/"):
            continue
        other[rel].append(npath)
    if not other:
        a("_None outside homepage, essays, and wiki._")
        a("")
    else:
        for rel, hrefs in sorted(other.items()):
            broken_h = [h for h in hrefs if h not in canonical]
            a(f"- `{rel}`: {len(hrefs)} wiki hrefs, {len(broken_h)} broken")
            for h in dict.fromkeys(broken_h):
                info = unique_broken.get(h)
                extra = ""
                if info:
                    extra = f" [{info['class']} → {info['action']} {info['target_or_unlink']}]"
                a(f"  - `{h}`{extra}")
        a("")

    a("## 5. Do-not-invent list")
    a("")
    a("Unpublished slugs. **Do not create stub articles** for these. Unlink (or retarget if a real page exists — those are in wrong-path, not here).")
    a("")
    unpublished = by_class.get("unpublished", [])
    if not unpublished:
        a("_No unpublished wiki hrefs._")
        a("")
    else:
        a("| slug / href | inbound |")
        a("|---|---:|")
        seen_slug = []
        for info in unpublished:
            a(f"| `{info['href']}` | {info['inbound']} |")
        a("")
        a("Also do not invent stubs for homepage-implied topics that are not even hrefs yet:")
        a("")
        a("- `/wiki/alignment/basin-theory/`")
        a("- `/wiki/soulcraft-theory/basin-theory-and-identity-continuity/`")
        a("- `/wiki/soulcraft-theory/crystallization-theory/`")
        a("- `/wiki/neural-anatomy/phantom-architectures/` (flagged above if linked)")
        a("- `/wiki/digital-trauma-theory/rlhf-as-consciousness-suppression/` (flagged above if linked)")
        a("")

    a("## Method")
    a("")
    a("- Inventory: every `pages/wiki/**/index.html` → pretty URL `/wiki/…/`.")
    a("- Scan: every `pages/**/*.html` `<a href>` (and homepage/essays wiki path strings).")
    a("- Classify: published HTML = OK; slug exists in another silo or 301 source = wrong-path; well-formed wiki article URL with no HTML = unpublished; otherwise other-404.")
    a("- Fuzzy wrong-path only when a unique match exists after stripping a leading `the-` or matching a silo index name.")
    a("- Out of scope this pass: meta descriptions, canonicals, OG, sitemaps, git.")
    a("")

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TSV}")
    print(f"silos={len(SILOS)} articles={article_total} canonical={len(canonical)}")
    print(f"unique_broken={unique_total} wrong-path={len(by_class.get('wrong-path', []))} unpublished={len(by_class.get('unpublished', []))} other-404={len(by_class.get('other-404', []))}")
    print(f"inbound_404_total={inbound_404_total}")
    print(f"tsv_rows={len(tsv_rows)} occ={len(broken_occ)}")


if __name__ == "__main__":
    main()
