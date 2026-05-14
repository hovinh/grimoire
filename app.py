from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Grimoire",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

is_local = Path(__file__).parent.joinpath(".local").exists()


codex = st.Page("pages/codex.py", title="The Codex", icon="📖", default=True)
tome = st.Page("pages/tome.py", title="The Tome", icon="📜")
scribe = st.Page("pages/scribe.py", title="The Scribe", icon="✍️")

all_pages = [codex, tome, scribe] if is_local else [codex, tome]
pg = st.navigation(all_pages, position="hidden")

with st.sidebar:
    st.markdown(
        "<div style='padding:8px 0 12px'>"
        "<p style='font-size:1.5rem; font-weight:700; margin:0;'>📖 Grimoire</p>"
        "<p style='font-size:0.8rem; color:#888; font-style:italic; margin:2px 0 0;'>"
        "A Game Master's Compendium</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.page_link(codex, label="The Codex", icon="📖")
    if is_local:
        st.page_link(scribe, label="The Scribe", icon="✍️")
    # ── add future sections here ──────────────────────────────────────────────

pg.run()
