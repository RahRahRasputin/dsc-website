# 🎯 Ad Slides — Dashboard

Each subfolder = one skyscraper ad campaign. Everything about that ad lives in its folder.

## How to add an ad

1. Create a new folder: `slides/your-campaign-name/`
2. Drop in the ad image as `slide.webp` (or `.svg`)
3. Write a `readme.md` with:
   - **Target URL** — where the ad links to
   - **Campaign notes** — what it's promoting, dates, etc.
4. Add it to `/dsc-ads-config.json`

That's it. The ad rotator picks it up sitewide.

## How to remove an ad

Delete the folder and remove its entry from `dsc-ads-config.json`.

## Current slides

| Folder | Image | Links to | Status |
|--------|-------|----------|--------|
| `merch-placeholder/` | `slide.svg` | `/merch/` | Placeholder |

---

*The rotator reads `/dsc-ads-config.json` — update that file when adding/removing slides.*