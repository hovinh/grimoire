"""
Download and crop board game cover images from BoardGameGeek.
Saves 600x450 (4:3) JPEG files to data/images/{game_id}.jpg
and patches image_path into data/games.json.

Run from the project root:
    .venv/Scripts/python scripts/fetch_images.py
"""

import io
import json
import sys
import time
from pathlib import Path

import requests
from PIL import Image

PROJECT_ROOT = Path(__file__).parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "games.json"
OUT_DIR = PROJECT_ROOT / "data" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_W, TARGET_H = 600, 450  # 4:3 aspect ratio

HEADERS = {
    "User-Agent": "GrimoireApp/1.0 (personal board-game GM tool; educational, non-commercial)"
}

WIKI_API = "https://en.wikipedia.org/w/api.php"

# Wikipedia article titles for each game
WIKI_TITLES: dict[str, str] = {
    "codenames": "Codenames_(board_game)",
    "ticket-to-ride": "Ticket to Ride (board game)",
    "pandemic": "Pandemic_(board_game)",
    "catan": "Catan",
    "terraforming-mars": "Terraforming Mars (board game)",
    "gloomhaven": "Gloomhaven",
}


def fetch_wiki_image_url(title: str) -> str:
    r = requests.get(
        WIKI_API,
        params={
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "pithumbsize": 800,
            "pilicense": "any",
            "format": "json",
        },
        headers=HEADERS,
        timeout=15,
    )
    r.raise_for_status()
    pages = r.json()["query"]["pages"]
    page = next(iter(pages.values()))
    thumb = page.get("thumbnail", {}).get("source")
    if not thumb:
        raise ValueError(f"No thumbnail found on Wikipedia for '{title}'")
    return thumb


def center_crop_and_save(img_url: str, game_id: str) -> str:
    r = requests.get(img_url, headers=HEADERS, timeout=30)
    r.raise_for_status()

    img = Image.open(io.BytesIO(r.content)).convert("RGB")
    w, h = img.size

    target_ratio = TARGET_W / TARGET_H
    src_ratio = w / h

    if src_ratio > target_ratio:
        # Image is wider than 4:3 → trim the sides
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Image is taller than 4:3 → trim top/bottom
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    out_path = OUT_DIR / f"{game_id}.jpg"
    img.save(out_path, "JPEG", quality=90)
    return str(out_path.relative_to(PROJECT_ROOT)).replace("\\", "/")


def main() -> None:
    with open(DATA_FILE, encoding="utf-8") as f:
        games: list[dict] = json.load(f)

    game_map = {g["id"]: g for g in games}

    for game_id, wiki_title in WIKI_TITLES.items():
        print(f"\n[{game_id}]")
        try:
            img_url = fetch_wiki_image_url(wiki_title)
            print(f"  source : {img_url}")
            rel_path = center_crop_and_save(img_url, game_id)
            print(f"  saved  : {rel_path}  ({TARGET_W}x{TARGET_H})")
            if game_id in game_map:
                game_map[game_id]["image_path"] = rel_path
        except Exception as exc:
            print(f"  ERROR  : {exc}", file=sys.stderr)

        time.sleep(1)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)

    print("\ngames.json updated with image_path entries.")


if __name__ == "__main__":
    main()
