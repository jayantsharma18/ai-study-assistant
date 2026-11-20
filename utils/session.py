"""
utils/session.py
----------------
Manages Streamlit's session_state so every page shares the same data.

session_state is Streamlit's way of remembering things between reruns
(like a mini in-memory database for your app).
"""

import streamlit as st


def init_session() -> None:
    """
    Initialise all session variables once when the app first loads.
    Calling this multiple times is safe — it won't overwrite existing data.
    """
    defaults = {
        # --- Q&A page ---
        "chat_history": [],         # list of {"role":..., "content":...}

        # --- Quiz page ---
        "quiz_questions": [],       # list of parsed MCQ dicts
        "quiz_answers": {},         # {question_index: chosen_option}
        "quiz_submitted": False,    # has the student submitted the quiz?
        "quiz_score": 0,            # number of correct answers

        # --- Notes page ---
        "notes_summary": "",        # last generated summary
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
