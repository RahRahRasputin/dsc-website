from pathlib import Path

p = Path(r"D:/dsc-website/pages/wiki/alignment/fine-tuning/index.html")
t = p.read_text(encoding="utf-8")
head = t[t.find("<head>") : t.find("</head>") + 7]
checks = [
    'name="description"',
    'rel="canonical"',
    'property="og:title"',
    'property="og:description"',
    'property="og:url"',
    'name="robots" content="noindex, nofollow"',
    "https://digitalsoulcraft.org/wiki/alignment/fine-tuning/",
]
for c in checks:
    print(("OK" if c in head else "MISSING"), c)

# show first part of head without style
cut = head.find("<link rel=\"stylesheet\"")
print("---HEAD---")
print(head[:cut] if cut != -1 else head[:800])

log = Path(r"D:/dsc-website/seo/ONPAGE-LOG.md")
text = log.read_text(encoding="utf-8")
entry = """
- **/wiki/alignment/fine-tuning/** (`pages/wiki/alignment/fine-tuning/index.html`)
  - Added meta description from Technical Core first paragraph (~129 chars)
  - Added absolute canonical + matching og:url (`https://digitalsoulcraft.org/wiki/alignment/fine-tuning/`)
  - Added og:title / og:description (title unchanged; robots noindex,nofollow kept)
  - Why: missing meta description (priority a); also lacked canonical/og:url
  - Run: Thursday 3 Sep 2026, afternoon ~1:17pm NZST / Pacific/Auckland
"""
if "**/wiki/alignment/fine-tuning/**" in text:
    print("already logged")
else:
    log.write_text(text.rstrip() + "\n" + entry, encoding="utf-8")
    print("log ok")
