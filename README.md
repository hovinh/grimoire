# Grimoire

A Game Master's knowledge management tool for board game rules. Built with Streamlit.

## Pages

| Page | File | Visible |
|---|---|---|
| **The Codex** | `pages/codex.py` | Always |
| **The Tome** | `pages/tome.py` | Always (accessed via card) |
| **The Scribe** | `pages/scribe.py` | Local only |

- **The Codex** — catalog of board games with search and weight filter
- **The Tome** — full game reference: rules, quiz, teaching tips, strategy tips
- **The Scribe** — form to add or edit games (local only, hidden on deployed app)

---

## Setup

**Requirements:** Python 3.11

```bash
git clone <repo-url>
cd grimoire

py -3.11 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Create the `.local` marker file to enable write features:

```bash
# Windows
type nul > .local

# macOS / Linux
touch .local
```

Run the app:

```bash
.venv\Scripts\streamlit run app.py
```

---

## Project Structure

```
grimoire/
├── app.py                  # Entry point — navigation config, sidebar
├── pages/
│   ├── codex.py            # The Codex (game catalog)
│   ├── tome.py             # The Tome (game detail)
│   └── scribe.py           # The Scribe (add/edit form, local only)
├── utils/
│   └── db.py               # SQLite helpers (init, get, upsert, delete)
├── data/
│   ├── grimoire.db         # SQLite database — commit this with your code
│   └── images/             # Cover images at 600×450 (4:3 JPEG)
├── scripts/
│   ├── fetch_images.py               # Downloads and crops cover images from Wikipedia
│   ├── generate_placeholder_images.py # Generates styled placeholder cover images with PIL
│   ├── seed_lunar_creamery.py        # Example seed script — Lunar Creamery
│   ├── seed_moody_bear_kingdom.py    # Example seed script — Moody Bear Kingdom
│   └── seed_moon_leap.py             # Example seed script — Moon Leap
├── .streamlit/
│   └── config.toml         # Dark theme (gold + navy)
├── .local                  # Enables local-only features (gitignored)
└── requirements.txt
```

---

## Local vs Cloud

The Scribe (write features) is only available locally, controlled by a `.local` marker file in the project root.

```python
# How it works in app.py
is_local = Path(__file__).parent.joinpath(".local").exists()
```

- **Locally** — create `.local` after each fresh clone (it is gitignored and never committed)
- **Streamlit Community Cloud** — `.local` is never present, so The Scribe is completely absent: not visible in the sidebar and not reachable by URL

---

## Data Management

### Database

All game data lives in `data/grimoire.db` (SQLite). This file is committed to git and deployed with the app.

The `utils/db.py` module exposes:

```python
init_db()           # creates tables + migrates missing columns (called on every page load)
get_all_games()     # returns list of game dicts ordered by weight then title
get_game(id)        # returns one game dict with quiz, or None
upsert_game(dict)   # insert or update game + quiz questions
delete_game(id)     # deletes game and its quiz questions (cascade)
```

### Game Schema

**`games` table** — one row per game. List fields are stored as JSON strings.

| Field | Type | Notes |
|---|---|---|
| `id` | TEXT PK | Snake_case slug, e.g. `lunar_creamery` |
| `title` | TEXT | Display name |
| `weight` | TEXT | `light`, `medium`, or `heavy` |
| `bgg_weight` | REAL | BoardGameGeek complexity (1.0–5.0) |
| `min_players` | INTEGER | |
| `max_players` | INTEGER | |
| `play_time` | TEXT | e.g. `"~46 min"` or `"20–35 min"` |
| `image_url` | TEXT | Fallback URL if no local image |
| `image_path` | TEXT | Local path, e.g. `data/images/lunar_creamery.jpg` |
| `mechanics` | LIST | e.g. `["hand management", "set collection"]` |
| `description` | TEXT | 2–3 sentence catalog blurb |
| `theme` | TEXT | Narrative hook — must capture the winning condition |
| `objective` | TEXT | Win condition in 1–2 sentences |
| `setup` | LIST | Ordered setup steps |
| `round_structure` | LIST | Each phase of a round |
| `main_actions` | LIST | Player actions, use `**Bold**` for action names |
| `card_effects` | LIST | *(optional)* Individual card reference list |
| `combo_cards` | LIST | *(optional)* Card combination effects |
| `end_game_condition` | TEXT | When/how the game ends |
| `scoring` | LIST | *(optional)* End-game scoring breakdown |
| `teaching_tips` | LIST | Tips for teaching at the table |
| `strategy_tips` | LIST | Tips for playing well |
| `advanced_rule` | JSON | *(optional)* See structure below |

**`quiz_questions` table** — five rows per game, foreign-keyed to `games.id`.

**`advanced_rule` object structure:**

```json
{
  "name": "Rule Name",
  "summary": "One-sentence description of what the rule adds.",
  "locking": "...",    // optional — use for lock/block mechanics
  "unlocking": "...",  // optional — use for resolution mechanics
  "details": "..."     // optional — use for general rule details
}
```

### Adding / Editing Games

**Via The Scribe (recommended for most edits):**
- **Add**: click **＋ New Game** on The Codex, or **✍️ The Scribe** in the sidebar
- **Edit**: open any game's Tome, click **✏️ Edit** in the top-right

**Via seed script (recommended for large content updates):**

Copy an existing script in `scripts/` as a template, fill in the game data, and run it:

```bash
.venv\Scripts\python scripts/seed_your_game.py
```

After saving, commit `data/grimoire.db` and push. Streamlit Cloud will redeploy with the updated data.

```bash
git add data/grimoire.db
git commit -m "add game: <title>"
git push
```

### Cover Images

Images live in `data/images/{game-id}.jpg`, cropped to **600×450 (4:3)**.

**Option 1 — Fetch from Wikipedia:**

```bash
# 1. Add the game's Wikipedia article title to WIKI_TITLES in scripts/fetch_images.py
# 2. Run the script
.venv\Scripts\python scripts/fetch_images.py
```

The script downloads, center-crops, and saves the JPEG. Update `image_path` in the database via The Scribe's image upload field or directly in the seed script.

**Option 2 — Generate a styled placeholder:**

```bash
# 1. Add an entry to the GAMES list in scripts/generate_placeholder_images.py
# 2. Run the script
.venv\Scripts\python scripts/generate_placeholder_images.py
```

Generates a 600×450 JPEG with the game title and a thematic motif using the app's gold/navy color scheme.

**Option 3 — Manual upload:** Place a JPEG in `data/images/` named `{game-id}.jpg` and set `image_path` via The Scribe.

---

## Theme

Configured in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#c9a227"          # gold
backgroundColor = "#0f0f1a"       # dark navy
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e8e8e8"
font = "serif"
```

---

## Deployment (Streamlit Community Cloud)

1. Push your code (including `data/grimoire.db`) to GitHub
2. Connect the repo on [share.streamlit.io](https://share.streamlit.io)
3. Set **Main file path** to `app.py`
4. No secrets or environment variables needed

The app will run in read-only mode (The Scribe is hidden). To update game content after deploying, add/edit locally via The Scribe, then commit and push `data/grimoire.db`.

---

## Adding a New Navigation Section (Future)

1. Create `pages/your_page.py`
2. Register it in `app.py`:

```python
your_page = st.Page("pages/your_page.py", title="Your Title", icon="🗺️")
all_pages = [codex, tome, scribe, your_page] if is_local else [codex, tome, your_page]
```

3. Add the sidebar link:

```python
st.page_link(your_page, label="Your Title", icon="🗺️")
```

---

## Adding or Updating Game Content with AI

Use the prompt below to have an AI assistant (e.g. Claude) draft or rewrite game content from a rulebook. Always review the draft before writing it to the database.

### Content guidelines

- **Language**: Suitable for ages 10 and up. Avoid jargon adults use casually but kids wouldn't (e.g. "factions", "paranoia", "face value", "forgoing").
- **Theme**: Written as a short narrative story. Must naturally include the winning condition — the reader should know how to win just from reading the theme.
- **Action names**: Use `**Bold**` markdown for action names in `main_actions`, `card_effects`, and `combo_cards`.
- **Game ID**: Use snake_case (e.g. `lunar_creamery`), not hyphens.
- **Optional fields**: Leave `card_effects`, `combo_cards`, `scoring`, and `advanced_rule` out entirely if the game doesn't need them.

### Prompt template

```
I need you to draft game content for Grimoire, a board game reference app.
Read the attached rulebook and fill out the fields below.

Present the full draft for my review — do NOT write anything to the database yet.

Content guidelines:
- Language must be understandable for a 10-year-old. Only simplify where genuinely necessary.
- The `theme` field must be a short narrative story (3–5 sentences) that naturally captures the winning condition. The reader should know how to win just from reading it.
- Use **Bold** markdown for action names in list fields.
- Game ID must be snake_case.
- Only include `card_effects`, `combo_cards`, `scoring`, and `advanced_rule` if the game actually has those.

Required fields:
- id (snake_case)
- title
- weight ("light", "medium", or "heavy")
- bgg_weight (1.0–5.0)
- min_players / max_players
- play_time
- mechanics (list)
- description (2–3 sentence catalog blurb)
- theme (narrative, includes winning condition)
- objective (1–2 sentences)
- setup (ordered list)
- round_structure (list of phases)
- main_actions (list, bold action names)
- end_game_condition
- teaching_tips (list, 4 tips)
- strategy_tips (list, 4 tips)
- quiz (5 multiple-choice questions, 4 options each, include answer_index 0–3)

Optional fields (include only if relevant):
- card_effects (list, bold card names)
- combo_cards (list, bold card combinations)
- scoring (list of scoring rules)
- advanced_rule { name, summary, locking?, unlocking?, details? }

[Attach rulebook here]
```

### After the AI drafts the content

1. Review all fields — check for accuracy against the rulebook and language clarity.
2. Use The Scribe to enter the content, **or** write a seed script based on the existing ones in `scripts/` and run it:

```bash
.venv\Scripts\python scripts/seed_your_game.py
```

3. If the game has a duplicate entry with a hyphen-based ID (old convention), delete it:

```python
import utils.db as db
db.init_db()
db.delete_game("old-hyphen-id")
```

4. Commit and push:

```bash
git add data/grimoire.db
git commit -m "update game: <title>"
git push
```
