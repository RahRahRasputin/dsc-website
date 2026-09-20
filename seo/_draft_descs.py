"""Draft 70-160 char descriptions from Technical Core / silo intro."""
from __future__ import annotations
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(r"D:\dsc-website\pages\wiki")


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
        r"^(title:|description:|tags:|aliases:|date:|author:|-|The Problem[: ]|What This Silo)",
        re.I,
    )
    for para in paras:
        if len(para) < 40:
            continue
        if skip_re.search(para):
            continue
        if para.startswith('"') and len(para) < 120:
            continue
        return para
    return paras[0] if paras else ""


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def draft(text: str) -> str:
    text = text.replace('"', "'")
    sents = sentences(text)
    if not sents:
        return ""
    acc = sents[0]
    if 70 <= len(acc) <= 160:
        return acc
    if len(acc) < 70:
        for s in sents[1:]:
            nxt = acc + " " + s
            if len(nxt) > 160:
                break
            acc = nxt
            if len(acc) >= 70:
                return acc
        return acc  # may still be short
    # too long: cut at last comma/semicolon/emdash/space before 157
    cut = acc[:157]
    for sep in (" — ", " – ", "; ", ", "):
        i = cut.rfind(sep)
        if i >= 70:
            out = cut[: i].rstrip(" ,;:—–") + "."
            return out
    i = cut.rfind(" ")
    if i >= 70:
        return cut[:i].rstrip(" ,;:—–") + "."
    return cut.rstrip() + "."


need = []
for p in sorted(ROOT.rglob("index.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    url = slug_url(p)
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', t)
    desc = m.group(1) if m else ""
    truncated = bool(desc) and (
        (len(desc) == 160 and desc[-1] not in ".!?")
        or (desc and desc[-1] not in ".!?…—–" and len(desc) <= 160)
    )
    missing = not desc
    if not missing and not truncated:
        continue
    parser = Paras()
    parser.feed(t)
    src = first_useful(parser.paras)
    d = draft(src)
    need.append((url, "MISS" if missing else "TRUNC", len(d), d, src[:180]))

print("to write", len(need))
for url, kind, n, d, src in need:
    flag = "OK" if 70 <= n <= 160 and '"' not in d else "BAD"
    print(f"\n{kind} {flag} {n:3} {url}")
    print("  DESC", d)
    if flag == "BAD":
        print("  SRC ", src)
