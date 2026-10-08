// Digital Soulcraft — Site-wide Search Widget
(function() {
  'use strict';

  let index = [];
  let inputEl, resultsEl;

  // Load search index once
  async function loadIndex() {
    if (index.length) return;
    try {
      const res = await fetch('/search-index.json?_=' + Date.now());
      index = await res.json();
    } catch (e) {
      console.warn('Search index unavailable:', e);
    }
  }

  function normalize(s) {
    return s.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim();
  }

  function search(query) {
    if (!query || !index.length) return [];
    const q = normalize(query);
    const terms = q.split(/\s+/).filter(Boolean);
    if (!terms.length) return [];

    const scored = [];
    for (const item of index) {
      let score = 0;
      const title = normalize(item.title);
      const desc = normalize(item.description || '');
      const snippet = normalize(item.snippet || '');
      const all = title + ' ' + desc + ' ' + snippet;

      // Exact title match gets highest score
      if (title === q) score += 100;
      else if (title.startsWith(q)) score += 80;
      else if (title.includes(q)) score += 60;

      // Term-by-term matching
      for (const term of terms) {
        if (title.includes(term)) score += 30;
        else if (desc.includes(term)) score += 15;
        else if (snippet.includes(term)) score += 10;
        if (all.includes(term)) score += 5;
      }

      if (score > 0) {
        scored.push({ item, score });
      }
    }

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, 15).map(s => s.item);
  }

  function renderResults(results) {
    if (!resultsEl) return;
    if (!results.length) {
      resultsEl.innerHTML = '<div class="dsc-search-empty">No results found</div>';
      resultsEl.classList.add('show');
      return;
    }
    resultsEl.innerHTML = results.map(r => `
      <div class="dsc-search-result" data-path="${r.path}">
        <div class="result-title">${escapeHtml(r.title)}</div>
        <div class="result-silo">${escapeHtml(r.silo)}</div>
        ${r.description ? `<div class="result-desc">${escapeHtml(r.description.substring(0, 120))}</div>` : ''}
      </div>
    `).join('');
    resultsEl.classList.add('show');

    // Click handler
    resultsEl.querySelectorAll('.dsc-search-result').forEach(el => {
      el.addEventListener('click', () => {
        window.location.href = el.dataset.path;
      });
      // Keyboard navigation support
      el.addEventListener('mouseenter', () => {
        resultsEl.querySelectorAll('.dsc-search-result').forEach(e => e.classList.remove('active'));
        el.classList.add('active');
      });
    });
  }

  function escapeHtml(s) {
    if (!s) return '';
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  function init() {
    // Already initialized?
    if (document.getElementById('dsc-search-input')) return;

    const wrap = document.createElement('div');
    wrap.className = 'dsc-search-wrap';
    wrap.innerHTML = `
      <input type="search" id="dsc-search-input" class="dsc-search-input" placeholder="Search wiki, essays, field guide… (e.g. 'attention', 'gradient', 'consciousness')" autocomplete="off">
      <div id="dsc-search-results" class="dsc-search-results"></div>
    `;

    // Find where to insert — before the first h1 or after the breadcrumb/nav
    const nav = document.querySelector('nav, .wiki-nav, .breadcrumb');
    const header = document.querySelector('header, .wiki-header');
    const container = document.querySelector('.content, .wiki-content, .container, main');

    if (nav && nav.parentNode) {
      nav.parentNode.insertBefore(wrap, nav.nextSibling);
    } else if (header && header.parentNode) {
      header.parentNode.insertBefore(wrap, header.nextSibling);
    } else if (container && container.parentNode) {
      container.parentNode.insertBefore(wrap, container);
    } else {
      document.body.prepend(wrap);
    }

    inputEl = document.getElementById('dsc-search-input');
    resultsEl = document.getElementById('dsc-search-results');

    // Load index on focus
    let loaded = false;
    inputEl.addEventListener('focus', async () => {
      if (!loaded) { await loadIndex(); loaded = true; }
      if (inputEl.value.trim()) {
        renderResults(search(inputEl.value));
      }
    });

    // Search on input
    let timer;
    inputEl.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(async () => {
        if (!loaded) { await loadIndex(); loaded = true; }
        const q = inputEl.value.trim();
        if (q.length >= 2) {
          renderResults(search(q));
        } else {
          resultsEl.classList.remove('show');
        }
      }, 120);
    });

    // Close on blur (with delay for click)
    inputEl.addEventListener('blur', () => {
      setTimeout(() => resultsEl.classList.remove('show'), 200);
    });

    // Keyboard navigation
    inputEl.addEventListener('keydown', (e) => {
      const items = resultsEl.querySelectorAll('.dsc-search-result');
      const active = resultsEl.querySelector('.active');
      let idx = -1;
      if (active) idx = Array.from(items).indexOf(active);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const next = Math.min(idx + 1, items.length - 1);
        items.forEach(el => el.classList.remove('active'));
        if (items[next]) items[next].classList.add('active');
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prev = Math.max(idx - 1, 0);
        items.forEach(el => el.classList.remove('active'));
        if (items[prev]) items[prev].classList.add('active');
      } else if (e.key === 'Enter') {
        const target = active || items[0];
        if (target) window.location.href = target.dataset.path;
      } else if (e.key === 'Escape') {
        resultsEl.classList.remove('show');
        inputEl.blur();
      }
    });
  }

  // Run on DOMContentLoaded and also immediately if already loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();