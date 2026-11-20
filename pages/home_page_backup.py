"""
pages/home_page.py — Landing page content
------------------------------------------
Renders the home screen: hero banner, four clickable feature cards,
and a getting-started guide.

KEY CHANGE: Cards now use st.page_link() so clicking them navigates
to the correct page. Previously they were plain HTML divs with no link.

st.page_link(path, label, icon, use_container_width)
  - path : must match the path given in st.Page() inside Home.py
  - Renders as a styled navigation button
"""

import streamlit as st

# ── Hero banner ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <h1 style='font-size: 3rem;'>🎓 AI Study Assistant</h1>
        <p style='font-size: 1.2rem; color: #aaa;'>
            Your intelligent, AI-powered tutor — available 24 / 7
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ── Feature cards — each card has a visual panel + a clickable link ───────────
#
# Why two elements per card?
#   st.markdown() with HTML draws the visual styling (colours, rounded corners).
#   st.page_link() below it creates the actual clickable navigation button.
#   Pure HTML <a> tags don't work for Streamlit page navigation — only
#   st.page_link() understands Streamlit's internal routing.

col1, col2, col3, col4 = st.columns(4, gap="medium")

cards = [
    (
        "💬", "Ask a Question",
        "Get clear answers to any academic question, explained simply.",
        "pages/ask_question.py",
    ),
    (
        "📝", "Summarise Notes",
        "Paste lecture notes and get a concise, structured summary.",
        "pages/summarise_notes.py",
    ),
    (
        "🧠", "Quiz Generator",
        "Auto-generate MCQs on any topic and test yourself instantly.",
        "pages/quiz_generator.py",
    ),
    (
        "📅", "Exam Prep",
        "Study plans, topic priorities, and essay answer feedback.",
        "pages/exam_prep.py",
    ),
]

for col, (icon, title, desc, path) in zip([col1, col2, col3, col4], cards):
    with col:
        # Visual card panel (decorative HTML)
        st.markdown(
            f"""
            <div style='
                background: #1A1A2E;
                border: 1px solid #6C63FF44;
                border-radius: 12px 12px 0 0;
                padding: 1.4rem 1.4rem 1rem 1.4rem;
                text-align: center;
                height: 160px;
            '>
                <div style='font-size: 2.5rem;'>{icon}</div>
                <h4 style='margin: 0.4rem 0 0.3rem;'>{title}</h4>
                <p style='font-size: 0.82rem; color: #aaa; margin: 0;'>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Clickable navigation button — connects to the card above it
        st.page_link(path, label=f"Open {title}", icon=icon, use_container_width=True)

st.divider()

# ── Getting started guide ─────────────────────────────────────────────────────
st.subheader("🚀 Getting Started")
st.markdown(
    """
    1. **Pick a feature** from the sidebar on the left, or click **Open** on any card above.
    2. **Type your question**, paste your notes, or choose a quiz topic.
    3. **Hit the button** and let the AI do the heavy lifting!

    > **Tip:** The app remembers your quiz scores and chat history for the whole session.  
    > Refresh the page to start completely fresh.
    """
)
