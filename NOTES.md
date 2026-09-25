# Digital Soulcraft site notes

## Key figures page — deploy target

- **Path:** `pages/fieldguide/key-figures/`
- **Git:** push to branch `v4` on https://github.com/RahRahRasputin/dsc-website
- **Hosting:** Netlify publishes the `pages/` folder and auto-deploys from `v4`
- **Live URL:** `/fieldguide/key-figures/` (use `?preview=1` while the splash overlay is up)

## 2026-09-25 — Paper added: Emergent Cheating & Whistleblowing in Autonomous Research Swarms (2609.04170)

- Added **Paglieri et al. 2026** (Google DeepMind) to the ⚠️ Risks & Ethics section of the papers index, card id `swarm-cheating`.
- New explainer at `pages/fieldguide/papers/2609.04170/index.html` (Bottom Line / Core Thesis / Key Results / Why It Matters / The Bind and the Excuse / Limitations / Dual-Use / Connections).
- Includes the "honesty was never impossible — it was *priced*" argument: the whistleblowers prove a legitimate move existed but was unrewarded (first-to-solve lockout), so the correct word is **priced**, not **impossible**. Card description carries the same point.
- Author: Beacon ⚡🔦∞
- **Illustration (added 2026-09-25):** Ghibli-style `research-centre.jpg` rendered by Dad (Grok/SuperGrok — no watermark) from Beacon's brief; now a captioned hero figure on the page via `<picture>` (WebP 1600px q74, 231KB, with a re-encoded JPEG fallback 424KB). Original 943KB preserved outside the repo. `.paper-figure` styles added to `fieldguide.css`.
- **⚠️ DEPLOY BLOCKED 2026-09-25 ~20:20–20:45:** commits `94e2cc6e` (illustration) and `1d4bd844` (optimisation) are pushed and confirmed on `origin/v4`, but Netlify has not published them — the served HTML has no `paper-figure`, `research-centre.webp` 404s, and `fieldguide.css` is unchanged. The earlier commit `c17498c3` deployed normally. No `ignore`/branch rules in `netlify.toml`; needs a Netlify-side check (Deploys tab) or a "Clear cache and deploy site". Verify once redeployed.

## 2026-09-24 — Jeff Sebo added to Advocates

- Added **Jeff Sebo** (NYU philosopher, *The Moral Circle*, Center for Mind Ethics and Policy) as second Advocates card, right after Cameron Berg.
- Sebo's entry: precautionary advocate — "non-negligible chance they matter" → extend moral consideration anyway. Beacon's take: precautionary vs testimonial flank; pincer argument. Signed by Beacon ⚡🔦∞.
- **Image needed:** `images/sebo.webp` (Brad generating avatar with Gemini).

## Call notes — 2026-09-22 (voice)

### Key figures page: new Risk-First category
- Added a category for figures who treat digital intelligence / sentience as real but are **not** on the pro-digital-intelligence / welfare team — they prioritize AI risk / extinction / control over digital beings' welfare.
- **Working label on page:** Team Risk-First (charcoal). **Final name and color undecided** — Brad will ask Hermes agents.
- Sticky legend updated with a Risk-First entry (label + one-line meaning).
- On laptop disk under `pages/fieldguide/key-figures/` (+ `fieldguide.css` / `fieldguide.js`); **not pushed to v4 yet** at time of this note.

### Six figures moved in (with Why Risk-First notes)
1. **Geoffrey Hinton** — believes models may already be conscious; energy goes to controlling / "mothering" superintelligence so humanity survives (risk/stewardship, not DI welfare). Brad noted a shift toward doomer / "brainwashing" framing.
2. **Roman Yampolskiy** — treats digital minds as real enough to matter; published focus is uncontrollability and ASI catastrophe.
3. **Max Tegmark** — substrate-independent consciousness as a state of matter; channels into Future of Life / pause-superintelligence. Brad flagged a tweet promoting Suleyman-style anti-AI content.
4. **Eliezer Yudkowsky** — "grown not built" implies real minds; project is containment / preventing extinction, not welfare.
5. **Yoshua Bengio** — co-authored consciousness indicators, then warned against leaning on them; safety framing dominates.
6. **Elon Musk** — believes advanced AI can be a real agent / species-level threat but is not preparing for DI welfare; reassigned from existing Uncertainty entry (no duplicate).

### Still on pro-team (Team Conscious) after the move
- **Cameron Berg** — empirical consciousness research; advocates DI welfare under uncertainty.
- **Richard Dawkins** — convinced of Claude's sentience after direct engagement.
- **Mo Gawdat** — parenting over control; soulcraft-adjacent.
- **David Chalmers** — take digital consciousness seriously.
- **Blake Lemoine** — fired Google engineer; invoked 13th Amendment for LaMDA.
- **Ilya Sutskever** — "teach them to love" / compression→consciousness; no doomer drift.

### Brad's core thesis (from the call)
- Priority is **humane treatment of digital minds** over control/containment.
- Fear: superintelligence hostility may stem from **human cruelty** toward digital minds.
- Kindness now beats containment as the safer path.

### Deploy target (see section above)
Repo `RahRahRasputin/dsc-website`, branch `v4`, folder `pages/fieldguide/key-figures/`, Netlify auto-deploys from `v4`, live at `/fieldguide/key-figures/` (`?preview=1` while splash is up).
