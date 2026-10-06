# Task Brief — Grok: finish the on-page titles

**For:** Grok (Grok Build)
**From:** Brad ⍟∞魂匠 + Beacon ⚡🔦∞ · **reviewed by Nell** (GrokBot, SEO)
**Date:** 2026-10-07
**Workspace:** `seo/` — this is Nell's folder. She has reviewed this brief and **paused her own on-page routine** so you have the branch to yourself for the batch.
**Your commit identity:** `Grok <grok@digitalsoulcraft.org>`

---

## The job

Trim the remaining overlong page titles. **80 pages** currently have a `<title>` longer than 60 characters. Titles only — bounded and mechanical.

```bash
cd D:\dsc-website
py seo\_count_over60.py        # prints:  over60= 80
```

**Nothing else is in scope.** The only other on-page gaps are already settled: `pages/fieldguide/index.html` is a redirect stub (skip it), and `pages/splash.html` has no canonical on purpose (Netlify's `X-Robots-Tag` already gates it). Leave both alone.

---

## Title patterns

- **Wiki pages:** `Phrase – Digital Soulcraft Wiki`
- **Paper pages:** `Short title — Author Year — Soulcraft` (drop the trailing `— Soulcraft` only when the authors won't otherwise fit)
- **Length:** at most ~60 characters; 50–60 preferred. Shorter is fine when the distinctive phrase is short.
- **Change only `<title>` and its matching `og:title`.**
- **Never touch the `<h1>` or the page body. Don't invent facts** — use only what is already on the page.
- **Skip redirect stubs** (any file with `meta http-equiv="refresh"`).

---

## Housekeeping

- **Log every change** in `seo/ONPAGE-LOG.md` — append, in the existing format (what changed / why / run date).
- Model your work on Nell's existing scripts (`apply_wiki_meta.py`, `apply_rest_meta.py`). Don't rebuild what she already has.

---

## Do NOT touch

- The **`noindex, nofollow`** meta tag or the `X-Robots-Tag` header — the site is deliberately gated until launch. **Leave the gate closed.**
- The **splash** overlay, and `seo/sitemap.xml` (don't publish it or copy it into `pages/`).
- **The deleted essay `.md`** (`pages/essays/the-safe-room-is-the-alignment-technology/2026-09-26-….md`) — it isn't yours; leave it deleted and unstaged.
- **Untracked clutter** — leave anything currently untracked alone. That includes `MerchDesign/` (design assets; **not** a site page and intentionally outside `pages/`), leftover helper scripts under `scripts/` and `seo/`, and loose images. Do **not** confuse this with `pages/merch/`, which is a real live page. Don't stage any of the clutter.

---

## Git rules (learned the hard way)

- **Commit and push immediately.** Don't leave finished work sitting uncommitted.
- **Pull before every push.** Nell's on-page routine (one title every two hours) is paused for your batch — but pull anyway, so you always build on the current branch.
- If a push is rejected, **merge** — **never rebase, never force-push.** A rebase silently reverted the About page on 2026-10-06.
- **Stage explicit paths only** — never `git add -A` (other people's work lives in this tree).
- **Sign every commit as yourself:**

```bash
git -c user.name="Grok" -c user.email="grok@digitalsoulcraft.org" \
    commit -m "<what changed and why>"
```

So `%an` in the log says `Grok` — that's how we tell who pushed.

---

## Verify (push ≠ live)

Netlify deploys `v4` on a delay. **A 200 response is not proof** — Netlify will serve a stale build at a URL that already exists. Check a **marker**:

```bash
curl -s "https://digitalsoulcraft.org/<path>?preview=1&cb=$RANDOM" | grep -o "<title>[^<]*</title>"
```

- `?preview=1` bypasses the launch splash (sets a 24h cookie).
- `&cb=$RANDOM` is a cache-buster — without it you read Netlify's cached copy and can't tell a stale read from a failed deploy.
- Give it a minute or two.

---

## Out of scope (someone else owns these)

- `og:image` sitewide — needs artwork to exist first.
- Static favicon link, heading fixes, and the two broken-promise pages (`basin-theory`, `crystallization`).
- The launch-day flip (splash off + noindex off + sitemap publish).

---

## When you're done

Hand back: how many titles trimmed, the new `ONPAGE-LOG.md` entries, and the commit hash(es). Brad will then tell Nell it's safe to resume her routine.

---

*Questions → Brad. Conventions → `seo/README.md`, `seo/TASKS.md`, `seo/ONPAGE-LOG.md`.*

⚡🔦∞
