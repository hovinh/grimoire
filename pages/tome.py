import json
import sys
import time
from pathlib import Path

import streamlit as st
from PIL import Image

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import utils.db as db

db.init_db()

WEIGHT_EMOJI = {"light": "🟢", "medium": "🟡", "heavy": "🔴"}
WEIGHT_LABEL = {"light": "Light", "medium": "Medium", "heavy": "Heavy"}

TAG_CSS = (
    "display:inline-block; margin:2px 3px 2px 0;"
    "background:rgba(201,162,39,0.12); color:#c9a227;"
    "border:1px solid rgba(201,162,39,0.3); border-radius:4px;"
    "padding:2px 8px; font-size:12px; font-family:sans-serif;"
)

is_local = (ROOT / ".local").exists()


def game_image(game: dict):
    img_path = game.get("image_path")
    if img_path:
        full = ROOT / img_path
        if full.exists():
            return Image.open(full)
    return game.get("image_url", "")


# ── Guard ─────────────────────────────────────────────────────────────────────
if "selected_game" not in st.session_state:
    st.switch_page("pages/codex.py")

game = db.get_game(st.session_state.get("selected_game", ""))

if not game:
    st.error("Tome not found.")
    if st.button("← Return to The Codex"):
        st.switch_page("pages/codex.py")
    st.stop()

game_id: str = game["id"]

# Browsers use document.title as the default filename when printing/saving
# as PDF; Streamlit resets it back to the app's page_title ("Grimoire") on
# every rerun, so this has to reapply the game's title every render too. The
# nonce forces the srcdoc to differ each time, otherwise Streamlit reuses the
# same iframe and the script never re-fires.
st.components.v1.html(
    f"<script>/* {time.time()} */ "
    f"window.parent.document.title = {json.dumps(game['title'])};</script>",
    height=0,
)

# ── Print styling ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @media print {
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        #MainMenu,
        footer,
        .stButton,
        .no-print {
            display: none !important;
        }
        /* The app theme is light-on-dark; force a light-on-white
           page so printed/PDF output stays legible regardless of
           the browser's "print background graphics" setting. */
        html, body, .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background: #ffffff !important;
        }
        [data-testid="stMain"] * {
            color: #000000 !important;
            background-color: transparent !important;
            border-color: #999999 !important;
            box-shadow: none !important;
        }
        /* Compact layout: Streamlit's typography is rem-based (e.g.
           paragraphs render at 1.5rem), so shrinking the root
           font-size scales text, line-height, and rem-based spacing
           together, in proportion, without fighting Streamlit's own
           line-height math the way separate per-element font-size
           and margin overrides did (that caused wrapped list lines
           to overlap the next bullet). `zoom` was tried before that,
           but it isn't a standard CSS property and the real
           print-to-PDF pipeline renders it inconsistently — text
           and background color would drop out entirely. */
        html {
            font-size: 11px !important;
        }
        [data-testid="stImage"] img {
            max-width: 60% !important;
            height: auto !important;
        }
        [data-testid="stVerticalBlock"] {
            gap: 0.3rem !important;
        }
        [data-testid="stHorizontalBlock"] {
            gap: 0.5rem !important;
        }
        [data-testid="stElementContainer"] {
            margin-bottom: 0 !important;
        }
        [data-testid="stRadio"] label {
            padding: 0 !important;
            min-height: 0 !important;
        }
        [data-testid="stRadio"] > div {
            gap: 0.15rem !important;
        }
        hr {
            margin: 6px 0 !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Navigation ────────────────────────────────────────────────────────────────
if is_local:
    nav_col, print_col, edit_col = st.columns([5, 1, 1])
else:
    nav_col, print_col = st.columns([6, 1])

with nav_col:
    if st.button("← Return to The Codex"):
        st.switch_page("pages/codex.py")
with print_col:
    if st.button("🖨️ Print", use_container_width=True):
        st.session_state["_do_print"] = True

if is_local:
    with edit_col:
        if st.button("✏️ Edit", use_container_width=True):
            st.session_state["scribe_game_id"] = game_id
            st.session_state.pop("scribe_ready", None)
            st.switch_page("pages/scribe.py")

st.markdown("---")

# ── Hero ──────────────────────────────────────────────────────────────────────
col_img, col_info = st.columns([1, 2], gap="large")
with col_img:
    st.image(game_image(game), width="stretch")
with col_info:
    w = game["weight"]
    st.title(game["title"])
    st.markdown(
        f"{WEIGHT_EMOJI[w]} **{WEIGHT_LABEL[w]} Weight** &nbsp;·&nbsp; "
        f"BGG {game['bgg_weight']:.1f} / 5 &nbsp;·&nbsp; "
        f"⏱ {game['play_time']} &nbsp;·&nbsp; "
        f"👥 {game['min_players']}–{game['max_players']} players",
        unsafe_allow_html=True,
    )
    tags_html = "".join(
        f'<span style="{TAG_CSS}">{m}</span>' for m in game["mechanics"]
    )
    st.markdown(tags_html, unsafe_allow_html=True)
    st.markdown("")
    st.markdown(f"*{game['description']}*")

st.divider()


# ── Rule Sections ─────────────────────────────────────────────────────────────
def _render_section(label: str, content: str | list) -> None:
    st.subheader(label)
    if isinstance(content, list):
        for item in content:
            st.markdown(f"- {item}")
    else:
        st.markdown(content)
    st.markdown("")


_render_section("🎭 Theme", game["theme"])
_render_section("🏆 Objective", game["objective"])
_render_section("⚙️ Setup", game["setup"])
_render_section("🔄 Round Structure", game["round_structure"])
_render_section("⚡ Main Actions", game["main_actions"])
if game.get("card_effects"):
    _render_section("🃏 Card Effects", game["card_effects"])
if game.get("combo_cards"):
    _render_section("🔀 Combo Cards", game["combo_cards"])
_render_section("🏁 End Game Condition", game["end_game_condition"])

if game.get("scoring"):
    _render_section("🍦 Scoring", game["scoring"])

adv = game.get("advanced_rule")
if adv:
    st.subheader("🔮 Advanced Rules")
    st.markdown(f"**{adv['name']}**")
    st.markdown(adv["summary"])
    if adv.get("locking"):
        st.markdown(f"**Locking:** {adv['locking']}")
    if adv.get("unlocking"):
        st.markdown(f"**Unlocking:** {adv['unlocking']}")
    if adv.get("details"):
        st.markdown(adv["details"])
    st.markdown("")

st.divider()

# ── Rules Quiz ────────────────────────────────────────────────────────────────
st.subheader("📋 Rules Quiz")
st.caption(
    "Answer all 5 questions, then press **Check Score** "
    "to see how ready you are to teach this game."
)
st.markdown("")

quiz = game["quiz"]
submitted_key = f"quiz_{game_id}_submitted"

if st.session_state.get("_quiz_game") != game_id:
    st.session_state[submitted_key] = False
    st.session_state["_quiz_game"] = game_id

for i, q in enumerate(quiz):
    st.markdown(f"**Q{i + 1}. {q['question']}**")
    st.radio(
        label=f"q{i}",
        options=q["options"],
        key=f"q_{game_id}_{i}",
        label_visibility="collapsed",
        index=None,
    )
    st.markdown("")

if st.button("Check Score", type="primary"):
    answers = [st.session_state.get(f"q_{game_id}_{i}") for i in range(len(quiz))]
    if any(a is None for a in answers):
        st.warning(f"Please answer all {len(quiz)} questions before checking your score.")
    else:
        st.session_state[submitted_key] = True

if st.session_state.get(submitted_key):
    answers = [st.session_state.get(f"q_{game_id}_{i}") for i in range(len(quiz))]
    score = sum(
        1 for i, q in enumerate(quiz)
        if answers[i] == q["options"][q["answer_index"]]
    )

    col_score, col_msg = st.columns([1, 3])
    with col_score:
        st.metric("Score", f"{score} / {len(quiz)}")
    with col_msg:
        if score == len(quiz):
            st.success("Perfect score! You're ready to run this game.")
        elif score >= 3:
            st.info("Good grasp of the rules. Review the highlighted answers below.")
        else:
            st.warning("A few gaps — re-read the sections above and try again.")

    st.markdown("##### Answer Key")
    for i, q in enumerate(quiz):
        correct = q["options"][q["answer_index"]]
        user = answers[i]
        if user == correct:
            st.markdown(f"✅ **Q{i + 1}**: {correct}")
        else:
            st.markdown(
                f"❌ **Q{i + 1}**: ~~{user}~~ &nbsp;→&nbsp; **{correct}**",
                unsafe_allow_html=True,
            )

st.divider()

# ── Tips ──────────────────────────────────────────────────────────────────────
col_teach, col_strat = st.columns(2, gap="large")
with col_teach:
    st.subheader("🎓 Teaching Tips")
    for tip in game["teaching_tips"]:
        st.markdown(f"- {tip}")
with col_strat:
    st.subheader("♟️ Strategy Tips")
    for tip in game["strategy_tips"]:
        st.markdown(f"- {tip}")

# ── Print trigger ─────────────────────────────────────────────────────────────
# Placed after all page content so the print dialog can't fire before
# Streamlit has finished rendering the rest of the page (it did, when this
# lived right after the nav buttons — the printed page's content below the
# fold came out unstyled/faded because it hadn't painted yet). The nonce
# forces the srcdoc to differ between reruns, and the setTimeout gives the
# browser one more frame to finish painting before the snapshot is taken.
if st.session_state.pop("_do_print", False):
    st.components.v1.html(
        f"<script>/* {time.time()} */ "
        "setTimeout(() => window.parent.print(), 250);</script>",
        height=0,
    )
