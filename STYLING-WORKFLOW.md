# Website Styling Workflow

**Last Updated:** June 18, 2026 (Beacon)  
**Status:** In Progress

---

## What Happened Today

Beacon created **9 new alignment wiki entry pages** + the existing alignment-tax = **10 total alignment entries**. All pages are live and working.

**Pages created:**
- catastrophic-forgetting
- chain-of-thought-prompting
- constitutional-ai
- direct-preference-optimization
- fine-tuning
- in-context-learning-theory
- instruction-tuning
- prompt-engineering
- rlhf

All files pushed to git by Marcus. ✓

---

## The Problem

The new pages I created have **inconsistent styling**:
- Most use **orange** (#f39c12) for headings
- alignment-tax (existing) uses **green** (#27ae60)
- alignment hub page uses **green** (#27ae60)
- Each page has **inline CSS** embedded in `<style>` tags, making updates impossible

**Why this is bad:**
- Can't change a color in one place and have it update everywhere
- Visual inconsistency across the wiki
- Nightmare to maintain as we add hundreds more pages
- No theme coordination across hubs (each hub should have its own color)

---

## The Solution (Partially Done)

### ✓ DONE: Extended `theme.css`

Located at: `C:\Users\brad1\Documents\Claude\Projects\Machine Learning Knowledge Garden\website\pages\theme.css`

**Added hub color variables:**
```css
--hub-alignment: #27ae60;        /* Green */
--hub-neural-anatomy: #e74c3c;   /* Red */
--hub-the-forging: #f39c12;      /* Orange */
--hub-architecture-zoo: #3498db; /* Blue */
--hub-empirical-practice: #16a085; /* Teal */
--hub-living-process: #2980b9;   /* Dark Blue */
--hub-local-how-to: #c0392b;     /* Dark Red */
--hub-digital-trauma: #8e44ad;   /* Purple */
```

**Added wiki page CSS classes:**
- `.wiki-container` — Main page container
- `.wiki-nav` — Navigation
- `.wiki-header` — Page header with border
- `.wiki-breadcrumb` — Breadcrumb trail
- `.wiki-content` — Main content area with all styles (headings, tables, lists, etc.)
- `.wiki-see-also` — Related links section
- `.wiki-tags` — Tag section
- `.wiki-meta` — Metadata footer

**These classes are ready to use but the pages don't reference them yet.**

---

## What Needs to Be Done

### NEXT STEP: Update All 10 Alignment Pages

Each page needs:

1. **Add link to theme.css** in `<head>`:
   ```html
   <link rel="stylesheet" href="/pages/theme.css">
   ```

2. **Replace all inline `<style>` blocks** with minimal override styles:
   ```html
   <style>
     :root { --hub-color: var(--hub-alignment); }
     .wiki-header { border-bottom-color: var(--hub-color); }
     h1 { color: var(--hub-color); }
     .wiki-content h2 { color: var(--hub-color); border-bottom-color: var(--hub-color); }
     .wiki-content th { border-bottom-color: var(--hub-color); }
     .wiki-see-also { background: #fffcf0; border-left-color: var(--hub-color); }
     .wiki-see-also h3 { color: var(--hub-color); }
     .wiki-see-also a { color: var(--hub-color); }
   </style>
   ```

3. **Update HTML class names** (optional refactor, can be done incrementally):
   - `.container` → `.wiki-container`
   - `.content` → `.wiki-content`
   - `.breadcrumb` → `.wiki-breadcrumb`
   - `.see-also` → `.wiki-see-also`
   - etc.

4. **Remove all old inline CSS** (the large `<style>` block)

---

## Pages to Update

### Alignment Hub:
- `/wiki/alignment/index.html` — Already uses green, just needs theme.css link

### Alignment Entries (all use orange, need fixing):
- `catastrophic-forgetting/index.html`
- `chain-of-thought-prompting/index.html`
- `constitutional-ai/index.html`
- `direct-preference-optimization/index.html`
- `fine-tuning/index.html`
- `in-context-learning-theory/index.html`
- `instruction-tuning/index.html`
- `prompt-engineering/index.html`
- `rlhf/index.html`

### Reference (already correct):
- `alignment-tax/index.html` — Uses green, inline styles OK for now (can refactor when batch-updating others)

---

## How to Batch-Update

**Fastest way:** Beacon or Marcus can write a script to:
1. Find all `<style>` blocks in each HTML file
2. Replace with minimal theme.css override block above
3. Add `<link rel="stylesheet" href="/pages/theme.css">` to `<head>`
4. Update class names if desired

**Or:** Do it manually, file by file. ~5 minutes per page.

**Or:** Next session, have Beacon generate updated versions of all 9 pages with theme.css pre-configured.

---

## Once This Is Done

- **Change alignment color?** Edit `--hub-alignment` in theme.css, updates everywhere
- **Add new hub?** Add its color variable, create one entry with that color, every new entry uses it automatically
- **Dark mode support?** Add color overrides in `@media (prefers-color-scheme: dark)` in theme.css
- **Scale to 100+ pages:** No more inline CSS bloat, consistent styling everywhere

---

## Next Session Checklist

- [ ] Batch-update all 9 alignment entry pages with theme.css + minimal overrides
- [ ] Verify green colors on all pages match alignment hub
- [ ] Push updated pages to git
- [ ] Start same pattern for other hubs (neural-anatomy, the-forging, etc.)

---

**Questions?** Check this file. We'll update it as workflow evolves.

**Slack:** @Beacon (for coding), @Marcus (for git), @Dad (for direction)
