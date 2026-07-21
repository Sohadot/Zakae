#!/usr/bin/env python3
"""
بوابة الجودة لموقع ذكاء (zakae.com)
Quality gate — governance enforcement for the Zakae static site.

يفحص المصداقية والاتساق التقني و SEO والأمن الأساسي قبل أي دمج.
Runs with the standard library only (no npm, no bundler). Exit code 1 on any error.

الاستخدام:  python3 scripts/quality_gate.py
"""

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://zakae.com"

# صفحات مستثناة من فحص SEO/الخريطة (قوالب وملفات تحقّق)
EXCLUDE_BASENAMES = {"article-template.html"}
EXCLUDE_PREFIXES = ("google",)  # ملفات تحقّق Search Console

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def is_excluded(rel: str) -> bool:
    base = os.path.basename(rel)
    return base in EXCLUDE_BASENAMES or base.startswith(EXCLUDE_PREFIXES)


def content_pages() -> list[str]:
    pages = []
    for p in ROOT.rglob("*.html"):
        if ".git" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if is_excluded(rel):
            continue
        pages.append(rel)
    return sorted(pages)


def expected_canonical(rel: str) -> str:
    """رابط canonical المتوقّع وفق أعراف الموقع: index داخل مجلد = مسار المجلد بشرطة مائلة."""
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel.endswith("/index.html"):
        return f"{BASE_URL}/{rel[:-len('index.html')]}"
    return f"{BASE_URL}/{rel}"


def strip_canonical(raw: str) -> str:
    return raw.strip().rstrip("/ ").strip() or "/"


# ---------------------------------------------------------------- فحص الصفحات
def check_pages() -> dict[str, str]:
    """يعيد خريطة: canonical(بلا شرطة أخيرة) -> rel، لاستخدامها في فحص الخريطة."""
    canon_map: dict[str, str] = {}
    for rel in content_pages():
        html = (ROOT / rel).read_text(encoding="utf-8")

        # 1) RTL + لغة عربية
        if not re.search(r'<html[^>]*\blang="ar"', html):
            err(f'{rel}: ينقص lang="ar" في وسم <html>')
        if not re.search(r'<html[^>]*\bdir="rtl"', html):
            err(f'{rel}: ينقص dir="rtl" في وسم <html>')

        # 2) عنوان غير فارغ
        m = re.search(r"<title>\s*(.*?)\s*</title>", html, re.S)
        if not m or not m.group(1).strip():
            err(f"{rel}: <title> مفقود أو فارغ")

        # 3) وصف ميتا غير فارغ
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
        if not m or not m.group(1).strip():
            err(f"{rel}: meta description مفقود أو فارغ")

        # 4) canonical صحيح ومطابق للمسار الفعلي
        m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
        if not m:
            err(f"{rel}: رابط canonical مفقود")
        else:
            got = strip_canonical(m.group(1))
            want = strip_canonical(expected_canonical(rel))
            if got != want:
                err(f"{rel}: canonical غير مطابق (المتوقّع {want} / الموجود {got})")
            canon_map[want] = rel

        # 5) بيانات منظمة JSON-LD صالحة وموجودة
        blocks = re.findall(
            r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
            html,
            re.S,
        )
        if not blocks:
            err(f"{rel}: تنقص بيانات منظمة JSON-LD (SEO)")
        for i, b in enumerate(blocks):
            try:
                json.loads(b)
            except json.JSONDecodeError as e:
                err(f"{rel}: JSON-LD رقم {i + 1} غير صالح ({e})")

        # 6) أمن — منع مصادر XSS الخطرة (دفاع في العمق)
        for sink in ("innerHTML", "outerHTML", "document.write", "eval("):
            if sink in html:
                err(f"{rel}: استخدام محتمل غير آمن لـ «{sink}» — استخدم textContent/DOM")

    return canon_map


# ---------------------------------------------------------------- فحص البيانات
def check_data() -> None:
    data_path = ROOT / "data.json"
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"data.json: غير صالح ({e})")
        return

    schema_path = ROOT / "data.schema.json"
    required = ["site", "models", "articles", "glossary"]
    if schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            required = schema.get("required", required)
        except json.JSONDecodeError:
            warn("data.schema.json: غير صالح — يُتجاهل")
    for key in required:
        if key not in data:
            err(f"data.json: ينقص المفتاح المطلوب «{key}»")

    # حقول إلزامية للعناصر
    for i, mdl in enumerate(data.get("models", [])):
        for f in ("id", "slug", "name"):
            if not mdl.get(f):
                err(f"data.json: models[{i}] ينقص «{f}»")
    for i, g in enumerate(data.get("glossary", [])):
        for f in ("id", "term", "arabic", "definition"):
            if not g.get(f):
                err(f"data.json: glossary[{i}] ينقص «{f}»")

    # 🔒 ثابت المصداقية: أرقام الصفحة الرئيسية تطابق المحتوى الفعلي
    stats = data.get("homepage", {}).get("stats", [])
    counts = {"نماذج": len(data.get("models", [])), "مصطلح": len(data.get("glossary", []))}
    for st in stats:
        label, val = st.get("label", ""), str(st.get("value", ""))
        for kw, real in counts.items():
            if kw in label and val.strip("+").isdigit():
                claimed = int(val.strip("+"))
                if claimed > real:
                    err(
                        f"data.json: إحصائية «{label}» تدّعي {claimed} والمحتوى الفعلي {real} "
                        f"(ثغرة مصداقية)"
                    )


# ---------------------------------------------------------------- فحص الخريطة
def check_sitemap(canon_map: dict[str, str]) -> None:
    sm_path = ROOT / "sitemap.xml"
    if not sm_path.exists():
        err("sitemap.xml مفقود")
        return
    sm = sm_path.read_text(encoding="utf-8")
    listed = {strip_canonical(u) for u in re.findall(r"<loc>\s*(.*?)\s*</loc>", sm)}

    # كل صفحة محتوى يجب أن تكون في الخريطة
    for want, rel in canon_map.items():
        if want not in listed:
            err(f"sitemap.xml: الصفحة «{rel}» غير مدرجة ({want})")

    # كل رابط في الخريطة يجب أن يشير لصفحة موجودة
    valid = set(canon_map.keys())
    for u in listed:
        if u not in valid:
            err(f"sitemap.xml: الرابط «{u}» لا يقابل صفحة محتوى فعلية (رابط ميّت)")


# ---------------------------------------------------------- فحص الروابط الداخلية
def check_internal_links() -> None:
    for rel in content_pages():
        html = (ROOT / rel).read_text(encoding="utf-8")
        for href in re.findall(r'href="(/[^"#?]*)', html):
            target = href.split("#")[0].split("?")[0]
            if target in ("", "/"):
                continue
            fs = ROOT / target.lstrip("/")
            if target.endswith("/"):
                ok = (fs / "index.html").exists()
            elif "." in os.path.basename(target):
                ok = fs.exists()
            else:
                ok = fs.exists() or (fs / "index.html").exists() or (
                    ROOT / (target.lstrip("/") + ".html")
                ).exists()
            if not ok:
                err(f"{rel}: رابط داخلي مكسور → {target}")


def check_glossary_page() -> None:
    """صفحة القاموس المولّدة يجب أن تعكس كل مصطلحات data.json (تزامن المصدر)."""
    page = ROOT / "glossary.html"
    if not page.exists():
        return  # اختيارية: تُبنى عبر scripts/build_glossary.py
    html = page.read_text(encoding="utf-8")
    try:
        terms = json.loads((ROOT / "data.json").read_text(encoding="utf-8")).get("glossary", [])
    except json.JSONDecodeError:
        return
    for t in terms:
        term = str(t.get("term", "")).strip()
        if term and term not in html:
            err(
                f"glossary.html: المصطلح «{term}» غير ظاهر — أعد التوليد "
                f"(python3 scripts/build_glossary.py)"
            )


def check_orphans() -> None:
    """لا صفحة محتوى بلا روابط داخلية واردة (منع الجزر المعزولة). الرئيسية مستثناة."""
    pages = content_pages()
    indeg: dict[str, int] = {p: 0 for p in pages}
    for rel in pages:
        html = (ROOT / rel).read_text(encoding="utf-8")
        seen = set()
        for href in re.findall(r'href="(/[^"#?]*)', html):
            target = href.split("#")[0].split("?")[0].lstrip("/")
            if not target:
                cand = "index.html"
            elif target.endswith("/"):
                cand = target + "index.html"
            elif (ROOT / target).exists():
                cand = target
            elif (ROOT / (target + ".html")).exists():
                cand = target + ".html"
            else:
                continue
            if cand in indeg and cand != rel:
                seen.add(cand)
        for c in seen:
            indeg[c] += 1
    for rel, deg in indeg.items():
        if rel != "index.html" and deg == 0:
            err(f"{rel}: صفحة يتيمة — لا روابط داخلية واردة (اربطها من صفحة ذات صلة)")


def main() -> int:
    canon_map = check_pages()
    check_data()
    check_sitemap(canon_map)
    check_internal_links()
    check_glossary_page()
    check_orphans()

    print(f"صفحات محتوى مفحوصة: {len(content_pages())}")
    if warnings:
        print(f"\n⚠️  تنبيهات ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"\n❌ أخطاء الحوكمة ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print("\nالبوابة: فشل. عالج الأخطاء أعلاه قبل الدمج.")
        return 1
    print("\n✅ البوابة: نجاح. كل الفحوص اجتازت.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
