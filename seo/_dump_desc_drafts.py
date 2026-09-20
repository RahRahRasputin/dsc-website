from __future__ import annotations
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(r"D:\dsc-website\pages\wiki")
OUT = Path(r"D:\dsc-website\seo\_desc_drafts.json")


class Paras(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.in_p = False
        self.cur = []
        self.paras = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
        if tag == "p" and not self.skip:
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
        if self.in_p and not self.skip:
            self.cur.append(data)


def slug_url(p: Path) -> str:
    rel = p.relative_to(ROOT.parent).as_posix()
    return "/" + rel[: -len("index.html")]


def first_useful(paras: list[str]) -> str:
    skip_re = re.compile(
        r"^(title:|description:|tags:|aliases:|date:|author:|-+\s*$|The Problem[: ]|What This Silo|For the technical)",
        re.I,
    )
    for para in paras:
        if len(para) < 50:
            continue
        if skip_re.search(para):
            continue
        return para
    for para in paras:
        if len(para) >= 50:
            return para
    return paras[0] if paras else ""


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def draft(text: str) -> str:
    text = text.replace('"', "'").replace("\u201c", "'").replace("\u201d", "'")
    sents = sentences(text)
    if not sents:
        return ""

    def ok(s: str) -> bool:
        return 70 <= len(s) <= 160 and s[-1] in ".!?"

    s0 = sents[0]
    if ok(s0):
        return s0
    if len(s0) < 70:
        acc = s0
        for s in sents[1:]:
            nxt = acc + " " + s
            if len(nxt) > 160:
                # append a clause of s
                rest = s.rstrip(".")
                for sep in ("; ", " — ", " – ", ", "):
                    i = rest.find(sep)
                    if i != -1:
                        cand = acc + " " + rest[:i].rstrip() + "."
                        if ok(cand):
                            return cand
                break
            acc = nxt
            if ok(acc):
                return acc
        if acc[-1] not in ".!?":
            acc = acc.rstrip(" ,;:—–") + "."
        return acc
    # s0 too long
    cut = s0[:157]
    for sep in (" — ", " – ", "; ", ": ", ", "):
        i = cut.rfind(sep)
        if i >= 68:
            out = cut[:i].rstrip(" ,;:—–") + "."
            if 70 <= len(out) <= 160:
                return out
    i = cut.rfind(" ")
    out = cut[:i].rstrip(" ,;:—–") + "."
    return out


rows = []
for p in sorted(ROOT.rglob("index.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    url = slug_url(p)
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', t)
    desc = m.group(1) if m else ""
    truncated = bool(desc) and desc[-1] not in ".!?…"
    missing = not desc
    if not missing and not truncated:
        continue
    parser = Paras()
    parser.feed(t)
    src = first_useful(parser.paras)
    d = draft(src)
    title_m = re.search(r"<title>(.*?)</title>", t, re.S)
    title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else ""
    rows.append(
        {
            "url": url,
            "kind": "missing" if missing else "truncated",
            "title": title,
            "draft": d,
            "draft_len": len(d),
            "ok": 70 <= len(d) <= 160 and '"' not in d and d.endswith((".", "!", "?")),
            "src": src[:280],
        }
    )

OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
print("wrote", len(rows), "ok", sum(1 for r in rows if r["ok"]), "bad", sum(1 for r in rows if not r["ok"]))
for r in rows:
    if not r["ok"]:
        print("BAD", r["draft_len"], r["url"], r["draft"])
