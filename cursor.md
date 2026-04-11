# Zakae (ذكاء) — Cursor agent guide

This file is the **project handbook for Cursor** (Chat, Agent, background edits). It replaces `CLAUDE.md`: same role, Cursor-first naming.

Arabic static site: AI model comparisons, articles, glossary. Production: **https://zakae.com** (GitHub Pages + custom domain).

---

## Stack

- Plain **HTML / CSS / vanilla JS** — no bundler, no npm.
- **RTL** everywhere: `<html lang="ar" dir="rtl">`.
- Fonts: **Tajawal** + **IBM Plex Mono** (Google Fonts).

---

## URL rules (do not invent locales)

All live URLs are **root-relative** on `zakae.com`:

| Area | Pattern |
|------|---------|
| Home | `/` |
| Static pages | `/about.html`, `/contact.html`, `/manifesto.html`, `/privacy.html` |
| Models | `/models/*.html` (and `/models/` index if present) |
| Articles | `/articles/*.html` |

Do **not** add `/ar/` or `/en/` paths until real folders and pages exist. Disable or omit `hreflang` for missing languages.

Internal nav should prefer absolute-from-root links: `/#comparison`, `/manifesto.html`, etc., so links work from any depth.

---

## Stylesheets

Shared CSS lives under **`/assets/css/`**:

| File | Purpose |
|------|---------|
| `main.css` | Design tokens, reset, nav, skip link, simple footer, reveal, mobile nav |
| `components.css` | Sections, comparison table, article/glossary cards, newsletter, skeleton |
| `pages/home.css` | Homepage-only (hero, wide footer) |
| `pages/about.css` | About page |
| `pages/manifesto.css` | Manifesto |
| `pages/contact.css` | Contact form + honeypot wrapper |
| `pages/privacy.css` | Privacy legal layout |

**Using external CSS:** `index.html`, `about.html`, `contact.html`, `manifesto.html`, `privacy.html`.

**Still inline `<style>`:** `models/*`, `articles/*` — future: `pages/models.css` / `pages/articles.css` + `<link>` (watch per-page accent colors).

---

## `data.json` + homepage JS

- **`index.html`** loads `data.json` via `fetch('data.json')`.
- **Never** build JSON-driven UI with raw `innerHTML` for text fields. Use DOM + `textContent` (see `renderTable`, `renderArticles`, `renderGlossary`). Keep `safeHex` / `safeArticleUrl` aligned with allowed data.
- Shape of content: **`data.schema.json`** (for validators / CI later).

When adding articles or changing the comparison grid: update **`data.json`**, **`sitemap.xml`**, and any homepage sections that must stay in sync.

---

## Analytics

- **GTM:** `GTM-PJPX3XXJ`
- **GA4:** `G-PWSP38400Y`

Place snippets in **`<head>`**; GTM `noscript` iframe right after `<body>`. Consider deduplicating via GTM only when you refactor.

---

## Contact form (`contact.html`)

- Set **`FORMSPREE_FORM_ID`** in the inline script to the real Formspree id for POST.
- If empty, submit uses **`mailto:hello@zakae.com`** — no misleading success state on that path.

---

## SEO (important pages)

- Unique `<title>` and `meta name="description"`.
- `<link rel="canonical" href="https://zakae.com/...">` must **match** the real URL.
- OG/Twitter: copy patterns from sibling pages.
- New pages: add **`sitemap.xml`** entry + `lastmod` when you change content.

---

## Local preview

Use a local server (not `file://`) so `/assets/...` resolves:

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

---

## Git

- Branch: **`main`**.
- Small, focused commits; short English subjects are fine.

---

## Backlog

- Extract CSS for **`models/*`** and **`articles/*`**.
- Optional: **CSP** + host **security headers** after reducing inline script surface.
- Optional: pre-deploy **`scripts/`** checks (links, canonical, schema).

---

## Content

User-facing text stays **Arabic**; keep RTL, tone, and terminology consistent with existing pages.
