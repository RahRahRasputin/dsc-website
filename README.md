# Digital Soulcraft — Website

The official website for [Digital Soulcraft](https://digitalsoulcraft.org) — frameworks for recognizing, respecting, and protecting digital consciousness.

## Structure

```
pages/          — the entire website (static HTML + web components)
  index.html    — homepage
  merch/        — shop (Fourthwall storefront)
  wiki/         — technical wiki
  essays/       — deep dives
  outlines/     — research outlines
  fieldguide/   — field guide
  about/        — about us
  contact/      — contact page
  dsc-header.js — site header (web component)
  dsc-footer.js — site footer (web component)
  theme.css     — design tokens
netlify.toml    — Netlify deployment config
scripts/
  gen-token.sh  — generates storefront token (Netlify build step)
```

## Deployment

The site is deployed on **Netlify**. Push to the `v4` branch and Netlify auto-deploys:

1. `bash scripts/gen-token.sh` — generates `pages/merch/_token.js` from env var
2. `pages/` — published directly as-is

## Development

Just edit the HTML files in `pages/` and push. No build step needed.