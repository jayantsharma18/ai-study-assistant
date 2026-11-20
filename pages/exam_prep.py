
import streamlit as st
from utils.ai_client import chat

# Initialize saved results
for key in ["study_plan", "topic_result", "answer_feedback"]:
    if key not in st.session_state:
        st.session_state[key] = ""

# Custom styling
st.markdown("""
<style>
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}

.exam-header {
    background: linear-gradient(120deg, #172554, #4338ca);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.exam-header h1 {
    color: white;
    font-size: 32px;
}

.exam-header p {
    color: #e0e7ff;
    font-size: 15px;
}

.tool-card {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(129,140,248,0.25);
    border-radius: 14px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="exam-header">
    <h1>📚 Exam Preparation Hub</h1>
    <p>Your personal AI-powered exam coach.</p>
    <p>Plan your preparation, prioritise important topics and improve your answers.</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.subheader("🎯 Prepare smarter, perform better")
st.write("Choose one of the tools below to improve your exam preparation.")

# Three tools
tab1, tab2, tab3 = st.tabs([
    "📆 Study Planner",
    "🎯 Topic Prioritiser",
    "✍️ Answer Feedback"
])

# TAB 1: STUDY PLANNER
with tab1:
    st.subheader("📆 Create Your Personalised Study Plan")
    st.write("Tell us about your upcoming exam and get a realistic daily schedule.")

    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            exam_subject = st.text_input(
                "Subject / Exam Name",
                placeholder="e.g. Introduction to Machine Learning"
            )

            days_left = st.number_input(
                "Days until exam",
                min_value=1,
                max_value=365,
                value=14
            )

        with col2:
            hours_per_day = st.slider(
                "Study hours per day",
                1, 12, 3
            )

            weak_topics = st.text_area(
                "Your difficult topics",
                height=110,
                placeholder="Enter one topic per line..."
            )

        generate_plan = st.button(
            "✨ Generate Study Plan",
            type="primary",
            use_container_width=True
        )

    if generate_plan:
        if not exam_subject.strip():
            st.warning("Please enter your subject name.")
        else:
            weak_list = weak_topics.strip() or "None specified"

            system_msg = (
                "You are an expert academic coach. "
                "Create a detailed, realistic day-by-day study plan. "
                "Format it with clear headings for each day. "
                "For every day specify topics, study tasks and a quick self-test. "
                "Include revision and practice time. Be encouraging and realistic."
            )

            user_msg = (
                f"Subject: {exam_subject}\n"
                f"Days until exam: {days_left}\n"
                f"Study hours per day: {hours_per_day}\n"
                f"Weak topics: {weak_list}"
            )

            with st.spinner("🧠 Building your study plan..."):
                try:
                    plan = chat(
                        [
                            {"role": "system", "content": system_msg},
                            {"role": "user", "content": user_msg}
                        ],
                        temperature=0.6
                    )

                    st.session_state.study_plan = plan

                except Exception as e:
                    st.error("Unable to generate your study plan.")
                    st.caption(f"Technical details: {e}")

    if st.session_state.study_plan:
        st.divider()
        st.subheader("📋 Your Personalised Study Plan")

        with st.container(border=True):
            st.markdown(st.session_state.study_plan)

        st.download_button(
            "⬇️ Download Study Plan",
            data=st.session_state.study_plan,
            file_name="study_plan.txt",
            mime="text/plain",
            use_container_width=True
        )


# TAB 2: TOPIC PRIORITISER
with tab2:
    st.subheader("🎯 Identify Your Important Topics")
    st.write("Enter your syllabus and let AI help organise your revision priorities.")

    with st.container(border=True):
        syllabus = st.text_area(
            "Paste your syllabus or topic list",
            height=220,
            placeholder="Chapter 1: Introduction\nChapter 2: Fundamentals\nChapter 3: Applications..."
        )

        exam_board = st.text_input(
            "Exam board or academic standard (optional)",
            placeholder="e.g. University semester examination"
        )

        prioritise_btn = st.button(
            "🎯 Prioritise My Topics",
            type="primary",
            use_container_width=True
        )

    if prioritise_btn:
        if not syllabus.strip():
            st.warning("Please paste your syllabus or topics first.")
        else:
            board_note = (
                f"for the {exam_board} syllabus"
                if exam_board.strip()
                else ""
            )

            system_msg = (
                "You are an experienced academic exam coach. "
                "Analyse the supplied topics and rank them by likely exam importance. "
                "Do not claim access to actual exam frequency data unless supplied. "
                "Clearly state that your ranking is an estimate. "
                "Use a table with columns: Rank, Topic, Why it matters, "
                "Suggested study time. Be concise and practical."
            )

            with st.spinner("🔍 Analysing your syllabus..."):
                try:
                    result = chat(
                        [
                            {"role": "system", "content": system_msg},
                            {
                                "role": "user",
                                "content": f"Topics {board_note}:\n\n{syllabus}"
                            }
                        ],
                        temperature=0.3
                    )

                    st.session_state.topic_result = result

                except Exception as e:
                    st.error("Unable to analyse your topics.")
                    st.caption(f"Technical details: {e}")

    if st.session_state.topic_result:
        st.divider()
        st.subheader("📊 Your Topic Priorities")

        with st.container(border=True):
            st.markdown(st.session_state.topic_result)


# TAB 3: ANSWER FEEDBACK
with tab3:
    st.subheader("✍️ Improve Your Exam Answers")
    st.write("Submit a practice answer and receive AI-powered feedback.")

    with st.container(border=True):
        q_text = st.text_input(
            "📝 Exam Question",
            placeholder="e.g. Explain the architecture of a CNN."
        )

        a_text = st.text_area(
            "Your Answer",
            height=250,
            placeholder="Write your answer here..."
        )

        marks = st.number_input(
            "Maximum marks",
            min_value=1,
            max_value=100,
            value=10
        )

        feedback_btn = st.button(
            "🔍 Evaluate My Answer",
            type="primary",
            use_container_width=True
        )

    if feedback_btn:
        if not q_text.strip() or not a_text.strip():
            st.warning("Please enter both the question and your answer.")
        else:
            system_msg = (
                "You are a strict but encouraging academic exam marker. "
                f"The question is worth {marks} marks. "
                "Evaluate the answer based on accuracy, depth, key terminology "
                "and structure. Give an estimated mark out of the maximum marks. "
                "Explain the strengths, missing points and specific improvements. "
                "Do not claim this is an official examination mark. "
                "End with one motivational sentence."
            )

            with st.spinner("📝 Evaluating your answer..."):
                try:
                    feedback = chat(
                        [
                            {"role": "system", "content": system_msg},
                            {
                                "role": "user",
                                "content": (
                                    f"Question: {q_text}\n\n"
                                    f"Student answer:\n{a_text}"
                                )
                            }
                        ],
                        temperature=0.4
                    )

                    st.session_state.answer_feedback = feedback

                except Exception as e:
                    st.error("Unable to evaluate your answer.")
                    st.caption(f"Technical details: {e}")

    if st.session_state.answer_feedback:
        st.divider()
        st.subheader("📊 Your Answer Evaluation")

        with st.container(border=True):
            st.markdown(st.session_state.answer_feedback)


st.divider()
st.caption("🎓 Powered by Azure OpenAI · GPT-4.1-mini")
