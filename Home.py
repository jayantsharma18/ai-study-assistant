
import streamlit as st
from utils.session import init_session

# 1. Page configuration
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Initialize shared session
init_session()

# 3. Custom application styling
st.markdown("""
<style>
/* Main application */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #17172b 0%, #11111f 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #d1d5db;
}

/* Sidebar navigation */
[data-testid="stSidebarNav"] {
    padding-top: 15px;
}

[data-testid="stSidebarNav"] a {
    border-radius: 9px;
    margin: 3px 8px;
    transition: background 0.2s ease;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: rgba(99,102,241,0.18);
}

/* Sidebar branding */
.brand-card {
    background: linear-gradient(135deg, #312e81, #4f46e5);
    padding: 20px 16px;
    border-radius: 14px;
    margin-top: 18px;
    margin-bottom: 18px;
}

.brand-card h2 {
    color: white;
    font-size: 21px;
    margin: 0;
}

.brand-card p {
    color: #e0e7ff;
    font-size: 12px;
    margin-top: 8px;
}

.sidebar-footer {
    color: #9ca3af;
    font-size: 12px;
    text-align: center;
    padding: 15px 5px;
    border-top: 1px solid rgba(255,255,255,0.12);
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# 4. Sidebar branding
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <h2>🎓 AI Study Assistant</h2>
        <p>Your intelligent learning companion</p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("POWERED BY")
    st.markdown("**Azure OpenAI · GPT-4.1-mini**")

    st.divider()

    st.markdown("""
    <div class="sidebar-footer">
        Built with ❤️ using Streamlit<br>
        AI Study Assistant · 2026
    </div>
    """, unsafe_allow_html=True)

# 5. Register application pages
pg = st.navigation(
    {
        "🏠 HOME": [
            st.Page(
                "pages/home_page.py",
                title="Home",
                icon="🏠",
                default=True,
            ),
        ],
        "📚 STUDY TOOLS": [
            st.Page(
                "pages/ask_question.py",
                title="Ask a Question",
                icon="💬",
            ),
            st.Page(
                "pages/summarise_notes.py",
                title="Summarise Notes",
                icon="📝",
            ),
            st.Page(
                "pages/quiz_generator.py",
                title="Quiz Generator",
                icon="🧠",
            ),
            st.Page(
                "pages/exam_prep.py",
                title="Exam Prep",
                icon="📅",
            ),
        ],
    }
)

# 6. Run selected page
pg.run()
