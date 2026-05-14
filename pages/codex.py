import sys
from pathlib import Path

import streamlit as st
from PIL import Image

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import utils.db as db

db.init_db()

is_local = (ROOT / ".local").exists()

WEIGHT_EMOJI = {"light": "🟢", "medium": "🟡", "heavy": "🔴"}
WEIGHT_LABEL = {"light": "Light", "medium": "Medium", "heavy": "Heavy"}

TAG_CSS = (
    "display:inline-block; margin:2px 3px 2px 0;"
    "background:rgba(201,162,39,0.12); color:#c9a227;"
    "border:1px solid rgba(201,162,39,0.3); border-radius:4px;"
    "padding:1px 7px; font-size:11px; font-family:sans-serif;"
)


def game_image(game: dict):
    img_path = game.get("image_path")
    if img_path:
        full = ROOT / img_path
        if full.exists():
            return Image.open(full)
    return game.get("image_url", "")


games = db.get_all_games()

# ── Header ────────────────────────────────────────────────────────────────────
header_col, btn_col = st.columns([5, 1])
with header_col:
    st.markdown(
        "<h1 style='margin-bottom:0'>The Codex</h1>"
        "<p style='color:#888; margin-top:4px; font-style:italic;'>"
        "Browse the collection. Open a Tome to learn its secrets.</p>",
        unsafe_allow_html=True,
    )
with btn_col:
    if is_local:
        st.markdown("<div style='padding-top:18px'>", unsafe_allow_html=True)
        if st.button("＋ New Game", use_container_width=True, type="primary"):
            st.session_state.pop("scribe_game_id", None)
            st.session_state.pop("scribe_ready", None)
            st.switch_page("pages/scribe.py")
        st.markdown("</div>", unsafe_allow_html=True)
st.divider()

# ── Filters ───────────────────────────────────────────────────────────────────
col_search, col_weight = st.columns([3, 2])
with col_search:
    search = st.text_input(
        "search",
        placeholder="🔍  Search by title, mechanic, or keyword…",
        label_visibility="collapsed",
    )
with col_weight:
    weight_filter = st.radio(
        "Weight",
        ["All", "Light", "Medium", "Heavy"],
        horizontal=True,
        label_visibility="collapsed",
    )


def _matches(game: dict) -> bool:
    q = search.strip().lower()
    weight_ok = weight_filter == "All" or game["weight"].capitalize() == weight_filter
    if not q:
        return weight_ok
    text_ok = (
        q in game["title"].lower()
        or q in game["description"].lower()
        or any(q in m.lower() for m in game["mechanics"])
    )
    return weight_ok and text_ok


filtered = [g for g in games if _matches(g)]

st.caption(
    f"Showing **{len(filtered)}** of **{len(games)}** tomes"
    + (f" · filtered by *{weight_filter}*" if weight_filter != "All" else "")
    + (f' · matching *"{search}"*' if search.strip() else "")
)

if not filtered:
    st.info("No tomes match your search. Try a different keyword or weight filter.")
    st.stop()

# ── Card Grid ─────────────────────────────────────────────────────────────────
cols = st.columns(3, gap="medium")
for i, game in enumerate(filtered):
    with cols[i % 3]:
        with st.container(border=True):
            st.image(game_image(game), width="stretch")

            w = game["weight"]
            st.markdown(f"### {game['title']}")
            st.markdown(
                f"{WEIGHT_EMOJI[w]} **{WEIGHT_LABEL[w]}** &nbsp;·&nbsp; "
                f"⏱ {game['play_time']} &nbsp;·&nbsp; "
                f"👥 {game['min_players']}–{game['max_players']} players",
                unsafe_allow_html=True,
            )

            tags_html = "".join(
                f'<span style="{TAG_CSS}">{m}</span>' for m in game["mechanics"]
            )
            st.markdown(tags_html, unsafe_allow_html=True)
            st.caption(game["description"])

            if st.button(
                "Open Tome ✦",
                key=f"open_{game['id']}",
                use_container_width=True,
                type="primary",
            ):
                st.session_state["selected_game"] = game["id"]
                st.switch_page("pages/tome.py")
