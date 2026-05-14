import io
import re
import sys
from pathlib import Path

import streamlit as st
from PIL import Image

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import utils.db as db

db.init_db()

IMAGES_DIR = ROOT / "data" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s.strip("-")


def crop_to_cover(data: bytes) -> Image.Image:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    w, h = img.size
    target_ratio = 600 / 450
    if (w / h) > target_ratio:
        new_w = int(h * target_ratio)
        img = img.crop(((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h))
    else:
        new_h = int(w / target_ratio)
        img = img.crop((0, (h - new_h) // 2, w, (h - new_h) // 2 + new_h))
    return img.resize((600, 450), Image.LANCZOS)


def empty_question() -> dict:
    return {"question": "", "options": ["", "", "", ""], "answer_index": 0}


# ── State initialisation ──────────────────────────────────────────────────────

def _init_defaults() -> None:
    st.session_state.update({
        "sc_id": "",
        "sc_title": "",
        "sc_weight": "medium",
        "sc_bgg_weight": 2.5,
        "sc_min_players": 2,
        "sc_max_players": 4,
        "sc_play_time": "",
        "sc_mechanics": [""],
        "sc_description": "",
        "sc_theme": "",
        "sc_objective": "",
        "sc_setup": [""],
        "sc_round_structure": [""],
        "sc_main_actions": [""],
        "sc_end_game_condition": "",
        "sc_quiz": [empty_question() for _ in range(5)],
        "sc_teaching_tips": [""],
        "sc_strategy_tips": [""],
        "sc_image_path": "",
        "sc_image_url": "",
        "sc_uploaded_img": None,
    })


def _init_from_game(game: dict) -> None:
    st.session_state.update({
        "sc_id": game["id"],
        "sc_title": game["title"],
        "sc_weight": game["weight"],
        "sc_bgg_weight": float(game.get("bgg_weight") or 2.5),
        "sc_min_players": int(game.get("min_players") or 2),
        "sc_max_players": int(game.get("max_players") or 4),
        "sc_play_time": game.get("play_time") or "",
        "sc_mechanics": game.get("mechanics") or [""],
        "sc_description": game.get("description") or "",
        "sc_theme": game.get("theme") or "",
        "sc_objective": game.get("objective") or "",
        "sc_setup": game.get("setup") or [""],
        "sc_round_structure": game.get("round_structure") or [""],
        "sc_main_actions": game.get("main_actions") or [""],
        "sc_end_game_condition": game.get("end_game_condition") or "",
        "sc_quiz": game.get("quiz") or [empty_question() for _ in range(5)],
        "sc_teaching_tips": game.get("teaching_tips") or [""],
        "sc_strategy_tips": game.get("strategy_tips") or [""],
        "sc_image_path": game.get("image_path") or "",
        "sc_image_url": game.get("image_url") or "",
        "sc_uploaded_img": None,
    })


# ── Mode detection ────────────────────────────────────────────────────────────

edit_id = st.session_state.get("scribe_game_id")
is_edit = edit_id is not None

if not st.session_state.get("scribe_ready"):
    if is_edit:
        game = db.get_game(edit_id)
        if not game:
            st.error(f"Game '{edit_id}' not found.")
            st.stop()
        _init_from_game(game)
    else:
        _init_defaults()
    st.session_state["scribe_ready"] = True


# ── Dynamic list helpers ──────────────────────────────────────────────────────

def _sync(key: str) -> None:
    """Read widget values back into the master list before structural changes."""
    n = len(st.session_state[key])
    st.session_state[key] = [
        st.session_state.get(f"{key}_{i}", "") for i in range(n)
    ]


def _list_editor(label: str, key: str, placeholder: str = "") -> None:
    items = st.session_state[key]
    remove_idx = None
    for i, val in enumerate(items):
        c1, c2 = st.columns([11, 1])
        with c1:
            st.text_input(
                f"{label} {i + 1}",
                value=val,
                key=f"{key}_{i}",
                placeholder=placeholder,
                label_visibility="collapsed",
            )
        with c2:
            if len(items) > 1 and st.button("✕", key=f"rm_{key}_{i}"):
                remove_idx = i

    if remove_idx is not None:
        _sync(key)
        st.session_state[key].pop(remove_idx)
        st.rerun()

    if st.button(f"＋ Add {label.lower()}", key=f"add_{key}"):
        _sync(key)
        st.session_state[key].append("")
        st.rerun()


def _read_list(key: str) -> list[str]:
    _sync(key)
    return [v for v in st.session_state[key] if v.strip()]


# ── Navigation bar ────────────────────────────────────────────────────────────

col_back, col_title = st.columns([1, 5])
with col_back:
    if st.button("← The Codex"):
        st.session_state.pop("scribe_ready", None)
        st.session_state.pop("scribe_game_id", None)
        st.switch_page("pages/codex.py")
with col_title:
    mode_label = f"Editing — *{st.session_state.sc_title or 'Untitled'}*" if is_edit else "New Tome"
    st.markdown(f"## ✍️ The Scribe &nbsp; · &nbsp; {mode_label}", unsafe_allow_html=True)

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_basic, tab_rules, tab_quiz, tab_tips = st.tabs(
    ["📋 Basics", "📖 Rules", "❓ Quiz", "💡 Tips"]
)

# ═══ TAB 1 — BASICS ══════════════════════════════════════════════════════════
with tab_basic:
    st.session_state.sc_title = st.text_input(
        "Title *", value=st.session_state.sc_title, placeholder="e.g. Wingspan"
    )

    c1, c2 = st.columns(2)
    with c1:
        st.session_state.sc_weight = st.radio(
            "Weight *",
            ["light", "medium", "heavy"],
            index=["light", "medium", "heavy"].index(st.session_state.sc_weight),
            horizontal=True,
            format_func=str.capitalize,
        )
    with c2:
        st.session_state.sc_bgg_weight = st.number_input(
            "BGG Complexity (1–5)",
            min_value=1.0, max_value=5.0, step=0.1,
            value=st.session_state.sc_bgg_weight,
        )

    c3, c4, c5 = st.columns(3)
    with c3:
        st.session_state.sc_min_players = st.number_input(
            "Min players", min_value=1, max_value=20,
            value=st.session_state.sc_min_players,
        )
    with c4:
        st.session_state.sc_max_players = st.number_input(
            "Max players", min_value=1, max_value=20,
            value=st.session_state.sc_max_players,
        )
    with c5:
        st.session_state.sc_play_time = st.text_input(
            "Play time", value=st.session_state.sc_play_time,
            placeholder="e.g. 40–70 min",
        )

    st.markdown("**Mechanics** *(comma-separated)*")
    mechanics_str = st.text_input(
        "mechanics",
        value=", ".join(v for v in st.session_state.sc_mechanics if v.strip()),
        placeholder="e.g. engine building, card drafting",
        label_visibility="collapsed",
    )

    st.markdown("**Cover Image**")
    uploaded = st.file_uploader(
        "cover", type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )
    if uploaded:
        st.session_state.sc_uploaded_img = uploaded.read()

    if st.session_state.sc_uploaded_img:
        preview = crop_to_cover(st.session_state.sc_uploaded_img)
        st.image(preview, caption="Preview (auto-cropped to 600×450)", width=300)
    elif st.session_state.sc_image_path:
        full = ROOT / st.session_state.sc_image_path
        if full.exists():
            st.image(Image.open(full), caption="Current cover", width=300)

    st.session_state.sc_description = st.text_area(
        "Brief description * *(shown on the catalog card)*",
        value=st.session_state.sc_description,
        placeholder="2–3 sentences that hook a player's interest.",
        max_chars=300,
        height=100,
    )

# ═══ TAB 2 — RULES ═══════════════════════════════════════════════════════════
with tab_rules:
    st.session_state.sc_theme = st.text_area(
        "🎭 Theme", value=st.session_state.sc_theme, height=100,
        placeholder="The narrative hook — what world does the player inhabit?",
    )
    st.session_state.sc_objective = st.text_area(
        "🏆 Objective", value=st.session_state.sc_objective, height=80,
        placeholder="Win condition in one or two sentences.",
    )

    st.markdown("**⚙️ Setup**")
    _list_editor("Step", "sc_setup", "Describe this setup step…")

    st.markdown("**🔄 Round Structure**")
    _list_editor("Phase", "sc_round_structure", "Describe this phase…")

    st.markdown("**⚡ Main Actions**")
    _list_editor("Action", "sc_main_actions", "**Action name**: description…")

    st.session_state.sc_end_game_condition = st.text_area(
        "🏁 End Game Condition",
        value=st.session_state.sc_end_game_condition,
        height=100,
        placeholder="When does the game end, and how is the winner determined?",
    )

# ═══ TAB 3 — QUIZ ════════════════════════════════════════════════════════════
with tab_quiz:
    st.caption("5 multiple-choice questions · 4 options each · pick the correct answer")
    quiz = st.session_state.sc_quiz
    while len(quiz) < 5:
        quiz.append(empty_question())

    for qi in range(5):
        with st.expander(f"Question {qi + 1}", expanded=(qi == 0)):
            quiz[qi]["question"] = st.text_input(
                "Question", value=quiz[qi]["question"],
                key=f"sc_q{qi}_text",
                placeholder="What happens when…?",
            )
            st.markdown("Options & correct answer")
            correct_idx = quiz[qi]["answer_index"]
            for oi in range(4):
                oc1, oc2 = st.columns([10, 1])
                with oc1:
                    quiz[qi]["options"][oi] = st.text_input(
                        f"Option {chr(65 + oi)}",
                        value=quiz[qi]["options"][oi],
                        key=f"sc_q{qi}_o{oi}",
                        label_visibility="collapsed",
                        placeholder=f"Option {chr(65 + oi)}",
                    )
                with oc2:
                    st.markdown("<div style='padding-top:6px'>", unsafe_allow_html=True)
                    if st.checkbox(
                        "✓", value=(correct_idx == oi),
                        key=f"sc_q{qi}_correct{oi}",
                        help="Mark as correct answer",
                    ):
                        quiz[qi]["answer_index"] = oi
                    st.markdown("</div>", unsafe_allow_html=True)

# ═══ TAB 4 — TIPS ════════════════════════════════════════════════════════════
with tab_tips:
    st.markdown("**🎓 Teaching Tips**")
    _list_editor("Tip", "sc_teaching_tips", "A tip for teaching this game at the table…")

    st.markdown("**♟️ Strategy Tips**")
    _list_editor("Tip", "sc_strategy_tips", "A tip for winning or playing well…")

# ── Save / Cancel ─────────────────────────────────────────────────────────────
st.divider()
save_col, cancel_col = st.columns([1, 5])

with save_col:
    save = st.button("💾 Save to Codex", type="primary", use_container_width=True)
with cancel_col:
    if st.button("Cancel", use_container_width=True):
        st.session_state.pop("scribe_ready", None)
        st.session_state.pop("scribe_game_id", None)
        st.switch_page("pages/codex.py")

if save:
    errors = []
    title = st.session_state.sc_title.strip()
    if not title:
        errors.append("Title is required.")
    if not st.session_state.sc_description.strip():
        errors.append("Description is required.")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    game_id = st.session_state.sc_id or slugify(title)

    # Save cover image if uploaded
    image_path = st.session_state.sc_image_path
    if st.session_state.sc_uploaded_img:
        img = crop_to_cover(st.session_state.sc_uploaded_img)
        out = IMAGES_DIR / f"{game_id}.jpg"
        img.save(out, "JPEG", quality=90)
        image_path = f"data/images/{game_id}.jpg"

    mechanics = [m.strip() for m in mechanics_str.split(",") if m.strip()]

    game_record = {
        "id": game_id,
        "title": title,
        "weight": st.session_state.sc_weight,
        "bgg_weight": st.session_state.sc_bgg_weight,
        "min_players": st.session_state.sc_min_players,
        "max_players": st.session_state.sc_max_players,
        "play_time": st.session_state.sc_play_time.strip(),
        "image_url": st.session_state.sc_image_url,
        "image_path": image_path,
        "mechanics": mechanics,
        "description": st.session_state.sc_description.strip(),
        "theme": st.session_state.sc_theme.strip(),
        "objective": st.session_state.sc_objective.strip(),
        "setup": _read_list("sc_setup"),
        "round_structure": _read_list("sc_round_structure"),
        "main_actions": _read_list("sc_main_actions"),
        "end_game_condition": st.session_state.sc_end_game_condition.strip(),
        "teaching_tips": _read_list("sc_teaching_tips"),
        "strategy_tips": _read_list("sc_strategy_tips"),
        "quiz": st.session_state.sc_quiz,
    }

    db.upsert_game(game_record)

    st.session_state.pop("scribe_ready", None)
    st.session_state.pop("scribe_game_id", None)
    st.session_state["selected_game"] = game_id
    st.success(f"'{title}' saved!")
    st.switch_page("pages/tome.py")
