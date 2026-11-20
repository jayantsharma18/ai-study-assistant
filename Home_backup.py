
"""
Home.py — Navigation router for AI Study Assistant
----------------------------------------------------
WHAT CHANGED AND WHY (beginner explanation):

OLD approach: Streamlit auto-discovered files in pages/ folder.
  Problem: emoji filenames caused navigation to break on macOS.
  Problem: st.set_page_config() called in every page → silent errors.

NEW approach: st.navigation() — the official Streamlit API since v1.36.
  - We explicitly register every page here with st.Page().
  - st.set_page_config() is called ONCE here — never in page files.
  - init_session() is called ONCE here — never in page files.
  - Navigation in the sidebar is fully controlled and always works.

Run with:  streamlit run Home.py
"""

import streamlit as st
from utils.session import init_session

# ── 1. Page config — called ONCE here, never in page files ───────────────────
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 2. Shared session state — initialised once for the whole app ──────────────
init_session()

# ── 3. Sidebar branding — appears above the navigation links on every page ────
with st.sidebar:
    st.markdown("## 🎓 AI Study Assistant")
    st.markdown("Powered by **GPT-4.1-mini** via Azure AI Foundry")
    st.divider()
    st.caption("Built with Streamlit + Azure OpenAI")

# ── 4. Register all pages using st.navigation() ───────────────────────────────
#
# st.Page(path, title, icon, default) tells Streamlit:
#   - path   : which file to run when this page is selected
#   - title  : label shown in the sidebar
#   - icon   : emoji shown next to the label
#   - default: which page loads when the app first opens
#
# Pages are grouped under section headings using a dict.
#
pg = st.navigation(
    {
        "🏠 Home": [
            st.Page(
                "pages/home_page.py",
                title="Home",
                icon="🏠",
                default=True,
            ),
        ],
        "📚 Study Tools": [
            st.Page("pages/ask_question.py",    title="Ask a Question",  icon="💬"),
            st.Page("pages/summarise_notes.py", title="Summarise Notes", icon="📝"),
            st.Page("pages/quiz_generator.py",  title="Quiz Generator",  icon="🧠"),
            st.Page("pages/exam_prep.py",       title="Exam Prep",       icon="📅"),
        ],
    }
)

# ── 5. Run the selected page ──────────────────────────────────────────────────
# This line executes the code inside whichever page the user clicked.
pg.run()
