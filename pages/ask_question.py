
import streamlit as st
from utils.ai_client import chat

# Initialize chat history safely
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom styling
st.markdown("""
<style>
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

.chat-header {
    background: linear-gradient(120deg, #172554, #4338ca);
    padding: 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.chat-header h1 {
    color: white;
    font-size: 32px;
    margin-bottom: 8px;
}

.chat-header p {
    color: #e0e7ff;
    font-size: 15px;
}

.prompt-card {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(129,140,248,0.25);
    border-radius: 12px;
    padding: 15px;
    min-height: 85px;
}
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="chat-header">
    <h1>💬 AI Study Tutor</h1>
    <p>Ask questions, understand difficult concepts and learn at your own pace.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.divider()
    st.subheader("⚙️ Tutor Settings")

    subject = st.selectbox(
        "Choose your subject",
        [
            "General",
            "Mathematics",
            "Science",
            "History",
            "English",
            "Computer Science"
        ]
    )

    simplify = st.toggle(
        "Explain like I'm 12 years old",
        value=False
    )

    st.caption("Your tutor will adjust its explanations based on these settings.")

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# Suggested prompts when conversation is empty
if not st.session_state.chat_history:
    st.subheader("👋 What would you like to learn today?")
    st.write("Start by asking your AI tutor a question.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="prompt-card">
            <b>🧠 Understand concepts</b><br>
            <small>Learn difficult topics in simple language.</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="prompt-card">
            <b>💻 Programming help</b><br>
            <small>Understand code and programming concepts.</small>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="prompt-card">
            <b>📐 Solve problems</b><br>
            <small>Get step-by-step academic explanations.</small>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="prompt-card">
            <b>📚 Exam preparation</b><br>
            <small>Revise important topics for your exams.</small>
        </div>
        """, unsafe_allow_html=True)

# Display previous conversation
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask your AI tutor anything...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    simplify_instruction = (
        "Explain everything in very simple language suitable for a 12-year-old child."
        if simplify
        else "Explain clearly and accurately with useful examples where appropriate."
    )

    system_prompt = (
        f"You are a helpful and encouraging AI study tutor specialising in {subject}. "
        f"{simplify_instruction} "
        "Break difficult concepts into understandable steps. "
        "Format formulas, code and important points clearly. "
        "Be accurate, concise and educational."
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages += st.session_state.chat_history
    messages.append({"role": "user", "content": user_input})

    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        with st.spinner("🧠 Your AI tutor is thinking..."):
            try:
                reply = chat(messages)
                st.markdown(reply)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": reply}
                )

            except Exception as e:
                st.error("Something went wrong while contacting the AI tutor.")
                st.caption(f"Technical details: {e}")

                # Remove the unanswered message so it can be retried
                st.session_state.chat_history.pop()

st.divider()
st.caption("🎓 Powered by Azure OpenAI · GPT-4.1-mini")
