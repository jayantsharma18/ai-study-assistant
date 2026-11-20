
import re
import streamlit as st
from utils.ai_client import chat

# Initialize session state
defaults = {
    "quiz_questions": [],
    "quiz_answers": {},
    "quiz_submitted": False,
    "quiz_score": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# Parse AI-generated questions
def parse_questions(raw_text):
    questions = []
    blocks = re.split(r"\n(?=Q?\d+[\.\)])", raw_text.strip())

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]

        if len(lines) < 6:
            continue

        question = re.sub(r"^Q?\d+[\.\)]\s*", "", lines[0])
        options = {}
        answer = ""
        explanation = ""

        for line in lines[1:]:
            match = re.match(r"^([A-D])[.):]\s*(.+)$", line, re.I)

            if match:
                options[match.group(1).upper()] = match.group(2).strip()

            elif line.lower().startswith("answer"):
                match = re.search(r"\b([A-D])\b", line, re.I)
                answer = match.group(1).upper() if match else ""

            elif line.lower().startswith("explanation"):
                explanation = re.sub(
                    r"(?i)^explanation[:\s]*", "", line
                ).strip()

        if question and len(options) == 4 and answer in options:
            questions.append({
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": explanation
            })

    return questions


# Styling
st.markdown("""
<style>
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}

.quiz-header {
    background: linear-gradient(120deg, #172554, #4338ca);
    padding: 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.quiz-header h1 {
    color: white;
    font-size: 32px;
}

.quiz-header p {
    color: #e0e7ff;
}

.question-card {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(129,140,248,0.25);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
}

.score-card {
    background: linear-gradient(120deg, #172554, #4338ca);
    padding: 25px;
    border-radius: 16px;
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)


# Page header
st.markdown("""
<div class="quiz-header">
    <h1>🧠 AI Quiz Generator</h1>
    <p>Test your knowledge, challenge yourself and track your learning progress.</p>
</div>
""", unsafe_allow_html=True)


# Quiz settings
st.subheader("⚙️ Create Your Quiz")

with st.container(border=True):
    topic = st.text_input(
        "📚 Enter a topic or subject",
        placeholder="e.g. Deep Learning, Python, Mathematics"
    )

    custom_text = st.text_area(
        "Or paste your study material",
        height=120,
        placeholder="Paste your notes here to generate a quiz from them..."
    )

    col1, col2 = st.columns(2)

    with col1:
        num_q = st.slider("Number of questions", 3, 10, 5)

    with col2:
        difficulty = st.select_slider(
            "Difficulty level",
            options=["Easy", "Medium", "Hard"],
            value="Medium"
        )

    gen_btn = st.button(
        "🎲 Generate My Quiz",
        type="primary",
        use_container_width=True
    )


# Generate quiz
if gen_btn:
    source = custom_text.strip() or topic.strip()

    if not source:
        st.warning("Please enter a topic or paste study material first.")

    else:
        system_msg = (
            f"Create exactly {num_q} {difficulty} multiple-choice questions "
            f"about: {source}. "
            "Each question must have four options A, B, C, D and exactly "
            "one correct answer. Verify that each answer letter points "
            "to the correct option. "
            "Use this exact format:\n"
            "Q1. Question text\n"
            "A) Option one\nB) Option two\nC) Option three\nD) Option four\n"
            "Answer: B\n"
            "Explanation: One sentence explanation.\n"
            "Number questions sequentially. Output only the questions."
        )

        with st.spinner("🧠 Creating your personalised quiz..."):
            try:
                raw = chat([
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": "Generate the quiz now."}
                ], temperature=0.2)

                parsed = parse_questions(raw)

                if len(parsed) == num_q:
                    st.session_state.quiz_questions = parsed
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_score = 0

                    st.success(f"Successfully generated {num_q} questions!")
                    st.rerun()

                else:
                    st.error(
                        f"Could read only {len(parsed)} of {num_q} questions. "
                        "Please try again."
                    )

                    with st.expander("AI output for debugging"):
                        st.text(raw)

            except Exception as e:
                st.error("Unable to generate your quiz.")
                st.caption(f"Technical details: {e}")


# Display questions
if st.session_state.quiz_questions and not st.session_state.quiz_submitted:

    st.divider()
    st.subheader("📝 Your Quiz")

    total = len(st.session_state.quiz_questions)

    st.caption(
        f"Total questions: {total} · Difficulty: {difficulty}"
    )

    for i, q in enumerate(st.session_state.quiz_questions):

        with st.container(border=True):
            st.markdown(f"**Question {i+1} of {total}**")
            st.markdown(f"### {q['question']}")

            choice = st.radio(
                f"Select your answer for question {i+1}",
                options=list(q["options"].keys()),
                format_func=lambda k, q=q: f"{k}) {q['options'][k]}",
                index=None,
                key=f"radio_{i}",
                label_visibility="collapsed"
            )

            if choice:
                st.session_state.quiz_answers[i] = choice

    answered = len(st.session_state.quiz_answers)
    st.progress(answered / total)

    st.caption(f"You have answered {answered} out of {total} questions.")

    all_answered = answered == total

    if st.button(
        "✅ Submit My Quiz",
        type="primary",
        disabled=not all_answered,
        use_container_width=True
    ):
        score = sum(
            st.session_state.quiz_answers.get(i) == q["answer"]
            for i, q in enumerate(st.session_state.quiz_questions)
        )

        st.session_state.quiz_score = score
        st.session_state.quiz_submitted = True
        st.rerun()


# Results dashboard
if st.session_state.quiz_submitted:

    st.divider()

    total = len(st.session_state.quiz_questions)
    score = st.session_state.quiz_score
    percentage = round(score / total * 100) if total else 0

    st.subheader("🏆 Your Quiz Results")

    st.markdown(f"""
    <div class="score-card">
        <h2 style="color:white;">Your Score</h2>
        <h1 style="color:white;font-size:48px;">{score}/{total}</h1>
        <h3 style="color:#e0e7ff;">{percentage}% Accuracy</h3>
    </div>
    """, unsafe_allow_html=True)

    st.progress(percentage / 100)

    if percentage >= 80:
        st.success("🎉 Excellent work! You have a strong understanding.")
    elif percentage >= 50:
        st.warning("👍 Good effort! Keep practising to improve.")
    else:
        st.error("📚 Keep learning. Review the explanations and try again.")

    st.subheader("📖 Review Your Answers")

    for i, q in enumerate(st.session_state.quiz_questions):

        chosen = st.session_state.quiz_answers.get(i, "—")
        correct = q["answer"]

        with st.expander(
            f"{'✅' if chosen == correct else '❌'} Question {i+1}: {q['question']}"
        ):
            st.write(
                f"**Your answer:** {chosen}) "
                f"{q['options'].get(chosen, 'Not answered')}"
            )

            st.write(
                f"**Correct answer:** {correct}) {q['options'][correct]}"
            )

            if q["explanation"]:
                st.info(q["explanation"])

    if st.button("🔄 Generate Another Quiz", use_container_width=True):

        st.session_state.quiz_questions = []
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
        st.session_state.quiz_score = 0

        st.rerun()


st.divider()
st.caption("🎓 Powered by Azure OpenAI · GPT-4.1-mini")
