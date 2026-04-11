# CLAUDE.md — Zakae (ذكاء)

## Overview

Arabic static reference site for AI models. Live: https://zakae.com

**Stack:** static HTML, shared CSS under `/assets/css/`, vanilla JS. No build step.

**URL model (root only — no `/ar/` or `/en/` until those trees exist):**

- `/` — home
- `/about.html`, `/contact.html`, `/manifesto.html`, `/privacy.html`
- `/models/*.html`, `/articles/*.html`

**Content data:** `data.json` is loaded by `index.html` via `fetch('data.json')`. Editorial shape is described in `data.schema.json` (JSON Schema for validation tooling later).

**Contact form:** set `FORMSPREE_FORM_ID` in `contact.html` when Formspree is ready. If empty, submit opens `mailto:hello@zakae.com` with a prefilled message (no fake “sent” state).

## CSS layout

| File | Role |
|------|------|
| `assets/css/main.css` | Variables, reset, nav, simple footer, reveal, keyframes |
| `assets/css/components.css` | Sections, cards, comparison table, glossary, newsletter, skeleton |
| `assets/css/pages/home.css` | Homepage-only (hero, site footer grid) |
| `assets/css/pages/about.css` | About page |
| `assets/css/pages/manifesto.css` | Manifesto |
| `assets/css/pages/contact.css` | Contact form |
| `assets/css/pages/privacy.css` | Privacy legal prose |

**Still inline CSS:** `models/*`, `articles/*` (migrate to `pages/models.css` / `pages/articles.css` in a follow-up).

## Security (homepage)

Dynamic blocks from `data.json` are built with `createElement` / `textContent`, not `innerHTML`. Colors in the comparison table use `safeHex()`. Article URLs use `safeArticleUrl()`.

## SEO

- `canonical` on each page must match the real deployed path under `https://zakae.com/...`.
- `sitemap.xml` should list every published HTML URL (exclude templates).
- No `hreflang` for locales that do not exist.

## Analytics

Google Tag Manager (`GTM-PJPX3XXJ`) and GA4 (`G-PWSP38400Y`) are embedded in pages that include analytics. Prefer managing duplicates via GTM when you refactor.

## Local preview

```bash
python -m http.server 8000
```

Open `http://localhost:8000` so `/assets/...` paths resolve.
