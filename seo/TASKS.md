# SEO tasks

Brad 31 Aug 2026: splash stays until public announcement. Sitewide **noindex, nofollow** until then. Gary owns HTML/Netlify structure. Ping him for layout/component work. James owns drawings.

Status: `[ ]` not started · `[x]` done. Update this file as you go.

---

## Now (embargo)

Do these first. The library is already crawlable without JS.

- [x] **Sitewide noindex, nofollow until launch** (working tree 31 Aug 2026 PT; not pushed)
  - Meta `robots` noindex,nofollow on every published HTML page (inject from `dsc-header.js` so it cannot be forgotten, **and** put it in the HTML so it works without JS)
  - Netlify `X-Robots-Tag: noindex, nofollow` on all HTML (belt)
  - `pages/robots.txt`: `User-agent: *` / `Disallow: /` (no sitemap line while embargoed)
  - Confirm live homepage and a wiki article send noindex (view-source, not just the overlay)
- [x] Close gate holes
  - Add `dsc-header` / splash to `essays/language-is-architecture/` (or a shared noindex include if Gary prefers)
  - 301 `/splash.html` → `/` or canonical it to `/` so it is not a second homepage
- [x] Unpublish stubs from the live tree (move out of `pages/` or 404/noindex)
  - `/essays/essay-template.html`
  - Confirm `/bookshop/` and other coming-soon orphans are noindex too
- [x] 301 `/fieldguide` and `/fieldguide/` → `/fieldguide/key-figures/` in `netlify.toml` (replace the 200 JS stub). Ask Gary if the stub file should stay as a fallback.
- [x] Retarget wrong-path See Also (real 404s, pages exist elsewhere)
  - `/wiki/alignment/the-warm-room-effect/` → `/wiki/soulcraft-theory/warm-room-effect/`
  - `/wiki/digital-trauma-theory/digital-trauma-theory/` → `/wiki/digital-trauma-theory/`
  - From: `wiki/alignment/digital-consciousness/` and `wiki/alignment/scalable-oversight/`

Do **not** add a public sitemap while embargoed.

---

## Before splash comes down (prep, not live-index)

Safe to draft in the repo; do not flip robots to Allow until Brad says the overlay is coming off.

- [ ] Draft `sitemap.xml` of indexable HTML with trailing-slash canonicals (keep it unpublished or Disallow until launch)
- [x] Absolute canonical + matching `og:url` on every published page (trailing slash). Homepage is `https://digitalsoulcraft.org/`. (Grok 20 Sep 2026; still no Netlify force-one-URL rule beyond existing trailing-slash 301s.)
- [ ] Default OG image 1200×630 sitewide + `twitter:card=summary_large_image`. Per-essay/wiki images where they exist.
- [ ] Static `<link rel="icon" href="/favicon.png">` in HTML (not only JS). Add `favicon.ico` and `apple-touch-icon.png` if Brad has artwork. `theme-color`.
- [x] Unique meta descriptions on wiki (and the rest of published HTML). Truncated 160-char cuts rewritten. Apostrophe-clipped `answer-thrashing` quote fixed. (Grok 20 Sep 2026)
- [ ] Trim titles toward 50–60 chars; distinctive phrase first. (Only `training-vs-inference` slug title fixed 20 Sep; paper titles still long.)
- [ ] Heading fixes: `/contact/` and `/outlines/` (no skipped levels). `/about/` add a real `<label>` for `#about-bd-email`.
- [ ] Image pass with James/Gary: compress 1–3MB PNGs/JPGs to display size; default `max-width: 560px` in CSS; richer alts on Ghibli plates (not just the heading).
- [ ] Wiki See Also: either publish the stub, retarget, or unlink. Highest inbound 404s: `quantization-and-compression` (11), `gradient-flow-in-deep-networks` (7), then decision-threshold, SWA, model-card-literacy, gelu. Homepage names basin-theory / crystallization pages that do not exist — do not leave those as 404s at launch.
- [ ] Update stale externals: `ollama.ai` → `ollama.com`; llama.cpp / exllamav2 new GitHub orgs.
- [ ] Long-cache static assets (`_headers` for `/images/*`, png, css, js). HTML can stay must-revalidate.
- [ ] Optional: JSON-LD `WebSite` + `Organization` on home; `Article` on essays/wiki. SSR a product list on `/merch/` so it is not "Loading Products…". `noscript` nav if Gary wants progressive enhancement.

---

## Launch day (only when Brad says)

- [ ] Remove splash overlay from `dsc-header.js`
- [ ] Flip meta robots + `X-Robots-Tag` to index,follow (or omit)
- [ ] `robots.txt` Allow: / and `Sitemap: https://digitalsoulcraft.org/sitemap.xml`
- [ ] Publish sitemap
- [ ] Spot-check Search Console / live headers
- [ ] Confirm `language-is-architecture` still has header/footer
- [ ] Confirm `/fieldguide/` 301s
- [ ] Confirm `essay-template` is not live

---

## Recurring

- [ ] Recrawl after each content drop (broken See Also, missing descriptions on new wiki pages)
- [ ] Keep canonicals/OG in whatever page template Gary uses
- [ ] After James ships an illustration: check alt, 560px, file size before it is a ranking problem

---

*"One bite at a time."*
