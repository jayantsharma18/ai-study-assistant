
import streamlit as st
from utils.ai_client import chat

# Initialize summary state
if "notes_summary" not in st.session_state:
    st.session_state.notes_summary = ""

# Custom styling
st.markdown("""
<style>
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

.summary-header {
    background: linear-gradient(120deg, #172554, #4338ca);
    padding: 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.summary-header h1 {
    color: white;
    font-size: 32px;
}

.summary-header p {
    color: #e0e7ff;
}

.summary-panel {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(129,140,248,0.25);
    border-radius: 14px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="summary-header">
    <h1>📝 Smart Notes Summariser</h1>
    <p>Transform lengthy study material into clear, structured revision notes.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📚 Create your summary")
st.write("Paste your notes, choose a format, and let AI organise the important information.")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📄 Your Study Material")

    notes = st.text_area(
        "Paste your notes here",
        height=350,
        placeholder="Paste lecture notes, textbook content, articles or study material..."
    )

    st.caption(f"Characters entered: {len(notes)}")

    summary_style = st.selectbox(
        "Choose summary format",
        [
            "Bullet points",
            "Short paragraph",
            "Key terms only"
        ]
    )

    summarise_btn = st.button(
        "✨ Generate Summary",
        type="primary",
        use_container_width=True
    )

    if st.button("🗑️ Clear notes and summary", use_container_width=True):
        st.session_state.notes_summary = ""
        st.rerun()

with col2:
    st.subheader("📋 AI Generated Summary")

    if summarise_btn:
        if not notes.strip():
            st.warning("Please paste your study notes first.")

        else:
            style_instructions = {
                "Bullet points": "clear, concise bullet points grouped by topic",
                "Short paragraph": "a short, easy-to-read paragraph of maximum 150 words",
                "Key terms only": "a glossary of important terms with one-line definitions"
            }

            system_msg = (
                "You are an expert academic study assistant. "
                f"Summarise the supplied notes as {style_instructions[summary_style]}. "
                "Preserve important facts, terminology and meaning. "
                "Do not invent information that is not present in the notes."
            )

            messages = [
                {"role": "system", "content": system_msg},
                {
                    "role": "user",
                    "content": f"Summarise these notes:\n\n{notes}"
                }
            ]

            with st.spinner("🧠 Analysing your notes..."):
                try:
                    summary = chat(messages, temperature=0.3)
                    st.session_state.notes_summary = summary

                except Exception as e:
                    st.error("Unable to generate your summary.")
                    st.caption(f"Technical details: {e}")

    if st.session_state.notes_summary:
        with st.container(border=True):
            st.markdown(st.session_state.notes_summary)

        st.download_button(
            "⬇️ Download Summary",
            data=st.session_state.notes_summary,
            file_name="AI_Study_Summary.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:
        with st.container(border=True):
            st.markdown("### ✨ Your summary will appear here")
            st.write("Your organised revision notes will be displayed after generation.")
            st.caption("Choose your preferred format and click Generate Summary.")

st.divider()
st.caption("🎓 Powered by Azure OpenAI · GPT-4.1-mini")
