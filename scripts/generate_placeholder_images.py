"""
Generate styled placeholder cover images (600x450 JPEG) for games that
don't have real box art. Uses PIL to draw a thematic card with title,
subtitle, and a simple geometric motif.

Run from the project root:
    .venv/Scripts/python scripts/generate_placeholder_images.py
"""

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "games.json"
OUT_DIR = PROJECT_ROOT / "data" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 600, 450

# colour palette mirrors the app's dark-navy / gold theme
NAVY   = (22, 33, 62)       # #16213e
GOLD   = (201, 162, 39)     # #c9a227
WHITE  = (240, 236, 220)    # warm off-white
DIM    = (50, 65, 100)      # slightly lighter navy for panels

# Each entry: id, title, subtitle, accent colour, motif key
GAMES = [
    {
        "id":       "moody-bear-kingdom",
        "title":    "Moody Bear\nKingdom",
        "subtitle": "A kingdom of moods & honey",
        "accent":   (220, 140, 40),   # amber
        "motif":    "crown",
    },
    {
        "id":       "lunar-creamery",
        "title":    "Lunar\nCreamery",
        "subtitle": "Artisan scoops on the moon",
        "accent":   (100, 180, 230),  # ice blue
        "motif":    "moon",
    },
    {
        "id":       "moon-leap",
        "title":    "Moon Leap",
        "subtitle": "Race across the lunar surface",
        "accent":   (140, 100, 220),  # violet
        "motif":    "platforms",
    },
]


# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------

def _font(size: int):
    """Return a TrueType font if available, else the PIL default."""
    candidates = [
        "C:/Windows/Fonts/trebucbd.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _font_regular(size: int):
    candidates = [
        "C:/Windows/Fonts/trebuc.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/verdana.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


# ---------------------------------------------------------------------------
# Motif drawers
# ---------------------------------------------------------------------------

def _draw_crown(draw: ImageDraw.ImageDraw, cx: int, cy: int, accent):
    """Simple geometric crown."""
    r = 70
    base_y = cy + 30
    # crown band
    draw.rectangle([cx - r, base_y - 18, cx + r, base_y + 18],
                   fill=accent, outline=WHITE, width=2)
    # three points
    points = [
        (cx - r,   base_y - 18),
        (cx - r,   cy - r + 10),
        (cx - r//2, base_y - 40),
        (cx,       cy - r - 10),
        (cx + r//2, base_y - 40),
        (cx + r,   cy - r + 10),
        (cx + r,   base_y - 18),
    ]
    draw.polygon(points, fill=accent, outline=WHITE)
    # jewels
    for jx in [cx - r + 20, cx, cx + r - 20]:
        draw.ellipse([jx - 8, base_y - 10, jx + 8, base_y + 6],
                     fill=NAVY, outline=WHITE, width=1)


def _draw_moon(draw: ImageDraw.ImageDraw, cx: int, cy: int, accent):
    """Crescent moon."""
    r = 75
    # full circle
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    # bite out to form crescent
    off = int(r * 0.55)
    draw.ellipse([cx - r + off, cy - r, cx + r + off, cy + r], fill=NAVY)
    # small stars
    for sx, sy in [(cx + 35, cy - 60), (cx + 55, cy - 20), (cx + 20, cy + 55)]:
        star_r = 5
        draw.ellipse([sx - star_r, sy - star_r, sx + star_r, sy + star_r],
                     fill=WHITE)


def _draw_platforms(draw: ImageDraw.ImageDraw, cx: int, cy: int, accent):
    """Floating platforms with an arc trajectory."""
    platforms = [
        (cx - 120, cy + 60,  80, 14),
        (cx - 40,  cy + 10,  70, 14),
        (cx + 30,  cy - 40,  60, 14),
        (cx + 95,  cy - 85,  50, 14),
    ]
    for px, py, pw, ph in platforms:
        draw.rounded_rectangle(
            [px, py, px + pw, py + ph],
            radius=6, fill=accent, outline=WHITE, width=2
        )
    # draw a simple explorer dot leaping between platforms 2→3
    ex, ey = cx + 5, cy - 55
    draw.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=WHITE)
    # motion trail
    for i, (tx, ty) in enumerate([(cx - 10, cy - 20), (cx + 0, cy - 38)]):
        alpha_fill = (220, 220, 200, 180 - i * 60)
        r2 = 5 - i
        draw.ellipse([tx - r2, ty - r2, tx + r2, ty + r2], fill=WHITE)


MOTIF_FNS = {
    "crown":     _draw_crown,
    "moon":      _draw_moon,
    "platforms": _draw_platforms,
}


# ---------------------------------------------------------------------------
# Main image builder
# ---------------------------------------------------------------------------

def build_image(game: dict) -> Path:
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    accent = game["accent"]

    # --- outer border ---
    bw = 6
    draw.rectangle([bw, bw, W - bw, H - bw], outline=accent, width=bw)

    # --- inner decorative line ---
    m = 18
    draw.rectangle([m, m, W - m, H - m], outline=(*accent, 80), width=1)

    # --- top label strip ---
    draw.rectangle([0, 0, W, 50], fill=DIM)
    draw.line([(0, 50), (W, 50)], fill=accent, width=2)
    label_font = _font_regular(16)
    draw.text((W // 2, 25), "GRIMOIRE  ·  BOARD GAME COMPANION",
              font=label_font, fill=GOLD, anchor="mm")

    # --- motif in upper centre ---
    motif_fn = MOTIF_FNS.get(game["motif"])
    if motif_fn:
        motif_fn(draw, W // 2, H // 2 - 30, accent)

    # --- title text ---
    title_font = _font(52)
    title_lines = game["title"].split("\n")
    line_h = 60
    total_h = len(title_lines) * line_h
    start_y = H - 140 - (total_h // 2) + 30
    for i, line in enumerate(title_lines):
        y = start_y + i * line_h
        # subtle shadow
        draw.text((W // 2 + 2, y + 2), line, font=title_font,
                  fill=(0, 0, 0), anchor="mm")
        draw.text((W // 2, y), line, font=title_font, fill=WHITE, anchor="mm")

    # --- subtitle ---
    sub_font = _font_regular(20)
    draw.text((W // 2, H - 62), game["subtitle"],
              font=sub_font, fill=GOLD, anchor="mm")

    # --- bottom accent bar ---
    draw.rectangle([0, H - 36, W, H], fill=DIM)
    draw.line([(0, H - 36), (W, H - 36)], fill=accent, width=2)

    out_path = OUT_DIR / f"{game['id']}.jpg"
    img.save(out_path, "JPEG", quality=92)
    return out_path


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    for game in GAMES:
        path = build_image(game)
        rel = path.relative_to(PROJECT_ROOT)
        print(f"  saved: {rel}  ({W}x{H})")

    # patch image_path in games.json (they were already set, but let's confirm)
    with open(DATA_FILE, encoding="utf-8") as f:
        games: list[dict] = json.load(f)

    ids = {g["id"] for g in GAMES}
    updated = 0
    for g in games:
        if g["id"] in ids:
            expected = f"data/images/{g['id']}.jpg"
            if g.get("image_path") != expected:
                g["image_path"] = expected
                updated += 1

    if updated:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(games, f, ensure_ascii=False, indent=2)
        print(f"\ngames.json updated ({updated} image_path entries patched).")
    else:
        print("\ngames.json already up-to-date.")


if __name__ == "__main__":
    main()
