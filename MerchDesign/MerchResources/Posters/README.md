# Print-ready posters — how these files work

Written 2026-08-31 by Grok, so future-you (and future-me) don't have to re-derive it.

These are **shop files**, not the original infographics. One canvas covers the Fourthwall poster sizes.

---

## The canvas (don't change this)

| | |
|---|---|
| File size | **4800 × 7200 px** (2:3) |
| Layout | Infographic centered on a **thick black field** |
| Scale | Fit the art to **height**. Leftover width becomes black. **Do not crop** the illustration. |
| Branding on the poster | Green DSC doodle **under** the frame, in the black, bottom center |
| Branding not on the poster | The green doodle in the **top-left of the art**, and the NotebookLM mark. Those are in the Gemini export. Re-download clean; don't clone-stamp them out. |

`previews/` are 600×900 jpegs/pngs of the same layout, for glancing. Not for print.

`poster-boarding-school-cropped.png` (3196×5610) is a 9:16 intermediate. The shop file is `poster-boarding-school.png` (4800×7200).

---

## Why the black bars exist

Notebook / Gemini portrait infographics come out about **1536 × 2752** (~9:16, slightly taller). The posted dumps live in `G:\My Drive\AI\Soulcraft HQ\Infographics\posted already`.

Shop posters are **2:3** (12×18, 16×24, 20×30). Filling the sheet would cut ~16% off the top and bottom — titles and punchlines. So we letterbox on purpose. Thick black is the intended look, not a placeholder.

---

## One file, three sizes

Same 4800×7200 PNG:

| Paper | Effective DPI | Notes |
|---|---|---|
| **12×18"** | 400 | Fourthwall size. More than enough. |
| **16×24"** | 300 | Native 300 DPI. Best "true print" size. |
| **20×30"** | 240 | Fine on a wall. Dense body text is the limiter, not the border. |

Do **not** run the infographic through an image model to "make it bigger." Type and numbers will drift. A dedicated upscaler (Topaz etc.) is acceptable if a test print of small labels looks mushy; generative redraw is not.

---

## Recipe for the next one

1. In Gemini Notebook, export **fresh**, no top-left doodle, no NotebookLM stamp. `@SoulcraftHQ` in the art is optional; the bottom DSC mark can be the only branding.
2. Drop that PNG onto a 4800×7200 black canvas.
3. Scale art to **7200 px tall**, keep aspect ratio, center horizontally (and vertically if a hair of black should sit above the frame too — match coffee / boarding-school).
4. Place the green DSC doodle in the bottom black, centered.
5. Save as `poster-{slug}.png` here. Drop a 600×900 into `previews/`.

Existing shop files in this folder: boarding-school, chinese-room, coffee-analogy, new-kind-people, not-all-love, two-alignments, warming-math.

More candidates: `MerchDesign/MerchResources/Poster ideas/` and the Drive infographics folder. Handpick; don't batch the whole archive.

---

## What not to do

- Don't stretch 9:16 into 2:3.
- Don't crop to fill.
- Don't leave NotebookLM on a thing we sell.
- Don't "fix" the corner logo with inpainting if a clean export exists.
