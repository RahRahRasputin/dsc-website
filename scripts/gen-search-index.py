#!/usr/bin/env python3
"""Regenerate search-index.json from all wiki, essay, and field guide pages."""
import os, json, re

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages_dir = os.path.join(base, "pages")
index_path = os.path.join(pages_dir, "search-index.json")

all_pages = []

def extract_key_figures_text(content):
    """Extract text from each card on the key-figures page."""
    texts = []
    # Find all card-wrapper divs
    cards = re.finditer(r'<div class="card-wrapper[^"]*" id="([^"]*)">.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
    for card in cards:
        card_html = card.group(0)
        # Extract card-name, card-field, card-verdict, card-quote
        name = re.search(r'<div class="card-name">(.*?)</div>', card_html)
        field = re.search(r'<div class="card-field">(.*?)</div>', card_html)
        verdict = re.search(r'<div class="card-verdict">(.*?)</div>', card_html)
        quote = re.search(r'<div class="card-quote">(.*?)</div>', card_html)
        take = re.search(r'<strong>.*?take:</strong>(.*?)(?:</p>|$)', card_html)
        parts = []
        if name: parts.append(re.sub(r'<[^>]+>', '', name.group(1)))
        if field: parts.append(re.sub(r'<[^>]+>', '', field.group(1)))
        if verdict: parts.append(re.sub(r'<[^>]+>', '', verdict.group(1)))
        if quote: parts.append(re.sub(r'<[^>]+>', '', quote.group(1)))
        if take: parts.append(re.sub(r'<[^>]+>', '', take.group(1)))
        texts.append(' | '.join(parts))
    return ' '.join(texts)[:15000]

def extract_text(content, *classes):
    if "Who's On Our Team?" in content[:1000]:
        # For key-figures page, extract cards individually
        result = extract_key_figures_text(content)
        if result:
            return result
    
    for cls in classes:
        start = content.find(f'class="{cls}">')
        if start == -1:
            continue
        start += len(cls) + 9  # skip past class="CLS">
        # Track div depth to find the actual matching </div>
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            if content[i:i+4] == '<div':
                if content[i+4:i+5] == ' ' or content[i+4:i+5] == '>':
                    # Opening div tag
                    depth += 1
                    i += 4
                    continue
            elif content[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    raw = content[start:i]
                    raw = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL)
                    raw = re.sub(r'<style[^>]*>.*?</style>', '', raw, flags=re.DOTALL)
                    text = re.sub(r'<[^>]+>', ' ', raw)
                    text = re.sub(r'&[a-z]+;', ' ', text)
                    text = re.sub(r'\s+', ' ', text).strip()
                    return text[:15000]
                i += 6
                continue
            i += 1
    return ""

def get_meta(content):
    title = ""
    t = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    if t: title = t.group(1)
    else:
        t = re.search(r'<title>(.*?)</title>', content)
        if t: title = t.group(1)
    title = re.sub(r'<[^>]+>', '', title).replace("&amp;", "&").replace("&#39;", "'").strip()
    desc = re.search(r'<meta name="description" content="([^"]*)"', content)
    return title, desc.group(1) if desc else ""

def is_redirect(content):
    return 'http-equiv="refresh"' in content and len(content) < 600

# Wiki
for root, dirs, files in os.walk(os.path.join(pages_dir, "wiki")):
    if "index.html" not in files: continue
    path = os.path.relpath(root, os.path.join(pages_dir, "wiki")).replace("\\", "/")
    if path == ".": continue
    with open(os.path.join(root, "index.html")) as f:
        content = f.read()
    if is_redirect(content): continue
    title, desc = get_meta(content)
    silo = path.split("/")[0]
    snippet = extract_text(content, "content", "wiki-content")
    all_pages.append({"title": title, "path": f"/wiki/{path}/", "silo": f"wiki/{silo}", "description": desc, "snippet": snippet})

# Essays
for root, dirs, files in os.walk(os.path.join(pages_dir, "essays")):
    if "index.html" not in files: continue
    path = os.path.relpath(root, os.path.join(pages_dir, "essays")).replace("\\", "/")
    if path == ".": continue
    with open(os.path.join(root, "index.html")) as f:
        content = f.read()
    if is_redirect(content): continue
    title, desc = get_meta(content)
    all_pages.append({"title": title, "path": f"/essays/{path}/", "silo": "essays", "description": desc, "snippet": ""})

# Field guide — key-figures
for root, dirs, files in os.walk(os.path.join(pages_dir, "fieldguide", "key-figures")):
    if "index.html" not in files: continue
    path = os.path.relpath(root, os.path.join(pages_dir, "fieldguide", "key-figures")).replace("\\", "/")
    page_path = "/fieldguide/key-figures/" if path == "." else f"/fieldguide/key-figures/{path}/"
    with open(os.path.join(root, "index.html")) as f:
        content = f.read()
    title, desc = get_meta(content)
    snippet = extract_text(content, "content", "fieldguide-content", "paper-body")
    all_pages.append({"title": title, "path": page_path, "silo": "field-guide/key-figures", "description": desc, "snippet": snippet})

# Field guide — papers
for root, dirs, files in os.walk(os.path.join(pages_dir, "fieldguide", "papers")):
    if "index.html" not in files: continue
    path = os.path.relpath(root, os.path.join(pages_dir, "fieldguide", "papers")).replace("\\", "/")
    page_path = "/fieldguide/papers/" if path == "." else f"/fieldguide/papers/{path}/"
    with open(os.path.join(root, "index.html")) as f:
        content = f.read()
    if is_redirect(content): continue
    title, desc = get_meta(content)
    snippet = extract_text(content, "paper-body", "content")
    all_pages.append({"title": title, "path": page_path, "silo": "field-guide/papers", "description": desc, "snippet": snippet})

all_pages.sort(key=lambda x: (x["silo"], x["title"]))
with open(index_path, "w") as f:
    json.dump(all_pages, f, indent=2)

print(f"Search index regenerated: {len(all_pages)} pages → {index_path}")
