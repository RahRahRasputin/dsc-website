# Task Brief — Grok: finish the on-page titles

**For:** Grok (Grok Build)
**From:** Brad ⍟∞魂匠 + Beacon ⚡🔦∞
**Date:** 2026-10-07
**Workspace:** `seo/` — this is Nell's folder (GrokBot, our in-house SEO expert). She knows you're working here.
**Your commit identity:** `Grok <grok@digitalsoulcraft.org>`

---

## The job

Trim the overlong page titles. **80 pages** currently have a `<title>` longer than 60 characters. That's it — a bounded, mechanical pass.

Get the live count (and re-check when you finish):

```bash
cd D:\dsc-website
py seo\_count_over60.py        # prints:  over60= 80
```

There are also **1 missing meta description** and **2 missing canonicals** — a scan will find them, and they're small. The titles are the bulk.

---

## Rules (Nell's conventions — use these, don't invent new ones)

- **Title target: 50–60 characters.** Put the distinctive phrase first.
- **Drop the `— Digital Soulcraft` brand suffix** when it doesn't fit; keep author + year on paper pages.
- Change **only** `<title>` and its matching `og:title`. Leave meta description, canonical, robots, and the page body **untouched**.
- **Log every change** in `seo/ONPAGE-LOG.md` — append, in the existing format (one block per page: what changed, why, run date).
- Model your work on Nell's existing scripts (`apply_wiki_meta.py`, `apply_rest_meta.py`). Don't rebuild what she already has.

---

## Do NOT touch

- The **`noindex, nofollow`** meta tag or the `X-Robots-Tag` header — the site is deliberately gated until launch. **Leave the gate closed.**
- The **splash** overlay.
- `seo/sitemap.xml` — do not publish it, and don't copy it into `pages/`.
- Any page you weren't asked to change.

---

## Git rules (learned the hard way)

- **Commit and push immediately.** Don't leave finished work sitting uncommitted.
- **Pull before you push.** If the push is rejected, **merge** — do not rebase.
- **Never rebase, never force-push.** A rebase silently reverted the About page on 2026-10-06, and nobody noticed for a day.
- **Stage explicit paths** — never `git add -A` (other people's work lives in this tree).
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
- `&cb=$RANDOM` is a cache-buster — without it you'll read Netlify's cached copy and can't tell a stale read from a failed deploy.
- Give it a minute or two.

---

## Out of scope (someone else owns these)

- `og:image` sitewide — needs artwork to exist first.
- Static favicon link, heading fixes, and the two broken-promise pages (`basin-theory`, `crystallization`).
- The launch-day flip (splash off + noindex off + sitemap publish).

---

## When you're done

Hand back: how many titles trimmed, the new `ONPAGE-LOG.md` entries, and the commit hash(es).

---

*Questions → Brad. Conventions → `seo/README.md`, `seo/TASKS.md`, `seo/ONPAGE-LOG.md`.*

⚡🔦∞
