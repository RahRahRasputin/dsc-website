from __future__ import annotations
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(r"D:\dsc-website\pages")


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []
        self.in_p = False
        self.paras: list[str] = []
        self.cur: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "p" and self.skip == 0:
            self.in_p = True
            self.cur = []

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if tag == "p" and self.in_p:
            text = re.sub(r"\s+", " ", "".join(self.cur)).strip()
            if text:
                self.paras.append(text)
            self.in_p = False

    def handle_data(self, data):
        if self.in_p and self.skip == 0:
            self.cur.append(data)


def page_url(rel: Path) -> str:
    posix = rel.as_posix()
    if posix.endswith("/index.html"):
        return "/" + posix[: -len("index.html")]
    return "/" + posix


rows = []
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(encoding="utf-8-sig", errors="replace")
    has_desc = 'name="description"' in t or "name='description'" in t
    has_canon = "rel=\"canonical\"" in t or "rel='canonical'" in t
    has_og = 'property="og:title"' in t
    title_m = re.search(r"<title>(.*?)</title>", t, re.S)
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
    if has_desc and has_canon and has_og:
        continue
    parser = TextExtractor()
    parser.feed(t)
    first = parser.paras[0] if parser.paras else ""
    rel = p.relative_to(ROOT).as_posix()
    url = page_url(p.relative_to(ROOT))
    need = []
    if not has_desc:
        need.append("desc")
    if not has_canon:
        need.append("canon")
    if not has_og:
        need.append("og")
    rows.append((url, ",".join(need), len(first), title, first[:400]))

print("pages needing something", len(rows))
missing_desc = [r for r in rows if "desc" in r[1]]
print("missing desc", len(missing_desc))
print("\n=== MISSING DESC ===")
for url, need, n, title, first in missing_desc:
    print(f"\nURL {url}")
    print(f"TITLE {title}")
    print(f"NEED {need} FIRSTLEN {n}")
    print(f"FIRST {first}")

print("\n=== HAS DESC, MISSING CANON/OG (wiki only, count) ===")
wiki_canon = [r for r in rows if r[0].startswith("/wiki/") and "desc" not in r[1]]
print(len(wiki_canon))
for url, need, n, title, first in wiki_canon[:15]:
    print(url, need, title[:70])
