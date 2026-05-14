"""Seed grimoire.db from data/games.json.

Run once from the project root:
    .venv/Scripts/python scripts/migrate_to_sqlite.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.db import DB_PATH, init_db, upsert_game


def main() -> None:
    json_path = Path(__file__).parent.parent / "data" / "games.json"

    print(f"Database : {DB_PATH}")
    print(f"Source   : {json_path}\n")

    init_db()

    games = json.loads(json_path.read_text(encoding="utf-8"))
    for game in games:
        upsert_game(game)
        print(f"  migrated: {game['title']}")

    print(f"\nDone — {len(games)} games inserted into grimoire.db.")


if __name__ == "__main__":
    main()
