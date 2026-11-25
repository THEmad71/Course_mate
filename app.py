
import streamlit as st
from graph_engine import ask_graph

import os
import streamlit as st

# Load Streamlit Cloud secrets into environment
for key in [
    "GEMINI_API_KEY",
    "QDRANT_URL",
    "QDRANT_API_KEY"
]:
    if key in st.secrets:
        os.environ[key] = str(st.secrets[key])

# Import after loading secrets
from graph_engine import ask_graph


# 1. Page Configuration
st.set_page_config(
    page_title="CourseMate",
    page_icon="🎓",
    layout="centered"
)


# 2. Custom Styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)


# 3. Header
st.markdown(
    '<div class="main-title">🎓 CourseMate</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-powered IIUC CSE Academic Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []


# 5. Clear Chat Button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# 6. Display Previous Messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# 7. Student Input
question = st.chat_input(
    "Ask about IIUC CSE courses..."
)


# 8. Process Student Question
if question:

    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)


    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("CourseMate is thinking..."):

            try:

                answer = ask_graph(question)

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(
                    "Something went wrong. Please try again."
                )

                print("CourseMate Error:", str(e))
