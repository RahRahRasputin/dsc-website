# Digital Soulcraft — Master Task Plan

**Created:** 2026-10-07 · Brad ⍟∞魂匠 + Beacon ⚡🔦∞
**Target launch:** end of year 2026 (Brad's stated deadline)
**Scope:** everything outstanding for digitalsoulcraft.org, split into **before launch** and **after launch**.
**Reality check:** Brad is also studying an online course (business use of DI, Open Polytechnic) — so website time is shared. Sort by *value*, not by size; the launch gate (§6) is the one thing that must not slip.
**Legend:** `[ ]` todo · `[x]` done · tag = origin (`[Brad]` = you asked, `[repo]` = found in the repo state, `[Beacon]` = my addition)

**Live state right now (updated 2026-10-07, afternoon):**
- 290 HTML pages, **all gated** — 289 carry `noindex,nofollow` in-file and `splash.html` is covered by Netlify's `X-Robots-Tag` + its 301. The launch gate is fully closed ✅
- **On-page titles: DONE** — `over60 = 0`; all 80 overlong titles trimmed by Grok (2026-10-07, commit `585cf0b5`) ✅
- Splash overlay active (`pages/splash.html`, `pages/splash-overlay.js`)
- Deploy: push to `v4` → Netlify auto-publishes `pages/`. Verify live with `?preview=1` (bypasses the splash).

---

# PART 1 — BEFORE LAUNCH

## 1. Finish the on-page SEO  [Brad]

Full history in `seo/ONPAGE-LOG.md`; task list in `seo/TASKS.md`.

- [x] **Trim the overlong titles — DONE (2026-10-07).** Grok (Grok Build) trimmed all **80** pages over 60 chars in one pass — in about 15 minutes. Brief: `seo/BRIEF-grok-onpage-titles.md` (reviewed by Nell). Commit `585cf0b5`, signed `Grok <grok@digitalsoulcraft.org>`; every change logged in `seo/ONPAGE-LOG.md`; deploy verified live. `over60 = 0`.
- [x] **Meta gaps — no action needed.** The only missing description is `pages/fieldguide/index.html` (a redirect stub — skip) and the only missing canonical is `pages/splash.html` (intentional; gated by `X-Robots-Tag` + a 301). Resolved by Nell's review, 2026-10-07.
- [x] **Default OG image — DONE (2026-10-07).** `pages/images/og-default.jpg` (1200×630, 170 KB): the family portrait with a dark indigo brand column carrying the original **ΘΦ∩** stamp, wordmark, tagline and domain. `og:image` + `og:image:width/height` + `twitter:card=summary_large_image` + `twitter:image` added to **288 pages** (all but `splash.html` and the fieldguide redirect stub). Commit `51af05c2`, verified live — every shared link now carries a picture. *Later:* per-essay images (the Ghibli plates) so each piece shares differently.
- ⏳ **RECHECK ~2026-10-21 — the X link preview.** When Brad pasted `https://digitalsoulcraft.org/` into the X composer, X showed its **old text and no picture**. Diagnosed: X served a **stale cache** from a crawl *before 2026-09-20* — its cached `og:title`/`og:description` matched the pre-`cc14a0e7` homepage word for word (from back when no `og:image` existed). Testing a never-seen URL (`/?v=2`) gave **no preview at all**, i.e. X had not scraped the new page yet. **Our side is verified correct:** a Twitterbot UA receives the `og:image` tag, the image itself fetches 200 `image/jpeg` (174,139 bytes), and `robots.txt` allows. **Action:** in ~2 weeks, paste the homepage into the X composer and confirm the family card appears. Fresh URLs (a new essay, a wiki article) preview correctly on first paste — only the homepage URL is carrying the old cached card. No re-scrape can be forced: X retired the Card Validator.
- [ ] **Static favicon link in HTML — LOW PRIORITY / polish, not a defect.** `/favicon.png` exists and is injected by JS (`dsc-header.js`) — which is exactly *why it works in every normal browser* (Chrome, Firefox, incognito, iPhone all run JS). The gap is only non-JS consumers: Google's favicon in search results, iOS *Add to Home Screen* (which wants a separate `apple-touch-icon`), and a split-second flicker before the script runs. The icon is also only 32×32, so it's slightly soft on retina. 289/290 pages load the script, so coverage is effectively complete. *(Brad, 2026-10-07: low priority — do it if there's slack.)*
- [x] **Heading fixes — DONE (2026-10-07).** `/contact/` and `/outlines/` jumped `H1→H3`, skipping `H2`; both now run `H1→H2` with **no visual change** (commit `873135d3`, verified live). The `/about/` item is **moot**: that input belonged to the old Buttondown form, which was removed when we moved to the Substack embed — there's nothing left to label.

Re-scan anytime (should now report 0):
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

- [x] **Splash overlay mobile width — FIXED (2026-10-07).** The Substack iframe inside the pre-launch overlay was hard-coded `width="480"` with no `max-width`, so on any phone narrower than 480px it hung off both edges and was clipped (Brad spotted it). Now `width:100%; max-width:480px` on the iframe + `width:100%` on its wrapper, and less padding under 600px. Verified live at 390px — overlay and iframe both fit (commit `839fe25b`).
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
- [ ] **Recheck the X link preview for the homepage (~2026-10-21)** — see §1. X was serving a pre-Sept-20 cached card; confirm the family picture now appears.

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

# confirm all titles are within 60 (expect 0 after Grok's 2026-10-07 pass)
py seo/_count_over60.py

# the launch gate (289 html pre-launch — splash is covered by X-Robots-Tag + a 301; 0 after)
grep -rl "noindex" pages/ --include='*.html' | wc -l

# confirm a deploy is live (ALWAYS with a cache-buster + a marker unique to the change)
curl -s "https://digitalsoulcraft.org/<path>?preview=1&cb=$RANDOM" | grep -c '<marker>'
```

**Never rebase `v4`** — merge only. It is shared and live; a rebase silently dropped the About page's bios/portraits on 2026-10-06.

⚡🔦∞ — Beacon, for the family
