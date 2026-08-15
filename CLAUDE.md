# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Grimoire is a Streamlit app that acts as a Game Master's reference tool for board game rules: catalog, full rulebook-style reference per game, and a quiz. Data lives in a committed SQLite database, not an external service.

## Setup & running

Requires Python 3.11.

```bash
py -3.11 -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# enable write features (The Scribe) locally — gitignored marker file
type nul > .local   # Windows; use `touch .local` on macOS/Linux

.venv\Scripts\streamlit run app.py
```

There is no linter or build step in this repo. See "Testing" below for the unit test suite.

## Testing

Unit tests live in `tests/` and run with pytest, configured via `pytest.ini` (adds the repo root to `sys.path` so `from utils import db` works). Install dev deps once with `.venv\Scripts\pip install -r requirements-dev.txt`, then run the whole suite with `.venv\Scripts\python -m pytest -q`.

- Any new code change (new logic, a bug fix, an edit to existing behavior) must come with unit tests covering it, and the full suite must be run as the last step before considering the change done — fix failures rather than reporting the task complete with red tests.
- `utils/db.py` is the primary unit-testable surface: pure CRUD/JSON-encoding logic against SQLite. `tests/conftest.py` provides a `test_db` fixture that points `db.DB_PATH` at an isolated per-test temp file via `monkeypatch` — never point tests at `data/grimoire.db`, since that's the committed, deployed data source. It also provides a `make_game` fixture that builds a full valid game dict (every field `upsert_game`'s named-params query requires) with overridable fields via `make_game(**overrides)`.
- `pages/*.py` are Streamlit UI and are not covered by this suite (doing so would need `streamlit.testing.v1.AppTest`, a heavier setup) — for those, still verify changes by running the app and clicking through the affected page, per "Setup & running" above.

## Local-only write mode

`app.py` checks for a `.local` marker file (`is_local = Path(__file__).parent.joinpath(".local").exists()`) to decide whether **The Scribe** (add/edit page) is registered in navigation and shown in the sidebar. Every page module re-derives `is_local` itself the same way — there's no shared session flag. On Streamlit Community Cloud `.local` is never present, so writes are impossible and the page is unreachable even by direct URL. When adding UI that mutates data, gate it behind this same check, following the pattern already in `pages/codex.py` and `pages/tome.py`.

## Architecture

- **`app.py`** — entry point; declares the `st.Page` set and sidebar nav. `st.navigation(..., position="hidden")` is used with a hand-rolled sidebar (`st.page_link`) instead of Streamlit's default nav UI, so adding a page means updating `all_pages` *and* adding a `st.page_link` in the sidebar block.
- **`pages/codex.py`** — game catalog: search + weight filter over `db.get_all_games()`, card grid, navigates to `pages/tome.py` via `st.session_state["selected_game"]` + `st.switch_page`.
- **`pages/tome.py`** — full reference view for one game (rules, quiz, teaching/strategy tips). Reads the selected game id from `st.session_state["selected_game"]`; redirects back to the Codex if unset.
- **`pages/scribe.py`** — add/edit form. Reads/writes `st.session_state["sc_*"]` keys for form fields and `st.session_state["scribe_game_id"]` to know whether it's creating or editing. Only reachable when `.local` exists.
- **`utils/db.py`** — the only place that talks to SQLite (`data/grimoire.db`). Every page calls `db.init_db()` on load, which both creates tables if missing and runs additive `ALTER TABLE` migrations (`_maybe_add_column`) for columns added after the initial schema — this is the migration mechanism; there are no separate migration files. List-typed fields (`mechanics`, `setup`, `round_structure`, `main_actions`, `card_effects`, `combo_cards`, `scoring`, `teaching_tips`, `strategy_tips`) are stored as JSON text columns and transparently encoded/decoded in `_row_to_game` / `upsert_game`. `advanced_rule` is a JSON object column, also transparently encoded/decoded. `quiz_questions` is a separate table, foreign-keyed to `games.id` with cascade delete, and is fully replaced (delete-then-reinsert) on every `upsert_game` call rather than diffed.
- **`scripts/`** — one-off/repeatable data tooling, not part of the app runtime:
  - `seed_*.py` — each is a standalone script that builds a game dict (matching the schema below) and calls `db.upsert_game(...)`. Copy one as a template for adding a new game via script instead of the UI.
  - `fetch_images.py` — downloads a Wikipedia article's lead image, center-crops to 600×450, saves to `data/images/{id}.jpg`.
  - `generate_placeholder_images.py` — generates a styled 600×450 placeholder cover (PIL) using the app's gold/navy theme when no real image is available.

## Game data schema

Data model, full field list, and the `advanced_rule` JSON shape are documented in [README.md](README.md) under "Data Management" — read it before adding or editing game content or writing a seed script. Key points not to relearn by trial and error:

- Game `id` is a snake_case slug (e.g. `lunar_creamery`); an older hyphenated-id convention exists in some historical data and should be migrated away from when encountered, not replicated.
- `card_effects`, `combo_cards`, `scoring`, and `advanced_rule` are optional — omit entirely rather than writing empty placeholders.
- After changing game content (via The Scribe or a seed script), `data/grimoire.db` must be committed and pushed — it's the deployed data source; Streamlit Cloud has no separate database.
- Cover images are committed JPEGs at `data/images/{id}.jpg`, cropped to 600×450 (4:3).

## Content style rules (when drafting or editing game content)

- Written for ages 10+: avoid adult-jargon words the README calls out (e.g. "factions", "paranoia", "face value", "forgoing").
- `theme` is a short narrative (3–5 sentences) that must make the win condition clear from reading it alone — not a dry rules summary.
- Use `**Bold**` markdown for action/card names inside `main_actions`, `card_effects`, and `combo_cards`.
- Quiz is always 5 multiple-choice questions, 4 options each, with a 0-indexed `answer_index`.

## Theme

Dark gold/navy theme is set in `.streamlit/config.toml`. UI code in `pages/*.py` hardcodes matching hex values inline (e.g. the `TAG_CSS` gold `#c9a227` for mechanic tags) rather than reading from the theme config — keep new inline styling consistent with these values rather than introducing new colors.
