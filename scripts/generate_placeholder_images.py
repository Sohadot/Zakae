"""Generate minimal OG/hero placeholder images so local and deploy paths resolve."""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets" / "images"
ASSETS = ROOT / "assets"

# (path relative to ROOT, size, bg_rgb, accent_rgb)
PNG_SPECS = [
    (IMG / "chatgpt-guide-og.png", (1200, 630), (26, 26, 28), (26, 140, 60)),
    (IMG / "grok-explained-2026.png", (1200, 630), (18, 18, 22), (99, 102, 241)),
    (IMG / "grok-model-analysis-2026.png", (1200, 630), (18, 18, 22), (99, 102, 241)),
    (IMG / "claude-model-analysis-2026.png", (1200, 630), (245, 248, 252), (0, 102, 204)),
    (IMG / "deepseek-model-analysis-2026.png", (1200, 630), (15, 23, 42), (59, 130, 246)),
    (IMG / "deepseek-explained-2026.png", (1200, 630), (15, 23, 42), (59, 130, 246)),
    (IMG / "chatgpt-vs-gemini-2026.png", (1200, 630), (250, 250, 248), (42, 92, 143)),
    (IMG / "ai-agents-explained-2026.png", (1200, 630), (250, 250, 248), (45, 122, 79)),
    (IMG / "claude-vs-chatgpt-hero-2026.png", (1200, 630), (250, 250, 248), (184, 134, 11)),
    (IMG / "og-grok-explained-2026.png", (1200, 630), (18, 18, 22), (99, 102, 241)),
    (IMG / "og-deepseek-explained-2026.png", (1200, 630), (15, 23, 42), (59, 130, 246)),
    (IMG / "og-ai-agents-explained-2026.png", (1200, 630), (250, 250, 248), (45, 122, 79)),
    (IMG / "og-chatgpt-vs-gemini-2026.png", (1200, 630), (250, 250, 248), (42, 92, 143)),
    (IMG / "og-claude-model-2026.png", (1200, 630), (245, 248, 252), (0, 102, 204)),
    (IMG / "og-deepseek-model-2026.png", (1200, 630), (15, 23, 42), (59, 130, 246)),
    (IMG / "og-grok-model-2026.png", (1200, 630), (18, 18, 22), (99, 102, 241)),
    (IMG / "og-claude-vs-chatgpt-2026.png", (1200, 630), (250, 250, 248), (184, 134, 11)),
]

ROOT_OG = [
    (ASSETS / "og-image.png", (1200, 630), (26, 25, 22), (184, 134, 11)),
    (ASSETS / "og-chatgpt-guide.png", (1200, 630), (26, 26, 28), (26, 140, 60)),
    (ASSETS / "og-gemini-guide.png", (1200, 630), (248, 250, 252), (37, 99, 235)),
    (ASSETS / "og-asia-ai-race.png", (1200, 630), (254, 242, 242), (185, 28, 28)),
    (ASSETS / "og-chatgpt-model.png", (1200, 630), (26, 26, 28), (26, 140, 60)),
    (ASSETS / "og-ai-arabic.png", (1200, 630), (250, 250, 248), (42, 92, 143)),
    (ASSETS / "og-deepseek-revolution.png", (1200, 630), (15, 23, 42), (59, 130, 246)),
]


def draw_band(im: Image.Image, accent: tuple[int, int, int]) -> None:
    w, h = im.size
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, int(h * 0.72), w, h], fill=accent)


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)

    for path, size, bg, accent in PNG_SPECS + ROOT_OG:
        im = Image.new("RGB", size, bg)
        draw_band(im, accent)
        path.parent.mkdir(parents=True, exist_ok=True)
        im.save(path, "PNG", optimize=True)

    for name, bg, accent in (
        ("gemini-main-hero-2026.jpg", (248, 250, 252), (37, 99, 235)),
        ("gemini-ai-analysis-2026.jpg", (248, 250, 252), (37, 99, 235)),
    ):
        im = Image.new("RGB", (1200, 630), bg)
        draw_band(im, accent)
        im.save(IMG / name, "JPEG", quality=88, optimize=True)

    print("Wrote", len(PNG_SPECS) + len(ROOT_OG), "PNG + 2 JPEG")


if __name__ == "__main__":
    main()
