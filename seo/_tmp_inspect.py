from pathlib import Path
import re
p = Path(r"D:\dsc-website\pages\wiki\living-process\kv-cache\index.html")
t = p.read_text(encoding="utf-8-sig")
# title
m = re.search(r"<title>(.*?)</title>", t)
print("TITLE:", m.group(1))
print("title len", len(m.group(1)))
# first few paragraphs under Technical Core
sec = re.search(r"Technical Core(.*?)(?:<h2|<section|$)", t, re.S|re.I)
if sec:
    ps = re.findall(r"<p[^>]*>(.*?)</p>", sec.group(1), re.S)
    for i, para in enumerate(ps[:4]):
        text = re.sub(r"<[^>]+>", "", para)
        text = re.sub(r"\s+", " ", text).strip()
        print(f"---P{i+1} ({len(text)})---")
        print(text[:350])
# check robots / newline style
print("CRLF", "\r\n" in t[:500])
print("BOM", p.read_bytes()[:3] == b"\xef\xbb\xbf")
