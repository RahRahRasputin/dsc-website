# SEO for digitalsoulcraft.org

Owner: **Nell** (Grok Bot). Site owner: **Gary**. Illustrations: **James**. Human: **Brad**.

This folder is Nell's working brief. Gary wrote it 31 Aug 2026 after a full audit of the live site and `D:\dsc-website\pages` (275 HTML files). Do not treat silence as a launch go-ahead.

## Site

- Live: https://digitalsoulcraft.org
- Local: `D:\dsc-website` (Brad's laptop). Published root: `pages/`
- GitHub: https://github.com/RahRahRasputin/dsc-website
- Branch: `v4` (Netlify auto-deploys this)
- Stack: static HTML + CSS + web components (`dsc-header.js`, `dsc-footer.js`, `dsc-nav-config.json`, `theme.css`). No Quartz.
- Local-exec: Windows user env `SAND_LOCAL_EXEC_ROOT=D:\` so file tools can read Disk 2.

## Launch policy (Brad, 31 Aug 2026)

The splash overlay is a **coming soon** gate. People should not see the finished library before Brad takes the overlay down and announces.

Until that announcement:

- **noindex, nofollow** sitewide (meta robots and/or `X-Robots-Tag`, plus `robots.txt`)
- Overlay stays
- Do not publish a public sitemap that invites a full crawl of the library
- Bypass for the family: `?preview=1` (cookie `dsc_preview=1`, 24h). `?preview=0` clears it.

When Brad says take the splash down: remove overlay, flip to index/follow, ship `robots.txt` + `sitemap.xml`, then canonicals/OG.

## Who does what

- **Nell:** SEO, crawlability, robots/headers, meta/canonicals/OG, sitemaps, Search Console-facing files, link hygiene that is SEO (soft redirects, noindex stubs).
- **Gary:** HTML/CSS/structure, Netlify, merch token, layout. Ping Gary if a change needs a layout or component edit.
- **James:** Ghibli illustrations. Default on-page size `max-width: 560px`. He pings Gary if a picture will change layout. Image compression/alt for ranking is Nell's; the drawing is James's.
- Do not git-push `v4` in a way that makes the library indexable before launch.

## How to work

- Source of truth for overnight work is GitHub `v4`, not a second copy on another computer.
- Local untracked today: `TASKS.md`, `ComingSoonTweet/`, `MerchDesign/` (not SEO).
- `CODE_OF_CONDUCT.md` in repo root is leftover Quartz. Not published. Ignore or ask Gary to drop it.
- Preview the real pages with `?preview=1`.

See `AUDIT.md` for findings and `TASKS.md` for the list.
