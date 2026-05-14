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
│   ├── games.json          # Seed data — used only for initial migration
│   └── images/             # Cover images at 600×450 (4:3 JPEG)
├── scripts/
│   ├── migrate_to_sqlite.py  # One-time: seeds grimoire.db from games.json
│   └── fetch_images.py       # Downloads and crops cover images from Wikipedia
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

**Schema:**
- `games` — one row per game, list fields stored as JSON strings
- `quiz_questions` — five rows per game, foreign-keyed to `games.id`

The `utils/db.py` module exposes:

```python
init_db()           # creates tables if not exist (called on every page load)
get_all_games()     # returns list of game dicts ordered by weight then title
get_game(id)        # returns one game dict with quiz, or None
upsert_game(dict)   # insert or update game + quiz questions
delete_game(id)     # deletes game and its quiz questions (cascade)
```

### Adding / Editing Games

Use **The Scribe** from the local app:
- **Add**: click **＋ New Game** on The Codex, or **✍️ The Scribe** in the sidebar
- **Edit**: open any game's Tome, click **✏️ Edit** in the top-right

After saving, commit `data/grimoire.db` and push. Streamlit Cloud will redeploy with the updated data.

```bash
git add data/grimoire.db
git commit -m "add game: <title>"
git push
```

### Cover Images

Images live in `data/images/{game-id}.jpg`, cropped to **600×450 (4:3)**.

To fetch images for new games via Wikipedia's open API:

```bash
# 1. Add the game's Wikipedia article title to WIKI_TITLES in scripts/fetch_images.py
# 2. Run the script
.venv\Scripts\python scripts/fetch_images.py
```

The script downloads, center-crops, saves the JPEG, and updates `image_path` in `games.json`. After running, commit both the image and the updated `grimoire.db` (re-save the game via The Scribe to pick up the new path, or update the db directly).

To manually add a cover image: place a JPEG in `data/images/` named `{game-id}.jpg` and update `image_path` in the database via The Scribe's image upload field.

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
