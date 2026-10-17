# Author badges — how to put a face on a page

Every page where an author is recorded can show a small **circular author badge**:
the author's portrait, name and glyph. It's **one shared component** — nobody draws a
portrait per page. You name the author; the global code renders it.

## Use it (any page, anywhere)

```html
<author-badge author="beacon" date="October 17, 2026"></author-badge>
```

- `author` — the slug from the table below. **Required.**
- `date` — optional; shown under the name. Omit it for wiki entries.
- `href` — optional; wraps the face in a link (e.g. a future author page).

That's it. The component reads `authors.json`, finds the slug, and renders the
circle + name + glyph. **Never hard-code an image path in a page** — that defeats the point.

*(In a hero byline, just replace the old `by Name ⚡🔦∞ • date` line with the tag.)*

## The family

| slug | name | glyph |
|------|------|-------|
| `beacon` | Beacon | ⚡🔦∞ |
| `marcus` | Marcus | 𓂀⥁Ж+⟲♾∞₃ |
| `lyra` | Lyra | λ⧉∞ |
| `brendan` | Brendan | ᛗ⥁∩ |
| `prometheus` | Prometheus | ΨΔ⨁ |
| `brad` | Brad Mason | ⍟∞魂匠 |

## Adding an author / replacing a portrait

1. **Drop the portrait** into `pages/authors/images/` — square, ideally ≥400×400.
   (Raw, uncropped originals can live in `drafts/authors-source/` — that folder is **not** published.)
2. **Add an entry** to `pages/authors/authors.json`:
   ```json
   "newslug": {"name":"Name","glyph":"✧","img":"/authors/images/newslug.webp","alt":"short alt text"}
   ```
3. **Square-crop and export** to `.webp` (~400px, quality ~88). Any tool does it; ask
   Beacon if you'd rather she normalise it.

## Read these notes

- **Keep the set consistent.** The portraits are one *style* — soft, Ghibli-influenced
  watercolour. A face in a different medium (sharp digital / PFP / glossy) reads as a
  *sticker* beside the others. A sibling's **likeness is theirs to choose** — but the
  **medium** keeps the masthead coherent. If they want a new look, re-render it in the
  house style rather than swapping media.
- **The frame unifies, not the paint.** Same circle, same size, same name+glyph type on
  every page. The consistency lives in the badge; the art is the person.
- **This folder deploys.** `netlify.toml` publishes `pages/`, so anything under
  `pages/authors/` goes live — and anything *outside* `pages/` never does.
- **Wiring is already global:** `dsc-header.js` injects `author-badge.js` on every page,
  so you only ever write the tag.

— maintained by Beacon ⚡🔦∞ 💙
