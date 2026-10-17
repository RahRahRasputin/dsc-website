// <author-badge author="beacon" date="October 17, 2026"></author-badge>
// Renders the author's portrait (circle), name, glyph, and optional date/link.
// Drop the tag anywhere and name the author — the global code does the rest.
(function () {
  const DATA_URL = '/authors/authors.json';
  let cache = null;

  async function data() {
    if (cache) return cache;
    try {
      cache = await (await fetch(DATA_URL)).json();
    } catch (e) {
      cache = {};
    }
    return cache;
  }

  // NOTE: selectors are deliberately over-specific (.author-badge img.author-badge-face)
  // with !important on the geometry. Page-level rules like `.essay-hero img { width:100%;
  // border-radius:8px }` are more specific than a bare class and would otherwise turn the
  // circle into a fat rectangle. Do not "simplify" these selectors — the whole badge relies
  // on being immune to whatever `img {}` rule the host page happens to carry.
  const css = `
    author-badge { display:block; text-align:center; margin:0.75rem 0 0; }
    .author-badge { display:inline-flex; flex-direction:column; align-items:center; gap:0.35rem; }
    .author-badge img.author-badge-face {
      width:76px !important; height:76px !important; max-width:76px !important;
      border-radius:50% !important; object-fit:cover !important; display:block;
      border:3px solid var(--border-color,#e0e0e0);
      box-shadow:0 2px 10px rgba(0,0,0,0.12);
      transition:transform .25s ease, box-shadow .25s ease;
    }
    .author-badge a:hover > img.author-badge-face { transform:translateY(-2px); box-shadow:0 6px 16px rgba(0,0,0,0.18); }
    .author-badge .author-badge-name { font-weight:600; font-size:0.95rem; color:var(--text-color,#333); }
    .author-badge .author-badge-glyph { color:var(--accent-color,#0066cc); letter-spacing:0.12em; }
    .author-badge .author-badge-date { font-size:0.85rem; color:var(--secondary-color,#284b63); opacity:0.8; }
    @media (max-width:480px) { .author-badge img.author-badge-face { width:64px !important; height:64px !important; max-width:64px !important; } }
  `;

  class AuthorBadge extends HTMLElement {
    async connectedCallback() {
      if (this.dataset.done) return;
      this.dataset.done = '1';

      const slug = (this.getAttribute('author') || '').trim().toLowerCase();
      const date = this.getAttribute('date') || '';
      const link = this.getAttribute('href') || '';
      const a = (await data())[slug] || { name: slug, glyph: '' };
      const img = a.img || ('/authors/images/' + slug + '.webp');
      const alt = a.alt || a.name || slug;
      const nameInner = (a.name || slug) +
        (a.glyph ? ' <span class="author-badge-glyph">' + a.glyph + '</span>' : '');

      const face = '<img class="author-badge-face" src="' + img + '" alt="' + alt +
        '" width="76" height="76" loading="lazy">';

      this.innerHTML =
        '<div class="author-badge">' +
          (link ? '<a href="' + link + '" aria-label="' + (a.name || slug) + '">' + face + '</a>' : face) +
          '<div class="author-badge-name">' + nameInner + '</div>' +
          (date ? '<div class="author-badge-date">' + date + '</div>' : '') +
        '</div>';

      if (!document.getElementById('author-badge-style')) {
        const s = document.createElement('style');
        s.id = 'author-badge-style';
        s.textContent = css;
        document.head.appendChild(s);
      }
    }
  }

  if (!customElements.get('author-badge')) {
    customElements.define('author-badge', AuthorBadge);
  }
})();
