
import streamlit as st

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    .hero {
        padding: 45px 35px;
        border-radius: 20px;
        background: linear-gradient(120deg, #172554, #312e81, #4338ca);
        color: white;
        margin-bottom: 30px;
    }

    .hero h1 {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
        color: white;
    }

    .hero p {
        font-size: 17px;
        color: #e0e7ff;
    }

    .feature-card {
        padding: 22px;
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 16px;
        min-height: 175px;
        margin-bottom: 15px;
    }

    .feature-card h3 {
        margin-top: 5px;
    }

    .feature-card p {
        color: #888;
        font-size: 14px;
    }

    .section-heading {
        font-size: 25px;
        font-weight: 700;
        margin: 30px 0 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
<div class="hero">
    <h1>🎓 AI Study Assistant</h1>
    <p>Your intelligent learning companion.</p>
    <p>Learn smarter, revise faster, and prepare better with AI.</p>
</div>
""", unsafe_allow_html=True)

# Welcome section
st.markdown("## Welcome to your learning dashboard 👋")
st.write(
    "Everything you need to make studying easier is available in one place."
)

st.markdown('<div class="section-heading">🚀 Explore Your Tools</div>',
            unsafe_allow_html=True)

# Feature cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2>💬</h2>
        <h3>Ask Question</h3>
        <p>Ask academic questions and get AI-powered explanations.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/ask_question.py",
                 label="Open Ask Question →",
                 icon="💬",
                 use_container_width=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2>📝</h2>
        <h3>Summarise Notes</h3>
        <p>Turn lengthy study material into clear, concise notes.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/summarise_notes.py",
                 label="Open Summariser →",
                 icon="📝",
                 use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h2>🧠</h2>
        <h3>Quiz Generator</h3>
        <p>Create multiple-choice quizzes and test your knowledge.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/quiz_generator.py",
                 label="Open Quiz Generator →",
                 icon="🧠",
                 use_container_width=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h2>📚</h2>
        <h3>Exam Preparation</h3>
        <p>Generate structured study material for your exams.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/exam_prep.py",
                 label="Open Exam Preparation →",
                 icon="📚",
                 use_container_width=True)

st.divider()

# Footer
st.markdown("""
<div style="text-align:center; padding:15px; color:gray;">
    <p>Made with ❤️ using Python, Streamlit and Azure OpenAI</p>
    <p>AI Study Assistant | Study Smarter. Achieve More.</p>
</div>
""", unsafe_allow_html=True)
