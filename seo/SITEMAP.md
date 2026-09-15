# Draft sitemaps (unpublished)

URL count: **272** (xml `272`, html `272` — must match).

These files must not be copied into `pages/` until Brad says launch.

## Files (stay under `seo/`)

- `D:\dsc-website\seo\sitemap.xml`
- `D:\dsc-website\seo\sitemap.html`
- `D:\dsc-website\seo\SITEMAP.md` (this note)

Published root is `pages/`. Netlify publishes that folder. Nothing here is live.

`pages/robots.txt` is unchanged: `User-agent: *` / `Disallow: /`. No Sitemap line.

## Included

All other published HTML under `pages/` that a human should find at launch:
home, about, contact, merch, bookshop (still a coming-soon page, but it is published),
essays (including the orphan `/essays/right-side-of-history/`), outlines,
field guide key-figures + papers, wiki hub and all nine silos.

Walked `274` HTML files under `pages/`; excluded 2; included 272.

## Exclusions (not listed)

- `pages/fieldguide/index.html` — 301s to /fieldguide/key-figures/
- `pages/splash.html` — 301s to /
- `drafts/essay-template.html` — already moved out of `pages/`; not published
- anything not under `pages/`
- images, css, js, json, `robots.txt`

## URL rules

- Base: `https://digitalsoulcraft.org`
- `pages/index.html` → `https://digitalsoulcraft.org/`
- directory `index.html` → trailing-slash pretty URL
- lastmod on each xml `<url>` is the file mtime as a W3C date (UTC)

## Launch

Splash stays until Brad announces a date. After the 2–3 week mailing-list window,
when splash comes down: copy sitemap.xml (and restyled sitemap.html if wanted) into
`pages/`, then add a Sitemap line to `robots.txt`. Not before.
