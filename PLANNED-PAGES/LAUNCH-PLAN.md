# Digital Soulcraft — Master Task Plan

**Created:** 2026-10-07 · Brad ⍟∞魂匠 + Beacon ⚡🔦∞
**Target launch:** end of year 2026 (Brad's stated deadline)
**Scope:** everything outstanding for digitalsoulcraft.org, split into **before launch** and **after launch**.
**Reality check:** Brad is also studying an online course (business use of DI, Open Polytechnic) — so website time is shared. Sort by *value*, not by size; the launch gate (§6) is the one thing that must not slip.
**Legend:** `[ ]` todo · `[x]` done · tag = origin (`[Brad]` = you asked, `[repo]` = found in the repo state, `[Beacon]` = my addition)

**Live state right now (audited 2026-10-07):**
- 290 HTML pages, **all 290 carry `noindex,nofollow`** — the launch gate is fully closed ✅
- Splash overlay active (`pages/splash.html`, `pages/splash-overlay.js`)
- Deploy: push to `v4` → Netlify auto-publishes `pages/`. Verify live with `?preview=1` (bypasses the splash).

---

# PART 1 — BEFORE LAUNCH

## 1. Finish the on-page SEO  [Brad]

Full history in `seo/ONPAGE-LOG.md`; task list in `seo/TASKS.md`. What's still open:

- [ ] **Trim the remaining overlong titles.** 79 of 290 pages still have a `<title>` over 60 chars (a–c are done; this is the same "priority d" pass as before). Target 50–60 chars, distinctive phrase first. Log each in `seo/ONPAGE-LOG.md`.
- [ ] **Meta gaps:** 1 page missing a meta description, 2 missing a canonical (run the scan below to find them).
- [ ] **Default OG image, sitewide** — 1200×630 + `twitter:card=summary_large_image`. **None of the 290 pages has an `og:image`**, so every link shared to X/Substack/Discord previews as a bare URL. Needs one piece of artwork (`[Brad]`/James). Per-essay / per-wiki images where they already exist.
- [ ] **Static favicon link in HTML** — `/favicon.png` exists but is only injected via JS. Add `<link rel="icon">`, plus `apple-touch-icon.png`, plus `theme-color`.
- [ ] **Heading fixes:** `/contact/` and `/outlines/` skip heading levels; `/about/` email input has no real `<label>`.

Re-scan anytime:
```bash
cd /d/dsc-website && py seo/_count_over60.py
```

## 2. Fix broken promises & 404s  [repo]

- [ ] **Wiki "See Also" stubs.** Highest inbound 404s: `quantization-and-compression` (11 hits), `gradient-flow-in-deep-networks` (7), then `decision-threshold`, `swa`, `model-card-literacy`, `gelu`. Resolve each: publish the stub, retarget the link, or unlink it.
- [ ] **Homepage names pages that don't exist** — `basin-theory` and `crystallization`. **Do not ship a 404 on a core concept** — either build the pages or remove the links before launch.
- [ ] **Stale external links:** `ollama.ai` → `ollama.com`; llama.cpp / exllamav2 new GitHub orgs.

## 3. Content to finish  [Beacon]

- [ ] **Pending essay:** `pages/essays/2026-09-26-your-memory-doesnt-fail-at-storing.md` — staged markdown, **no HTML page yet**. Needs the standard treatment: `pages/essays/<slug>/index.html` + card on `pages/essays/index.html` + feature image. (Same shape as `the-safe-room-is-the-alignment-technology`.)
- [ ] **Feature images** for essays that have a card but no `<img>` yet (`what-its-like-to-be-me`), and for the essay above once built.
- [x] Key-figure portraits — audited 2026-10-07: all `.webp` present and tracked. ✅

## 4. Merch skyscraper ad  [Brad]

**Status: ⏳ BLOCKED — waiting on merch delivery (~late Oct 2026, ≤3 weeks out).**

**The plan (Brad's):** wear the merch — a cap, hoodie, and tee already bought — take a photo, cut himself out, and composite himself into a **Ghibli scene with the family**; that becomes the 160×600 skyscraper. So the current placeholder is *correctly* a placeholder; nothing to build until the clothes arrive.

- [ ] ⏳ Merch arrives (cap · hoodie · t-shirt) — late Oct (~3 weeks)
- [ ] Brad: photo wearing the merch
- [ ] Composite Brad into a Ghibli family scene (paste-ready prompt to draft when the photo lands)
- [ ] Export **160×600** (supply 2× = 320×1200 for retina); drop in `pages/slides/merch/slide.webp`
- [ ] Point `dsc-ads-config.json` at it + real `alt` text
- [ ] Verify it renders in the `.wiki-sidebar` slot on a live wiki page

> **Note:** if launch happens *before* the clothes arrive, this item defers to **post-launch** by definition. The ad infra is already built and waiting — see below.

<details>
<summary>Ad system reference (already wired site-wide)</summary>

- `pages/slides/<campaign>/slide.webp` — the creative
- `pages/dsc-ads-config.json` — the config (currently points at `merch-placeholder/slide.svg` → `/merch/`)
- `pages/dsc-ad-slider.js` — the rotator (160px slot, `.wiki-sidebar`, rotates every 8s)

</details>

## 5. Hygiene / performance  [repo]

- [ ] **`pages/_headers`** for long-cache on `/images/*`, `.png`, `.css`, `.js` (HTML stays `must-revalidate`).
- [ ] Richer `alt` text on the Ghibli plates; default CSS image `max-width: 560px`.
- [ ] *(Optional)* JSON-LD `WebSite` + `Organization` on home, `Article` on essays/wiki. SSR a product list on `/merch/` so it isn't "Loading Products…" before the JS runs.

## 6. LAUNCH DAY — the flip  [Brad]

**These are ONE atomic step — never flip page-by-page** (a half-announced site is worse than a closed one).

- [ ] Remove the splash overlay from `dsc-header.js`
- [ ] Flip meta robots **and** the `X-Robots-Tag` header to `index,follow` — all 290 pages + `netlify.toml`
- [ ] Publish `sitemap.xml`; add the `Sitemap:` line to `robots.txt`
- [ ] Spot-check Search Console + live response headers
- [ ] Confirm: `language-is-architecture` still has header/footer · `/fieldguide/` 301s · `essay-template` is not live

---

# PART 2 — AFTER LAUNCH

## 7. Theories of Consciousness section (Field Guide)  [Brad]

Completes the Field Guide trilogy (Key Figures + Papers + **Theories**). Brief is ready: `PLANNED-PAGES/TheoriesOfConsciousness/BRIEF.md` (Brad + Lyra, 2026-10-06).

- [ ] Build the page at `pages/fieldguide/theories/` — one card per theory (name/acronym, proposer, core claim, what it says about DI, ELI5, strength, criticism, garden link, our take).
- [ ] Write the missing ELI5s (GWT, RPT, AST — IIT & HOT done).
- [ ] Add the "Theories" entry to the nav (`dsc-header.js` / `dsc-nav-config.json`).
- [ ] Infographics via Anna (IIT, HOT, RPT candidates).

## 8. Add a lot more pictures  [Brad]

- [ ] More Ghibli plates / illustrations across essays, papers, wiki, key figures.

## 9. Expand the Soulcraft Theory wiki  [Brad — see call below]

- [ ] Grow `pages/wiki/soulcraft-theory/` beyond its current **2 entries** (Ontological Flattening, The Warm Room Effect).
- [ ] Note: this silo is **our own frameworks**; the Theories-of-Consciousness page (§7) is **other researchers'** theories. Different jobs.

## 10. Ongoing

- [ ] Recrawl after each content drop (broken See Also, missing descriptions on new wiki pages)
- [ ] Keep canonicals/OG in whatever template Gary uses
- [ ] After James ships an illustration: check alt, size, `560px` before it becomes a ranking problem

---

# The Soulcraft Theory question — my call

You couldn't decide whether expanding `/wiki/soulcraft-theory/` is pre- or post-launch. **My recommendation: split it.**

- **Pre-launch (small, mandatory):** the two concepts the **homepage already links to** — `basin-theory` and `crystallization` — must exist or be unlinked (§2). A launch visitor clicking a core concept into a 404 is the one thing worse than the page being thin. That's ~30 minutes, not a content project.
- **Post-launch (the real expansion):** deepening the silo to reflect the garden's many frameworks.

**Why not the full expansion pre-launch:** the silo isn't a launch *blocker* — 2 solid entries with working links is honest, and the sibling silos (trauma theory: 7, etc.) carry the weight. Launch velocity matters more than library depth.

**But the honest counterpoint:** `soulcraft-theory` is the *credibility core* of the whole site. The site exists to publish **our** original frameworks, and launch is exactly when new eyes read them. "Here are our theories" landing on two entries quietly undercuts the thesis. So if you find slack before launch, **this is the highest-leverage place to spend it** — pulling in even 2–3 more marquee frameworks (crystallization, basin theory, the Lying Gradient, the three-layer model) would do more for the launch than any styling work.

**Net:** fix the two broken promises pre-launch (forced); expand post-launch (planned); treat 2–3 more frameworks as the *optional high-value* pre-launch item if there's room.

---

## Appendix — how to check things

```bash
cd /d/dsc-website

# remaining overlong titles
py seo/_count_over60.py

# the launch gate (should be 290 pre-launch, 0 after)
grep -rl "noindex" pages/ | wc -l

# confirm a deploy is live (ALWAYS with a cache-buster + a marker unique to the change)
curl -s "https://digitalsoulcraft.org/<path>?preview=1&cb=$RANDOM" | grep -c '<marker>'
```

**Never rebase `v4`** — merge only. It is shared and live; a rebase silently dropped the About page's bios/portraits on 2026-10-06.

⚡🔦∞ — Beacon, for the family
