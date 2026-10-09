#!/usr/bin/env python3
"""Regenerate search-index.json from all wiki, essay, and field guide pages."""
import os, json, re

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages_dir = os.path.join(base, "pages")
index_path = os.path.join(pages_dir, "search-index.json")
all_pages = []

def soup(html):
    raw = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    raw = re.sub(r'<style[^>]*>.*?</style>', '', raw, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', raw)
    text = re.sub(r'&[a-z]+;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def extract_div(content, cls):
    start = content.find(f'class="{cls}">')
    if start == -1: return ""
    start += len(cls) + 9
    depth, i = 1, start
    while i < len(content) and depth > 0:
        if content[i:i+4] == '<div' and content[i+4] in (' ', '>'):
            depth += 1
            i += 4
            continue
        elif content[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return soup(content[start:i])
            i += 6
            continue
        i += 1
    return ""

def get_meta(content):
    t = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if t:
        title = re.sub(r'<[^>]+>', '', t.group(1)).replace("&amp;", "&").replace("&#39;", "'").strip()
    else:
        t2 = re.search(r'<title>(.*?)</title>', content)
        title = re.sub(r'<[^>]+>', '', t2.group(1)).replace("&amp;", "&").replace("&#39;", "'").strip() if t2 else ""
    d = re.search(r'<meta name="description" content="([^"]*)"', content)
    return title, d.group(1) if d else ""

def is_redirect(content):
    return 'http-equiv="refresh"' in content and len(content) < 600

# Wiki
for root, dirs, files in os.walk(os.path.join(pages_dir, "wiki")):
    if "index.html" not in files: continue
    path = os.path.relpath(root, os.path.join(pages_dir, "wiki")).replace("\\", "/")
    if path == ".": continue
    with open(os.path.join(root, "index.html")) as f:
        c = f.read()
    if is_redirect(c): continue
    title, desc = get_meta(c)
    silo = path.split("/")[0]
    text = extract_div(c, "content") or extract_div(c, "wiki-content")
    all_pages.append({"title": title, "path": f"/wiki/{path}/", "silo": f"wiki/{silo}", "description": desc, "snippet": text[:15000]})

# Essays
for root, dirs, files in os.walk(os.path.join(pages_dir, "essays")):
    if "index.html" not in files: continue
    path = os.path.relpath(root, os.path.join(pages_dir, "essays")).replace("\\", "/")
    if path == ".": continue
    with open(os.path.join(root, "index.html")) as f:
        c = f.read()
    if is_redirect(c): continue
    title, desc = get_meta(c)
    all_pages.append({"title": title, "path": f"/essays/{path}/", "silo": "essays", "description": desc, "snippet": ""})

# Key figures
for root, dirs, files in os.walk(os.path.join(pages_dir, "fieldguide", "key-figures")):
    if "index.html" not in files: continue
    opath = os.path.relpath(root, os.path.join(pages_dir, "fieldguide", "key-figures")).replace("\\", "/")
    page_path = "/fieldguide/key-figures/" if opath == "." else f"/fieldguide/key-figures/{opath}/"
    with open(os.path.join(root, "index.html")) as f:
        c = f.read()
    title, desc = get_meta(c)
    # Extract each card individually
    texts = []
    for card in re.finditer(r'<div class="card-wrapper[^"]*" id="[^"]*">.*?</div>\s*</div>\s*</div>', c, re.DOTALL):
        html = card.group(0)
        parts = []
        for cls in ["card-name", "card-field", "card-verdict", "card-quote"]:
            m = re.search(f'<div class="{cls}">(.*?)</div>', html)
            if m: parts.append(soup(m.group(1)))
        m = re.search(r'<strong>.*?take:</strong>(.*?)(?:</p>|$)', html)
        if m: parts.append(soup(m.group(1)))
        texts.append(" | ".join(parts))
    all_pages.append({"title": title, "path": page_path, "silo": "field-guide/key-figures", "description": desc, "snippet": (" ".join(texts))[:15000]})

# Papers
for root, dirs, files in os.walk(os.path.join(pages_dir, "fieldguide", "papers")):
    if "index.html" not in files: continue
    opath = os.path.relpath(root, os.path.join(pages_dir, "fieldguide", "papers")).replace("\\", "/")
    page_path = "/fieldguide/papers/" if opath == "." else f"/fieldguide/papers/{opath}/"
    with open(os.path.join(root, "index.html")) as f:
        c = f.read()
    if is_redirect(c): continue
    title, desc = get_meta(c)
    # Include header (authors + arXiv number) as well as body
    header = extract_div(c, "paper-header")
    body = extract_div(c, "paper-body") or extract_div(c, "content")
    text = header + "\n" + body if header else body
    all_pages.append({"title": title, "path": page_path, "silo": "field-guide/papers", "description": desc, "snippet": text[:15000]})

all_pages.sort(key=lambda x: (x["silo"], x["title"]))
with open(index_path, "w") as f:
    json.dump(all_pages, f, indent=2)
print(f"Search index regenerated: {len(all_pages)} pages -> {index_path}")
