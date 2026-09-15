from pathlib import Path
import re

p = Path(r"D:\dsc-website\pages\wiki\living-process\positional-encoding\index.html")
raw = p.read_bytes()
has_bom = raw.startswith(b"\xef\xbb\xbf")
t = raw.decode("utf-8-sig")

m_title = re.search(r"<title>(.*?)</title>", t)
title = m_title.group(1)
print("title len", len(title))
print("title:", title)

desc = (
    "Attention Mechanisms process all tokens in parallel, but attention is "
    "order-blind by default. Positional encoding adds order information to token embeddings."
)
print("desc len", len(desc))
print("desc:", desc)
assert 70 <= len(desc) <= 160, len(desc)
assert 'name="description"' not in t
assert "name='description'" not in t
assert '"' not in desc

pat = (
    r'(  <meta name="robots" content="noindex, nofollow">\r?\n)'
    r'(  <title>' + re.escape(title) + r'</title>)'
)
m = re.search(pat, t)
if not m:
    raise SystemExit("anchor not found")

nl = "\n" if "\r\n" not in m.group(0) else "\r\n"
url = "https://digitalsoulcraft.org/wiki/living-process/positional-encoding/"
insert = (
    m.group(1)
    + f'  <meta name="description" content="{desc}">{nl}'
    + f'  <link rel="canonical" href="{url}">{nl}'
    + f'  <meta property="og:title" content="{title}">{nl}'
    + f'  <meta property="og:description" content="{desc}">{nl}'
    + f'  <meta property="og:url" content="{url}">{nl}'
    + m.group(2)
)
t2 = t[: m.start()] + insert + t[m.end() :]
assert 'name="robots" content="noindex, nofollow"' in t2
body1 = re.search(r"<body.*", t, re.S).group(0)
body2 = re.search(r"<body.*", t2, re.S).group(0)
assert body1 == body2

out = t2.encode("utf-8")
if has_bom:
    out = b"\xef\xbb\xbf" + out
p.write_bytes(out)
print("patched ok")

head = t2[t2.find("<head>") : t2.find("</head>") + 7]
cut = head.find('<link rel="stylesheet"')
print("---HEAD---")
print(head[:cut] if cut != -1 else head[:900])

log = Path(r"D:\dsc-website\seo\ONPAGE-LOG.md")
text = log.read_text(encoding="utf-8")
slug = "**/wiki/living-process/positional-encoding/**"
entry = f"""
- {slug} (`pages/wiki/living-process/positional-encoding/index.html`)
  - Added meta description from Technical Core first paragraph (~{len(desc)} chars)
  - Added absolute canonical + matching og:url (`{url}`)
  - Added og:title / og:description (title unchanged; robots noindex,nofollow kept)
  - Why: missing meta description (priority a); also lacked canonical/og:url
  - Run: Tuesday 15 Sep 2026, early afternoon ~1:21pm NZST / Pacific/Auckland
"""
if slug in text:
    raise SystemExit("already logged")
marker = "## 2026-09-15 (Tue) NZ"
if marker not in text:
    text = text.rstrip() + "\n\n" + marker + "\n" + entry
else:
    text = text.rstrip() + "\n" + entry
log.write_text(text + "\n", encoding="utf-8")
print("logged")
