import re
from pathlib import Path

ROOT = Path(r"D:\dsc-website\pages")
skip = {ROOT / "fieldguide" / "index.html", ROOT / "splash.html"}
missing = []
for p in sorted(ROOT.rglob("*.html")):
    if p in skip:
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    rel = p.relative_to(ROOT).as_posix()
    head = t[t.find("<head>") : t.find("</head>") + 7]
    if head.find("<head>") == -1:
        head = t[t.lower().find("<head") : t.lower().find("</head>") + 7]
    issues = []
    if 'name="robots" content="noindex, nofollow"' not in head:
        issues.append("robots")
    if 'name="description"' not in head:
        issues.append("desc")
    if 'rel="canonical"' not in head:
        issues.append("canon")
    if 'property="og:title"' not in head:
        issues.append("og:title")
    if 'property="og:url"' not in head:
        issues.append("og:url")
    if 'name="og:title"' in head:
        issues.append("name-og")
    n_desc = head.count('name="description"')
    if n_desc != 1:
        issues.append(f"desc_n={n_desc}")
    if issues:
        missing.append((rel, issues))
print("html", len(list(ROOT.rglob("*.html"))))
print("issues", len(missing))
for item in missing:
    print(item)
