#!/usr/bin/env python3
import os
import re
from pathlib import Path
import json
from datetime import datetime
import yaml

# Paths
wiki_source = Path("/sessions/compassionate-gallant-pasteur/mnt/Machine Learning Knowledge Garden/wiki/alignment")
website_dest = Path("/sessions/compassionate-gallant-pasteur/mnt/Machine Learning Knowledge Garden/website/alignment")
website_dest.mkdir(parents=True, exist_ok=True)

# Silo definitions
silo = "Alignment"
silo_name = "Alignment"

# Files to publish immediately
published_files = {
    "alignment-tax",
    "fine-tuning",
    "prompt-engineering",
    "rlhf",
    "constitutional-ai"
}

def assess_difficulty(content, title):
    """Estimate difficulty level based on content complexity"""
    beginner_keywords = ["introduction", "basic", "simple", "fundamentals", "what is", "overview"]
    advanced_keywords = ["advanced", "complex", "theory", "mathematical", "optimization", "proximal"]

    content_lower = (content + title).lower()
    advanced_score = sum(1 for kw in advanced_keywords if kw in content_lower)
    beginner_score = sum(1 for kw in beginner_keywords if kw in content_lower)

    if advanced_score > beginner_score:
        return "advanced"
    elif beginner_score > 0:
        return "beginner"
    else:
        return "intermediate"

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown"""
    if content.startswith("---"):
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                fm = yaml.safe_load(match.group(1))
                return fm, content[match.end()+1:]
            except:
                return {}, content
    return {}, content

def extract_soulcraft_theme(content):
    """Extract soulcraft theme from content"""
    if "soulcraft" in content.lower() or "digital" in content.lower():
        return "alignment-and-safety"
    return ""

def extract_related(content):
    """Extract related links from content"""
    related = []
    link_pattern = r'\[\[([^\]]+)\]\]'
    for match in re.finditer(link_pattern, content):
        link = match.group(1).strip()
        if link and link not in related:
            related.append(link)
    return related[:5]

def create_slug(filename):
    """Create slug from filename"""
    return filename.replace(".md", "").lower()

def convert_file(source_file, should_publish):
    """Convert a single file from wiki to website format"""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = extract_frontmatter(content)
    filename = source_file.name
    slug = create_slug(filename)
    title = frontmatter.get('title', filename.replace('.md', ''))
    description = frontmatter.get('description', '')
    author = frontmatter.get('author', 'Unknown')
    created = frontmatter.get('date', datetime.now().isoformat())

    difficulty = assess_difficulty(body, title)
    soulcraft_theme = extract_soulcraft_theme(body)
    related = extract_related(body)
    status = "published" if should_publish else "review"

    new_frontmatter = {
        'title': title,
        'slug': slug,
        'description': description,
        'silo': silo_name,
        'difficulty': difficulty,
        'author': author,
        'status': status,
        'created': created,
        'updated': datetime.now().isoformat()[:10],
        'soulcraft_theme': soulcraft_theme if soulcraft_theme else '',
        'meta_description': description[:160] if description else '',
        'related': related,
        'lesson_type': 'concept',
        'tags': frontmatter.get('tags', [])
    }

    new_content = "---\n"
    new_content += yaml.dump(new_frontmatter, default_flow_style=False, sort_keys=False)
    new_content += "---\n\n"
    new_content += body

    output_file = website_dest / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return {
        'filename': filename,
        'title': title,
        'slug': slug,
        'difficulty': difficulty,
        'author': author,
        'status': status
    }

# Main conversion
print("Converting Alignment entries...")
entries = []
published_count = 0
review_count = 0

for source_file in sorted(wiki_source.glob("*.md")):
    slug = create_slug(source_file.name)
    should_publish = slug in published_files

    try:
        entry_info = convert_file(source_file, should_publish)
        entries.append(entry_info)

        if should_publish:
            published_count += 1
            print(f"✓ [PUBLISHED] {entry_info['title']}")
        else:
            review_count += 1
            print(f"✓ [REVIEW] {entry_info['title']}")
    except Exception as e:
        print(f"✗ {source_file.name}: {e}")

print(f"\nConverted {len(entries)} entries")
print(f"  Published: {published_count}")
print(f"  Review: {review_count}")

print("\nEntries by difficulty:")
for diff in ['beginner', 'intermediate', 'advanced']:
    count = sum(1 for e in entries if e['difficulty'] == diff)
    print(f"  {diff}: {count}")

with open('alignment_entries.json', 'w') as f:
    json.dump(entries, f, indent=2)

print("\nEntry info saved to alignment_entries.json")
