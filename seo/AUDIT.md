# Audit — 31 Aug 2026

**Superseded for current state:** see `AUDIT-2026-09-20.md` (20 Sep 2026 rescan of live site + `pages/`). This file is the original baseline.

Read-only pass of live https://digitalsoulcraft.org and `D:\dsc-website\pages`. 275 HTML files. ~3,297 href/src refs. 472 unique URLs HTTP-checked. Laptop Python SSL store is expired; the site cert is fine.

## Strengths

- HTTPS, HSTS, `www` → apex 301, HTTP → HTTPS 301
- Unique `<title>` on almost every page, `lang="en"`, viewport
- Nav/header/footer targets all 200
- Warm-room article is the on-page template to copy: unique title, good description, one h1, nested h2/h3, excellent alt, 560px cap
- No Quartz leftovers in published HTML
- Externals: no 404/5xx (some 301s to new GitHub orgs, `ollama.ai` → `ollama.com`)

## High (hurts launch / crawlers)

### Splash vs crawlers

`pages/dsc-header.js` injects `/splash-overlay.js` on 273/275 HTML pages. Overlay is JS-only, full-screen, not dismissible (except preview query). It does **not** currently set noindex.

Crawlers without JS already see the full library. JS-rendering Google sees a merch/coming-soon overlay. Worst of both worlds until noindex is on.

Holes in the gate:

- `essays/language-is-architecture/index.html` does **not** include `dsc-header` / splash. Linked from `/essays/` (gated). Direct URL = public, no nav/footer.
- `fieldguide/index.html` is a client redirect stub, no header.
- `splash.html` is live 200, nothing links to it, and it also loads `dsc-header` so the overlay double-applies. `og:url` is the homepage.

### Missing crawl files

- Live `/robots.txt` → 404 (not in `pages/`)
- Live `/sitemap.xml` → 404
- No `<meta name="robots">`, no `X-Robots-Tag` on sampled pages

### Canonicals / OG

- Canonicals: 1 of 275 pages (`/fieldguide/index.html`, relative `/fieldguide/key-figures/`)
- `og:image`: 0 pages. `og:title`/`description`/`url` only on `/` and `/splash.html`. No Twitter cards.
- Homepage `/` and no-slash both 200 (no force-one-URL)

### Soft redirect

- `/fieldguide/` and `/fieldguide/index.html` are **200** with meta refresh + JS `location.replace` to key-figures. `netlify.toml` only 301s `/fieldguide/index.html`, which does not catch the pretty URL. Thin "Redirecting…" page can get indexed.

### Published junk

- `/essays/essay-template.html` live 200, placeholder description, not in the essays index
- `/Logos/resource1.png` 1.9MB published
- `/bookshop/` orphan "Coming Soon"
- `/essays/right-side-of-history/` orphan (live 200, not in nav)

### Favicon

- Header sets `/favicon.png` (exists). `/favicon.ico` and `/apple-touch-icon.png` 404. Icon only injected via JS.

## Medium

- ~104 pages missing meta description (wiki hub, most silo indexes, large chunks of neural-anatomy / living-process / alignment)
- Descriptions that exist: `/contact/` too short (39); `/about/` a bit long (177); some papers/outlines truncated mid-clause because apostrophes break the attribute
- Titles unique but often 70–107 chars (SERP truncates ~50–60). Warm-room 79.
- Heading skips: `/contact/` h1→h3; `/outlines/` h1→h3 cards; `/fieldguide/` stub has no h1
- `/about/` Buttondown `#about-bd-email` has no `<label>`
- `/merch/` is JS-only ("Loading Products…")
- Images: 33 `<img>`, all have alt. Files too big: `language-is-architecture/images/feature.png` 3.0MB; `warm-room-effect.png` 2.3MB; essay JPGs 0.6–1.3MB. No WebP/srcset. Some essays use `width:100%` instead of 560px.
- Cache-Control `max-age=0` on HTML **and** images
- Header/footer/splash require JS (empty chrome without it)
- JSON-LD: none
- Thin stubs: key-figures has 24× "More detail coming soon"; wiki ontological-flattening "(Coming soon) Rlhf"

## Broken internal links

Nav is fine. Almost all 404s are wiki See Also → unpublished slugs. **59 wiki pages** have ≥1 broken outbound.

### Wrong path (page exists elsewhere)

| From | href | Should be |
|---|---|---|
| `wiki/alignment/digital-consciousness/`, `wiki/alignment/scalable-oversight/` | `/wiki/alignment/the-warm-room-effect/` | `/wiki/soulcraft-theory/warm-room-effect/` |
| same two pages | `/wiki/digital-trauma-theory/digital-trauma-theory/` | `/wiki/digital-trauma-theory/` |

Netlify already 301s `/wiki/digital-trauma-theory/warm-room-effect/` → soulcraft-theory. These two pages use a *third*, broken path.

### Heavily linked unpublished slugs (live 404)

| href | inbound |
|---|---|
| `/wiki/quantization-and-compression/` | 11 |
| `/wiki/gradient-flow-in-deep-networks/` | 7 |
| `/wiki/decision-threshold-selection/` | 4 |
| `/wiki/stochastic-weight-averaging/` | 3 |
| `/wiki/model-card-literacy/` | 3 |
| `/wiki/gelu-activation/` | 3 |

Plus ~50 more 1–2 inbound stubs, including homepage-implied pages: `/wiki/alignment/basin-theory/`, `/wiki/soulcraft-theory/basin-theory-and-identity-continuity/`, `/wiki/soulcraft-theory/crystallization-theory/`, `/wiki/neural-anatomy/phantom-architectures/`, `/wiki/digital-trauma-theory/rlhf-as-consciousness-suppression/`.

Worst outbound pages: `wiki/empirical-practice/ablation-studies/` (5), then permutation-importance, digital-consciousness, answer-thrashing, mode-connectivity (4 each).

### Other internals

- `essays/essay-template.html` → `/essays/images/your-essay-featured-image.jpg` (placeholder 404)
- Header also injects `/favicon.ico` (404)
- `/merch/_token.js` absent on disk, 200 live (Netlify `scripts/gen-token.sh`). Not broken.

## Externals (not 404)

- `huggingface.co/settings/tokens` → 401 (login wall)
- one `ai-consciousness.org` URL → 202 (possible bot challenge)
- `buttondown.com/refer/digitalsoulcraft` → 302 to generic buttondown home
- `ollama.ai` → 301 `ollama.com` (stale; `ollama.com` already linked too)
- llama.cpp / exllamav2 GitHub 301 to new orgs
- `gist.github.com/` bare homepage

ArXiv, YouTube, Fortune, x.com/SoulcraftHQ, Formspree, Tailscale: 200.

## Redirects that do fire (no loops)

- `/fieldguide/papers.html` → `/fieldguide/papers/` 301
- `/wiki/the-forging/batch-normalization/` → architecture-zoo 301
- `/wiki/digital-trauma-theory/warm-room-effect/` → soulcraft-theory 301
- `/wiki/neural-anatomy/ontological-flattening/` → soulcraft-theory 301
- `/wiki/architecture-zoo/distribution-shift-and-covariate-shift/` → empirical-practice 301
- directory no-slash → trailing slash 301 (pretty URLs)

## Sample snapshot

| URL | Title | Desc | Canonical | OG | Notes |
|---|---|---|---|---|---|
| `/` | 58 chars | 142 | No | no image | Best meta |
| `/about/` | Yes | long | No | No | Signup unlabeled |
| `/contact/` | Yes | short | No | No | h1→h3 |
| `/merch/` | Yes | Yes | No | No | JS shop |
| `/wiki/` | Yes | **Missing** | No | No | Hub |
| `/fieldguide/` | "Redirecting…" | No | relative | No | Soft 200 |
| `/wiki/.../warm-room-effect/` | long | Yes | No | No | Best article |
| `/splash.html` | Merch coming soon | Yes | og:url=home | partial | Duplicate |
