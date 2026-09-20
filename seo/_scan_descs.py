import re
from pathlib import Path
ROOT = Path(r"D:\dsc-website\pages")
for p in sorted(ROOT.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', t)
    if not m:
        continue
    d = m.group(1)
    url = "/" + p.relative_to(ROOT).as_posix().replace("/index.html", "/").replace("index.html", "")
    flags = []
    if len(d) < 70:
        flags.append("SHORT")
    if len(d) > 160:
        flags.append("LONG")
    if d and d[-1] not in ".!?…—–":
        flags.append("NOEND")
    if d.endswith(" o") or d.endswith(" a") or d.endswith(" the") or d.endswith(" of"):
        flags.append("CUT")
    if flags:
        print(f"{','.join(flags):12} {len(d):3} {url} | {d[-40:]}")
