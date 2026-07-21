#!/usr/bin/env python3
"""
مُولّد صفحة القاموس المرجعية (glossary.html) من data.json.

يبني صفحة ثابتة قابلة للفهرسة (SEO)، منظّمة حسب الفئة والمستوى، بطبقات
لجماهير متنوعة (مبتدئ / ممارس / متقدم). المصدر الوحيد للحقيقة هو data.json —
أعد التشغيل بعد أي تعديل على المصطلحات.

الاستخدام:  python3 scripts/build_glossary.py
"""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://zakae.com"

CATEGORY_TITLES = {
    "foundation": "الأساسيات",
    "interaction": "التفاعل والاستخدام",
    "architecture": "البنية والتقنية",
    "training": "التدريب والتعلّم",
    "capability": "القدرات",
    "agents": "الوكلاء الأذكياء",
    "evaluation": "القياس والتقييم",
    "deployment": "التشغيل والنشر",
    "risk": "المخاطر والموثوقية",
}
CATEGORY_ORDER = list(CATEGORY_TITLES.keys())

DIFFICULTY = {
    "beginner": ("مبتدئ", "#1a9f5a"),
    "intermediate": ("متوسط", "#d98a00"),
    "advanced": ("متقدم", "#c0392b"),
}


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def build() -> str:
    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    terms = data.get("glossary", [])

    # تجميع حسب الفئة مع الحفاظ على ترتيب منطقي
    groups: dict[str, list] = {}
    for t in terms:
        groups.setdefault(t.get("category", "foundation"), []).append(t)
    ordered_cats = [c for c in CATEGORY_ORDER if c in groups] + [
        c for c in groups if c not in CATEGORY_ORDER
    ]

    # أقسام المصطلحات
    sections = []
    for cat in ordered_cats:
        cards = []
        for t in groups[cat]:
            label, color = DIFFICULTY.get(t.get("difficulty", ""), ("", "#666"))
            badge = (
                f'<span class="gl-badge" style="background:{color}">{esc(label)}</span>'
                if label
                else ""
            )
            cards.append(
                f"""      <article class="glossary-card" id="term-{esc(t.get('id',''))}">
        <div class="gl-head"><span class="glossary-term">{esc(t.get('term',''))}</span>{badge}</div>
        <div class="glossary-arabic">{esc(t.get('arabic',''))}</div>
        <p class="glossary-def">{esc(t.get('definition',''))}</p>
      </article>"""
            )
        sections.append(
            f"""    <section class="gl-group" aria-labelledby="cat-{esc(cat)}">
      <h2 class="gl-group-title" id="cat-{esc(cat)}">{esc(CATEGORY_TITLES.get(cat, cat))}</h2>
      <div class="glossary-grid">
{chr(10).join(cards)}
      </div>
    </section>"""
        )
    sections_html = "\n\n".join(sections)

    # بيانات منظمة: مجموعة مصطلحات معرّفة
    defined_terms = [
        {
            "@type": "DefinedTerm",
            "name": t.get("term", ""),
            "description": t.get("definition", ""),
            "inDefinedTermSet": f"{BASE_URL}/glossary.html",
        }
        for t in terms
    ]
    termset_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "DefinedTermSet",
            "name": "قاموس مصطلحات الذكاء الاصطناعي بالعربية",
            "url": f"{BASE_URL}/glossary.html",
            "inLanguage": "ar",
            "hasDefinedTerm": defined_terms,
        },
        ensure_ascii=False,
        indent=1,
    )
    breadcrumb_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "قاموس المصطلحات"},
            ],
        },
        ensure_ascii=False,
        indent=1,
    )

    count = len(terms)
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>قاموس مصطلحات الذكاء الاصطناعي بالعربية | ذكاء</title>
  <meta name="description" content="قاموس عربي شامل لأهم مصطلحات الذكاء الاصطناعي — {count} مصطلحاً موضّحاً بلغة واضحة، منظّمة حسب الفئة والمستوى، من LLM وRAG إلى التكميم والوكلاء.">
  <link rel="canonical" href="{BASE_URL}/glossary.html">
  <script type="application/ld+json">
{termset_ld}
  </script>
  <script type="application/ld+json">
{breadcrumb_ld}
  </script>
  <meta property="og:title" content="قاموس مصطلحات الذكاء الاصطناعي بالعربية | ذكاء">
  <meta property="og:description" content="قاموس عربي شامل لأهم مصطلحات الذكاء الاصطناعي، منظّمة حسب الفئة والمستوى.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{BASE_URL}/glossary.html">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/main.css">
  <link rel="stylesheet" href="/assets/css/components.css">
  <style>
    .gl-wrap{{max-width:1100px;margin:auto;padding:0 20px 60px}}
    .gl-tracks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px;margin:32px 0 8px}}
    .gl-track{{background:#fff;border:1px solid #eee;border-radius:14px;padding:22px}}
    .gl-track h3{{margin:0 0 8px;font-size:19px}}
    .gl-track p{{color:#555;font-size:15px;margin:0 0 12px;line-height:1.7}}
    .gl-track a{{color:#0a66c2;text-decoration:none;font-size:15px}}
    .gl-track a:hover{{text-decoration:underline}}
    .gl-group{{margin-top:48px}}
    .gl-group-title{{font-size:24px;border-right:4px solid #0a66c2;padding-right:12px;margin-bottom:20px}}
    .gl-head{{display:flex;align-items:center;justify-content:space-between;gap:10px}}
    .gl-badge{{color:#fff;font-size:12px;font-weight:600;border-radius:999px;padding:3px 10px;white-space:nowrap}}
  </style>
  <script>
  (function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-PJPX3XXJ');
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-PWSP38400Y"></script>
  <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-PWSP38400Y');
  </script>
</head>
<body>
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PJPX3XXJ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

  <a href="#main-content" class="skip-link">انتقل إلى المحتوى الرئيسي</a>

  <nav role="navigation" aria-label="القائمة الرئيسية">
    <div class="nav-inner">
      <a href="/" class="nav-logo" aria-label="ذكاء — الصفحة الرئيسية">ذكاء<span class="ac">.</span><span class="dot" aria-hidden="true"></span></a>
      <ul class="nav-links" id="nav-links" role="list">
        <li><a href="/#comparison">المقارنة</a></li>
        <li><a href="/#articles">المقالات</a></li>
        <li><a href="/glossary.html" class="active">المصطلحات</a></li>
        <li><a href="/manifesto.html">البيان</a></li>
        <li><a href="/about.html">عن الموقع</a></li>
        <li><a href="/contact.html" class="nav-cta">تواصل</a></li>
      </ul>
      <div class="nav-right">
        <div class="lang-switcher" role="group" aria-label="اختيار اللغة">
          <a href="/glossary.html" class="lang-btn active" aria-current="page">AR</a>
          <span class="lang-btn disabled" aria-label="الإنجليزية قريباً">EN</span>
        </div>
        <button class="hamburger" id="hamburger" type="button" aria-label="فتح القائمة" aria-expanded="false" aria-controls="nav-links">
          <span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span>
        </button>
      </div>
    </div>
  </nav>

<main id="main-content">

  <header class="page-hero" role="banner">
    <span class="page-tag">قاموس المصطلحات</span>
    <h1>قاموس مصطلحات الذكاء الاصطناعي بالعربية</h1>
    <p>{count} مصطلحاً موضّحاً بلغة عربية واضحة — منظّمة حسب الفئة والمستوى، لتخدم المبتدئ والممارس وصانع القرار.</p>
  </header>

  <div class="gl-wrap">

    <section class="gl-tracks" aria-label="مسارات حسب مستواك">
      <div class="gl-track">
        <h3>🌱 للمبتدئ</h3>
        <p>ابدأ بالمفاهيم الجوهرية قبل الغوص في التفاصيل.</p>
        <a href="/articles/how-to-choose-ai-model.html">كيف تختار نموذج الذكاء الاصطناعي المناسب؟ ←</a>
      </div>
      <div class="gl-track">
        <h3>🛠️ للممارس والمطوّر</h3>
        <p>مصطلحات التطبيق العملي: الموجّهات، الاسترجاع، الواجهات.</p>
        <a href="/articles/prompt-engineering-guide.html">هندسة الموجّهات: الدليل العملي ←</a>
      </div>
      <div class="gl-track">
        <h3>🧭 لصانع القرار</h3>
        <p>ما يهمّك: الخصوصية، التكلفة، الموثوقية، والاختيار.</p>
        <a href="/articles/open-vs-closed-models.html">النماذج المفتوحة مقابل المغلقة ←</a>
      </div>
    </section>

{sections_html}

  </div>

</main>

<footer class="simple-footer" role="contentinfo">
  <div class="footer-bottom">
    <p class="footer-copy" id="footer-copy"></p>
    <div class="footer-links">
      <a href="/">الرئيسية</a>
      <a href="/privacy.html">سياسة الخصوصية</a>
    </div>
  </div>
</footer>

<script>
  document.getElementById('footer-copy').textContent = `© ${{new Date().getFullYear()}} ذكاء — zakae.com`;
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('nav-links');
  function closeNav(){{navLinks.classList.remove('nav-open');hamburger.classList.remove('is-open');hamburger.setAttribute('aria-expanded','false')}}
  hamburger.addEventListener('click',()=>{{const isOpen=navLinks.classList.contains('nav-open');if(isOpen){{closeNav()}}else{{navLinks.classList.add('nav-open');hamburger.classList.add('is-open');hamburger.setAttribute('aria-expanded','true')}}}});
  navLinks.querySelectorAll('a').forEach(l=>l.addEventListener('click',closeNav));
  window.addEventListener('resize',()=>{{if(window.innerWidth>700)closeNav()}});
</script>
</body>
</html>
"""


def main() -> None:
    out = ROOT / "glossary.html"
    out.write_text(build(), encoding="utf-8")
    n = len(json.loads((ROOT / "data.json").read_text(encoding="utf-8")).get("glossary", []))
    print(f"✓ تم توليد glossary.html بـ {n} مصطلحاً")


if __name__ == "__main__":
    main()
