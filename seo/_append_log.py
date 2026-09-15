from pathlib import Path

log = Path(r"D:/dsc-website/seo/ONPAGE-LOG.md")
text = log.read_text(encoding="utf-8")
entry = """
- **/wiki/architecture-zoo/** (`pages/wiki/architecture-zoo/index.html`)
  - Added meta description from silo intro paragraph (~143 chars)
  - Added absolute canonical + matching og:url (`https://digitalsoulcraft.org/wiki/architecture-zoo/`)
  - Added og:title / og:description (title unchanged; robots noindex,nofollow kept)
  - Why: missing meta description (priority a); also lacked canonical/og:url
  - Run: Tuesday 8 Sep 2026, early afternoon ~1:47pm NZST / Pacific/Auckland
"""
if "/wiki/architecture-zoo/" in text:
    raise SystemExit("already logged")
# append under today's section header if present
marker = "## 2026-09-08 (Tue) NZ"
if marker not in text:
    text = text.rstrip() + "\n\n" + marker + "\n" + entry
else:
    text = text.rstrip() + "\n" + entry
log.write_text(text + "\n", encoding="utf-8")
print("logged")
