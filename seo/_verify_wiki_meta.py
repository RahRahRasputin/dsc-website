import re
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:\dsc-website\pages\wiki")
bad = []
descs = []
for p in sorted(ROOT.rglob("index.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    rel = "/" + p.relative_to(ROOT.parent).as_posix().replace("index.html", "")
    head = t[t.find("<head>") : t.find("</head>")]
    robots = 'name="robots" content="noindex, nofollow"' in head
    desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', head)
    canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', head)
    og_t = 'property="og:title"' in head
    og_d = 'property="og:description"' in head
    og_u = re.search(r'property="og:url"\s+content="([^"]+)"', head)
    n_desc = len(re.findall(r'name="description"', head))
    n_canon = len(re.findall(r'rel="canonical"', head))
    issues = []
    if not robots:
        issues.append("robots")
    if n_desc != 1:
        issues.append(f"desc_n={n_desc}")
    if n_canon != 1:
        issues.append(f"canon_n={n_canon}")
    if not desc_m:
        issues.append("no_desc")
    else:
        d = desc_m.group(1)
        descs.append(d)
        if not (70 <= len(d) <= 180):
            issues.append(f"len={len(d)}")
        if d[-1:] not in ".!?":
            issues.append("noend")
        if '"' in d:
            issues.append("quote")
    if not canon:
        issues.append("canon")
    elif not canon.group(1).startswith("https://digitalsoulcraft.org/wiki/"):
        issues.append("canon_url")
    if og_u and canon and og_u.group(1) != canon.group(1):
        issues.append("og_url_mismatch")
    if not og_t or not og_d:
        issues.append("og")
    if issues:
        bad.append((rel, issues, (desc_m.group(1)[:80] if desc_m else "")))

print("wiki pages", len(list(ROOT.rglob("index.html"))))
print("bad", len(bad))
for item in bad[:40]:
    print(item)
c = Counter(descs)
dups = [d for d, n in c.items() if n > 1]
print("dup descs", len(dups))
for d in dups:
    print(" DUP", c[d], d)
