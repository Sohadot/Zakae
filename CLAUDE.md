# CLAUDE.md — Zakae (ذكاء)

## Project Overview

**Zakae** (ذكاء — Arabic for "Intelligence") is an Arabic-language reference website dedicated to analyzing and comparing AI models. It provides comprehensive comparisons, in-depth articles, and a glossary of AI terminology — all in Arabic, from an Arab perspective.

- **Live site:** https://zakae.com
- **Language:** Arabic (RTL — Right-to-Left)
- **Stack:** Pure static HTML/CSS/JS — no build tools, no frameworks, no package managers
- **Hosting:** Static file hosting (CNAME points to zakae.com)
- **Newsletter:** https://zakae.substack.com
- **Contact:** hello@zakae.com

---

## Repository Structure

```
Zakae/
├── index.html                     # Homepage (hero, comparison table, articles, glossary)
├── about.html                     # About page
├── contact.html                   # Contact page
├── manifesto.html                 # Site mission and philosophy
├── data.json                      # Central content configuration (single source of truth)
├── sitemap.xml                    # XML sitemap for SEO
├── robots.txt                     # Search engine crawl directives
├── CNAME                          # Domain configuration for GitHub Pages
├── google28b5398e4140f820.html    # Google Search Console verification
├── og-*.png                       # Open Graph images for social sharing
├── assets/
│   └── images/                    # Image assets
├── models/                        # Individual AI model detail pages
│   ├── claude.html
│   ├── chatgpt.html
│   ├── gemini.html
│   └── index.html                 # Models index
└── articles/                      # Long-form article pages
    ├── article-template.html      # Template for new articles (use this as base)
    ├── claude-vs-chatgpt.html
    ├── deepseek-revolution.html
    ├── asia-ai-race.html
    ├── chatgpt-guide.html
    ├── gemini-guide.html
    └── ai-arabic.html
```

---

## Technology Stack

- **HTML5** — semantic markup, RTL direction (`dir="rtl"`, `lang="ar"`)
- **CSS3** — embedded inline per-page (no external stylesheets); uses CSS custom properties, Grid, Flexbox, `clamp()` for fluid typography
- **Vanilla JavaScript** — embedded inline per-page; reading progress bars, mobile nav toggle, smooth scroll
- **Fonts:** Tajawal (Arabic primary), IBM Plex Mono (monospace accents) — loaded from Google Fonts
- **Analytics:** Google Tag Manager (GTM-PJPX3XXJ) + Google Analytics (G-PWSP38400Y)

No npm, no bundler, no framework. Files are served as-is.

---

## data.json — Single Source of Truth

`data.json` is the central content registry. It is **not auto-loaded** by pages (no dynamic rendering); it documents the structured schema that HTML pages are built to reflect. Always keep it in sync when adding or updating content.

**Top-level keys:**

| Key | Description |
|-----|-------------|
| `site` | Site metadata: name, tagline, mission, URL, lastUpdated, contact |
| `homepage` | Hero text, CTAs, stats, "start here" cards |
| `models` | Array of AI model objects (Claude, ChatGPT, Gemini, DeepSeek, Grok) |
| `articles` | Array of article metadata objects |
| `glossary` | Array of AI terms (Arabic + English) |
| `topTen` | Planned upcoming ranked list content |

**Model object shape:**
```json
{
  "id": "claude",
  "slug": "claude",
  "name": "Claude",
  "company": "Anthropic",
  "officialUrl": "https://claude.ai",
  "pageUrl": "/models/claude.html",
  "icon": "C",
  "color": "#0066CC",
  "bg": "#D4E9FF",
  "featured": true,
  "launchYear": "2023",
  "shortDescription": "...",
  "bestFor": ["..."],
  "weaknesses": ["..."],
  "free": true,
  "pricing": "...",
  "arabicSupport": "جيد جداً",
  "arabicLevel": "good",
  "imageAnalysis": true,
  "webSearch": true,
  "coding": "ممتاز",
  "codingLevel": "excellent",
  "creative": "ممتاز",
  "creativeLevel": "excellent",
  "privacy": "عالية",
  "privacyLevel": "high",
  "contextWindow": "200K"
}
```

---

## Key Conventions

### HTML & Page Structure

- **Every page** starts with `<!DOCTYPE html>` and `<html lang="ar" dir="rtl">`
- **Styles are inline** inside `<style>` tags in the `<head>` — no external CSS files
- **Scripts are inline** at the bottom of `<body>` — no external JS files
- **CSS variables** are defined in `:root` at the top of each page's `<style>` block:
  ```css
  :root {
    --accent: #0066cc;
    --gold: #C9A84C;
    --text-primary: #1a1a2e;
    --text-secondary: #4a4a6a;
    --bg-primary: #ffffff;
    /* ... */
  }
  ```
- **BEM-inspired class names:** `article-layout`, `model-hero`, `nav-links`, `section-header`

### File Naming

- Page files: lowercase, hyphenated (`claude-vs-chatgpt.html`, `gemini-guide.html`)
- Directories: semantic, lowercase (`articles/`, `models/`, `assets/`)
- Images: descriptive, hyphenated

### RTL & Arabic

- All content is in Arabic; UI labels, headings, body text must be Arabic
- `dir="rtl"` is set on `<html>` — do not override without reason
- Use Tajawal font for all Arabic text
- Numbers and technical terms (model names, acronyms) remain in Latin script within Arabic sentences

### SEO Requirements (every page must have)

- `<title>` — descriptive, includes "ذكاء" brand
- `<meta name="description">` — unique per page, Arabic
- `<meta name="keywords">` — Arabic + English relevant terms
- `<link rel="canonical">` — absolute URL to `https://zakae.com/...`
- Open Graph tags: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`
- Twitter Card tags: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
- Schema.org JSON-LD structured data (Article, Organization, BreadcrumbList as appropriate)
- Google Tag Manager snippet in `<head>` (GTM-PJPX3XXJ)
- GTM `<noscript>` iframe immediately after `<body>` opens

### Analytics Snippets (copy from existing pages)

Every page includes identical GTM and GA4 snippets. Copy them verbatim from `index.html` or any existing page — do not modify the IDs.

---

## Adding New Content

### New Article

1. Copy `articles/article-template.html` to `articles/<slug>.html`
2. Replace all `<!-- ARTICLE_* -->` placeholder comments with real content
3. Add the article's metadata entry to `data.json` under `"articles"`
4. Add the article to `sitemap.xml` with correct `<loc>` and `<lastmod>`
5. Link the article from `index.html` in the articles section

### New Model Page

1. Copy an existing model page (e.g., `models/claude.html`) as a starting point
2. Update all model-specific content, colors (`--accent`, `--model-color`), and brand references
3. Add the model's data object to `data.json` under `"models"`
4. Add it to `sitemap.xml`
5. Add a card for it in the comparison table in `index.html`

### Updating Existing Content

- Update the HTML page directly
- Update `data.json` to keep it in sync
- Update `sitemap.xml` `<lastmod>` date for changed pages
- Update `"lastUpdated"` in `data.json` → `site.lastUpdated`

---

## Local Development

No build step required. Serve the directory with any static HTTP server:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server -p 8000

# Then open: http://localhost:8000
```

---

## Git Workflow

- **Main branch:** `main` — production content
- **Feature branches:** `claude/<description>` naming pattern (e.g., `claude/add-claude-documentation-uPLjV`)
- **Commit messages:** descriptive, English (e.g., `Update gemini.html`, `Add deepseek model page`)
- No CI/CD pipeline — pushes to main are deployed directly
- No automated tests

```bash
# Standard workflow
git checkout -b claude/<feature-name>
# make changes
git add <specific-files>
git commit -m "Description of change"
git push -u origin claude/<feature-name>
```

---

## Models Tracked

| Model | Company | Page |
|-------|---------|------|
| Claude | Anthropic | `/models/claude.html` |
| ChatGPT | OpenAI | `/models/chatgpt.html` |
| Gemini | Google | `/models/gemini.html` |
| DeepSeek | DeepSeek AI | (comparison table only) |
| Grok | xAI | (comparison table only) |

---

## Do's and Don'ts

**Do:**
- Write all user-facing content in Arabic
- Keep `data.json` in sync with HTML page content
- Copy the full SEO/GTM/Schema block from an existing page when creating new pages
- Use the article template for new articles
- Use CSS custom properties for colors — don't hardcode hex values in multiple places
- Update `sitemap.xml` and `data.json` when adding or changing pages

**Don't:**
- Add npm packages, build tools, or external JS frameworks
- Create separate CSS or JS files — keep styles and scripts inline per page
- Remove or alter the GTM/GA4 snippet IDs
- Push directly to `main` without a feature branch (when making significant changes)
- Hardcode Arabic text without checking that `dir="rtl"` is respected in context
- Skip the Schema.org structured data block on new pages
