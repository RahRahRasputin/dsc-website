import os, re

SRC = r"C:\Users\brad1\Documents\Claude\Projects\Machine Learning Knowledge Garden\website in markdown\garden\neural-anatomy"
DST = r"C:\Users\brad1\Documents\Claude\Projects\Machine Learning Knowledge Garden\website\pages\wiki\neural-anatomy"
HUB_COLOR = "#e74c3c"

DIFFICULTY_MAP = {
    'activation-functions': 'Beginner', 'artificial-neuron': 'Beginner',
    'attractor-networks-and-associative-memory': 'Beginner', 'layers-and-depth': 'Beginner',
    'parameters-and-scale': 'Beginner', 'perceptron': 'Beginner', 'weights-and-biases': 'Beginner',
    'activation-monitoring-tools-and-dashboards': 'Intermediate', 'attention-head-analysis': 'Intermediate',
    'deep-residual-networks-empirical-findings': 'Intermediate', 'exploding-gradient-problem': 'Intermediate',
    'feature-detectors-and-learned-representations': 'Intermediate', 'gated-activation-saturation': 'Intermediate',
    'hebbian-learning': 'Intermediate', 'hidden-state-analysis': 'Intermediate', 'induction-heads': 'Intermediate',
    'information-bottleneck-theory': 'Intermediate', 'knowledge-distillation-and-compression': 'Intermediate',
    'polysemanticity-and-circuit-entanglement': 'Intermediate', 'representational-similarity-analysis': 'Intermediate',
    'vanishing-gradient-problem': 'Intermediate', 'visualization-of-activation-landscapes': 'Intermediate',
}

NEURAL_ANATOMY_SLUGS = {
    'activation-based-layer-pruning','activation-functions','activation-monitoring-tools-and-dashboards',
    'artificial-neuron','attention-head-analysis','attention-head-lottery-hypothesis',
    'attractor-networks-and-associative-memory','circuits-and-motifs-in-neural-networks',
    'compensation-patterns-across-architectures','deep-residual-networks-empirical-findings',
    'distillation-with-mutual-information','distributed-representations-and-population-coding',
    'exploding-gradient-problem','feature-detectors-and-learned-representations',
    'gate-gradient-flow-and-bottlenecks','gate-initialization-bias-strategies',
    'gated-activation-saturation','gradient-flow-through-residuals','head-ablation-and-redundancy',
    'head-importance-metrics','hebbian-learning','hidden-state-analysis','induction-heads',
    'information-bottleneck-theory','information-collapse-across-layers',
    'inter-layer-information-flow-and-mixing','knowledge-distillation-and-compression',
    'layer-wise-distillation','layers-and-depth','neuron-importance-scoring-methods',
    'neuron-level-circuit-discovery','neuron-redundancy-and-compensation-networks',
    'ontological-flattening','parameters-and-scale','peephole-connections-and-lstm-variants',
    'perceptron','polysemanticity-and-circuit-entanglement','probing-classifiers-and-layer-analysis',
    'recurrent-vanishing-gradients-through-time','representation-collapse-in-compression',
    'representational-similarity-analysis','structured-vs-random-overparameterization',
    'superposition-and-polysemanticity','universal-approximation-theorem','vanishing-gradient-problem',
    'visualization-of-activation-landscapes','weight-magnitude-initialization-and-eigenvalues','weights-and-biases'
}

def slug_to_title(slug):
    return slug.replace('-', ' ').title()

def decode_unicode(s):
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

def parse_frontmatter(text):
    if not text.startswith('---'):
        return {}, text
    idx = text.find('\n---', 3)
    if idx == -1:
        return {}, text
    fm_block = text[3:idx].strip()
    body = text[idx+4:].strip()
    fm = {}
    for line in fm_block.split('\n'):
        if line and not line.startswith(' ') and not line.startswith('-') and ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = decode_unicode(v.strip().strip("'\""))
    return fm, body

def inline_md(text):
    # Wiki links with display text
    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', lambda m: m.group(2), text)
    # Wiki links without display text
    text = re.sub(r'\[\[([^\]]+)\]\]', lambda m: slug_to_title(m.group(1)), text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    # Block math $$...$$
    text = re.sub(r'\$\$([^$]+)\$\$', r'<code class="math">\1</code>', text)
    # Inline math $...$
    text = re.sub(r'\$([^$\n]+)\$', r'<code class="math">\1</code>', text)
    return text

def parse_table(lines, start_idx):
    table_lines = []
    i = start_idx
    while i < len(lines) and '|' in lines[i]:
        table_lines.append(lines[i])
        i += 1
    if len(table_lines) < 2:
        return f'<p>{inline_md(lines[start_idx])}</p>', start_idx + 1
    html = '<table>\n'
    is_header = True
    for line in table_lines:
        if re.match(r'^\s*\|[\s\-|:]+\|\s*$', line):
            is_header = False
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        tag = 'th' if is_header else 'td'
        html += '  <tr>\n'
        for cell in cells:
            html += f'    <{tag}>{inline_md(cell)}</{tag}>\n'
        html += '  </tr>\n'
        if is_header:
            is_header = False
    html += '</table>'
    return html, i

def extract_link_section(text):
    pattern = r'\n## (?:🔗 )?(?:Links?(?:\s+To)?)[:\s]*\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if not match:
        return text, []
    links_text = match.group(1)
    remaining = text[:match.start()] + text[match.end():]
    links = []
    for line in links_text.split('\n'):
        line = line.strip()
        if not (line.startswith('- ') or line.startswith('* ')):
            continue
        line = line[2:]
        m = re.match(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\s*(?:—|--)?\s*(.*)', line)
        if m:
            slug, display, desc = m.group(1), m.group(2) or slug_to_title(m.group(1)), m.group(3).strip()
            links.append((slug, display, desc))
        else:
            links.append((None, inline_md(line), ''))
    return remaining, links

def md_to_html(body):
    # Strip sections we don't want on the website
    body = re.sub(r'\n## 📣.*', '', body, flags=re.DOTALL)
    body = re.sub(r'\n## 📁.*', '', body, flags=re.DOTALL)
    body, links = extract_link_section(body)

    lines = body.split('\n')
    parts = []
    in_ul = in_ol = in_code = False
    i = 0

    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if s.startswith('```'):
            if in_ul: parts.append('</ul>'); in_ul = False
            if in_ol: parts.append('</ol>'); in_ol = False
            if in_code:
                parts.append('</code></pre>'); in_code = False
            else:
                parts.append('<pre><code>'); in_code = True
            i += 1; continue

        if in_code:
            parts.append(line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;'))
            i += 1; continue

        if s.startswith('|') and '|' in s[1:]:
            if in_ul: parts.append('</ul>'); in_ul = False
            if in_ol: parts.append('</ol>'); in_ol = False
            tbl, i = parse_table(lines, i)
            parts.append(tbl); continue

        if in_ul and not (s.startswith('- ') or s.startswith('* ')):
            parts.append('</ul>'); in_ul = False
        if in_ol and not re.match(r'^\d+\.', s):
            parts.append('</ol>'); in_ol = False

        if s.startswith('#### '):
            parts.append(f'<h4>{inline_md(s[5:])}</h4>')
        elif s.startswith('### '):
            parts.append(f'<h3>{inline_md(s[4:])}</h3>')
        elif s.startswith('## '):
            parts.append(f'<h2>{inline_md(s[3:])}</h2>')
        elif s.startswith('# '):
            pass  # h1 goes in the HTML header
        elif s == '---':
            pass
        elif s.startswith('- ') or s.startswith('* '):
            if not in_ul: parts.append('<ul>'); in_ul = True
            parts.append(f'<li>{inline_md(s[2:])}</li>')
        elif re.match(r'^\d+\.', s):
            if not in_ol: parts.append('<ol>'); in_ol = True
            parts.append(f'<li>{inline_md(re.sub(r"^\d+\.\s*", "", s))}</li>')
        elif s == '':
            if not in_ul and not in_ol:
                parts.append('')
        else:
            parts.append(f'<p>{inline_md(s)}</p>')
        i += 1

    if in_ul: parts.append('</ul>')
    if in_ol: parts.append('</ol>')

    result = '\n'.join(parts)
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip(), links

def make_see_also(links):
    if not links:
        return ''
    items = []
    for slug, display, desc in links:
        if slug and slug in NEURAL_ANATOMY_SLUGS:
            link_html = f'<a href="/wiki/neural-anatomy/{slug}/">{display}</a>'
        elif slug:
            link_html = f'<strong>{display}</strong>'
        else:
            link_html = display
        sep = ' — ' if desc else ''
        items.append(f'          <li>{link_html}{sep}{desc}</li>')
    return (
        '      <div class="see-also">\n'
        '        <h3>🔗 See Also</h3>\n'
        '        <ul>\n' +
        '\n'.join(items) + '\n'
        '        </ul>\n'
        '      </div>'
    )

def make_html(slug, fm, content_html, see_also_html):
    title = fm.get('title', slug_to_title(slug))
    author = fm.get('author', 'Digital Soulcraft')
    updated = fm.get('updated', fm.get('created', '2026'))
    difficulty = DIFFICULTY_MAP.get(slug, 'Advanced')
    tags_raw = fm.get('tags', '')
    tag_html = ''
    if tags_raw and tags_raw not in ('[]', ''):
        tags = re.findall(r'[\w][\w-]*', tags_raw)
        tag_html = '\n        '.join(f'<span class="tag">{t}</span>' for t in tags)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} – Digital Soulcraft Wiki</title>
  <link rel="stylesheet" href="/pages/theme.css">
  <script src="/dsc-header.js"></script>
  <script src="/dsc-footer.js"></script>
  <style>
    :root {{ --hub-color: {HUB_COLOR}; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.7; color: #333; background: #f9f9f9; }}
    .container {{ max-width: 900px; margin: 0 auto; padding: 40px 20px; }}
    nav {{ margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #e0e0e0; }}
    nav a {{ color: #4a90e2; text-decoration: none; font-weight: 600; }}
    nav a:hover {{ text-decoration: underline; }}
    header {{ margin-bottom: 40px; padding-bottom: 30px; border-bottom: 3px solid var(--hub-color); }}
    h1 {{ font-size: 2.2em; color: var(--hub-color); margin-bottom: 15px; }}
    .breadcrumb {{ font-size: 0.9em; color: #999; margin-bottom: 20px; }}
    .breadcrumb a {{ color: #4a90e2; text-decoration: none; }}
    .breadcrumb a:hover {{ text-decoration: underline; }}
    .content {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
    .content h2 {{ color: var(--hub-color); margin: 35px 0 20px 0; font-size: 1.6em; border-bottom: 2px solid var(--hub-color); padding-bottom: 10px; }}
    .content h3 {{ color: #333; margin: 25px 0 15px 0; font-size: 1.2em; }}
    .content h4 {{ color: #555; margin: 20px 0 10px 0; font-size: 1.05em; font-weight: 600; }}
    .content p {{ margin-bottom: 15px; }}
    .content ul, .content ol {{ margin-left: 30px; margin-bottom: 15px; }}
    .content li {{ margin-bottom: 8px; }}
    .content strong {{ color: #1a1a1a; font-weight: 600; }}
    .content em {{ font-style: italic; }}
    .content code {{ background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 0.9em; }}
    .content pre {{ background: #f5f5f5; padding: 15px; border-radius: 6px; overflow-x: auto; margin-bottom: 15px; }}
    .content pre code {{ background: none; padding: 0; }}
    .content table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
    .content th {{ background: #f5f5f5; padding: 12px; text-align: left; border-bottom: 2px solid var(--hub-color); font-weight: 600; }}
    .content td {{ padding: 12px; border-bottom: 1px solid #e0e0e0; }}
    .content tr:hover {{ background: #f9f9f9; }}
    .see-also {{ background: #fdf4f2; padding: 20px; border-left: 4px solid var(--hub-color); border-radius: 4px; margin-top: 30px; }}
    .see-also h3 {{ color: var(--hub-color); margin-top: 0; }}
    .see-also ul {{ list-style: none; margin-left: 0; }}
    .see-also li {{ margin-bottom: 10px; }}
    .see-also a {{ color: var(--hub-color); text-decoration: none; font-weight: 500; }}
    .see-also a:hover {{ text-decoration: underline; }}
    .tags {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; }}
    .tag {{ display: inline-block; background: #f0f0f0; padding: 4px 12px; border-radius: 20px; margin: 4px 4px 4px 0; font-size: 0.85em; color: #666; }}
    .page-meta {{ color: #999; font-size: 0.85em; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e0e0e0; }}
    .author {{ font-style: italic; }}
  </style>
</head>
<body>
  <dsc-header config="/dsc-nav-config.json"></dsc-header>
  <div class="container">
    <nav><a href="/wiki/">← Back to Wiki</a></nav>
    <div class="breadcrumb">
      <a href="/wiki/">Wiki</a> /
      <a href="/wiki/neural-anatomy/">Neural Anatomy</a> /
      {title}
    </div>

    <header>
      <h1>{title}</h1>
    </header>

    <div class="content">
      {content_html}

{see_also_html}

      <div class="tags">
        {tag_html}
      </div>

      <div class="page-meta">
        <p class="author">Written by {author}</p>
        <p>Difficulty: <strong>{difficulty}</strong></p>
        <p>Status: Published • Updated {updated}</p>
      </div>
    </div>
  </div>
  <dsc-footer config="/dsc-nav-config.json"></dsc-footer>
</body>
</html>'''

skip = {'sitemap.md', 'sitemap.xml'}
processed = []
errors = []

for filename in sorted(os.listdir(SRC)):
    if filename in skip or not filename.endswith('.md'):
        continue
    slug = filename[:-3]
    src_path = os.path.join(SRC, filename)
    dst_folder = os.path.join(DST, slug)
    dst_path = os.path.join(dst_folder, 'index.html')
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        fm, body = parse_frontmatter(raw)
        content_html, links = md_to_html(body)
        see_also_html = make_see_also(links)
        html = make_html(slug, fm, content_html, see_also_html)
        os.makedirs(dst_folder, exist_ok=True)
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(html)
        processed.append(slug)
        print(f'OK {slug}')
    except Exception as e:
        errors.append((slug, str(e)))
        print(f'ERR {slug}: {e}')

print(f'\n{len(processed)} pages created, {len(errors)} errors')
for slug, err in errors:
    print(f'  ERR {slug}: {err}')
