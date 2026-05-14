import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "grimoire.db"

_LIST_FIELDS = (
    "mechanics", "setup", "round_structure",
    "main_actions", "teaching_tips", "strategy_tips",
)


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = _connect()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS games (
            id                 TEXT PRIMARY KEY,
            title              TEXT NOT NULL,
            weight             TEXT NOT NULL,
            bgg_weight         REAL,
            min_players        INTEGER,
            max_players        INTEGER,
            play_time          TEXT,
            image_url          TEXT,
            image_path         TEXT,
            mechanics          TEXT,
            description        TEXT,
            theme              TEXT,
            objective          TEXT,
            setup              TEXT,
            round_structure    TEXT,
            main_actions       TEXT,
            end_game_condition TEXT,
            teaching_tips      TEXT,
            strategy_tips      TEXT
        );

        CREATE TABLE IF NOT EXISTS quiz_questions (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id        TEXT    NOT NULL REFERENCES games(id) ON DELETE CASCADE,
            question_order INTEGER NOT NULL,
            question       TEXT    NOT NULL,
            options        TEXT    NOT NULL,
            answer_index   INTEGER NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def _row_to_game(row: sqlite3.Row) -> dict:
    g = dict(row)
    for field in _LIST_FIELDS:
        raw = g.get(field)
        g[field] = json.loads(raw) if raw else []
    return g


def _get_quiz(conn: sqlite3.Connection, game_id: str) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM quiz_questions WHERE game_id = ? ORDER BY question_order",
        (game_id,),
    ).fetchall()
    return [
        {
            "question": r["question"],
            "options": json.loads(r["options"]),
            "answer_index": r["answer_index"],
        }
        for r in rows
    ]


def get_all_games() -> list[dict]:
    conn = _connect()
    rows = conn.execute("""
        SELECT * FROM games
        ORDER BY CASE weight WHEN 'light' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, title
    """).fetchall()
    games = [_row_to_game(r) for r in rows]
    for game in games:
        game["quiz"] = _get_quiz(conn, game["id"])
    conn.close()
    return games


def get_game(game_id: str) -> dict | None:
    conn = _connect()
    row = conn.execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
    if not row:
        conn.close()
        return None
    game = _row_to_game(row)
    game["quiz"] = _get_quiz(conn, game_id)
    conn.close()
    return game


def upsert_game(game: dict) -> None:
    quiz = game.get("quiz", [])
    data = {k: v for k, v in game.items() if k != "quiz"}
    for field in _LIST_FIELDS:
        data[field] = json.dumps(data.get(field) or [], ensure_ascii=False)

    conn = _connect()
    conn.execute("""
        INSERT INTO games (
            id, title, weight, bgg_weight, min_players, max_players,
            play_time, image_url, image_path, mechanics, description,
            theme, objective, setup, round_structure, main_actions,
            end_game_condition, teaching_tips, strategy_tips
        ) VALUES (
            :id, :title, :weight, :bgg_weight, :min_players, :max_players,
            :play_time, :image_url, :image_path, :mechanics, :description,
            :theme, :objective, :setup, :round_structure, :main_actions,
            :end_game_condition, :teaching_tips, :strategy_tips
        )
        ON CONFLICT(id) DO UPDATE SET
            title              = excluded.title,
            weight             = excluded.weight,
            bgg_weight         = excluded.bgg_weight,
            min_players        = excluded.min_players,
            max_players        = excluded.max_players,
            play_time          = excluded.play_time,
            image_url          = excluded.image_url,
            image_path         = excluded.image_path,
            mechanics          = excluded.mechanics,
            description        = excluded.description,
            theme              = excluded.theme,
            objective          = excluded.objective,
            setup              = excluded.setup,
            round_structure    = excluded.round_structure,
            main_actions       = excluded.main_actions,
            end_game_condition = excluded.end_game_condition,
            teaching_tips      = excluded.teaching_tips,
            strategy_tips      = excluded.strategy_tips
    """, data)

    conn.execute("DELETE FROM quiz_questions WHERE game_id = ?", (data["id"],))
    for i, q in enumerate(quiz):
        conn.execute(
            """INSERT INTO quiz_questions
               (game_id, question_order, question, options, answer_index)
               VALUES (?, ?, ?, ?, ?)""",
            (data["id"], i, q["question"],
             json.dumps(q["options"], ensure_ascii=False), q["answer_index"]),
        )

    conn.commit()
    conn.close()


def delete_game(game_id: str) -> None:
    conn = _connect()
    conn.execute("DELETE FROM games WHERE id = ?", (game_id,))
    conn.commit()
    conn.close()
