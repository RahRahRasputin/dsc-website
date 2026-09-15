from pathlib import Path
root = Path(r"D:\dsc-website\pages")
missing = []
for p in sorted(root.rglob("*.html")):
    t = p.read_text(encoding="utf-8", errors="replace")
    if 'name="description"' not in t and "name='description'" not in t:
        missing.append(p.relative_to(root).as_posix())
print("missing", len(missing))
for rel in missing[:25]:
    print(rel)
