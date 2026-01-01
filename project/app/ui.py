import streamlit as st
from app.chat import answer_question

st.set_page_config(page_title="Personal Knowledge Brain")

st.title("🧠 Personal Knowledge Brain")

# User identity
user_id = st.text_input("Enter your username",value="rak")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask something about your documnents"):
    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("assistant"):
        answer = answer_question(user_id, prompt)
        st.markdown(answer)

    st.session_state.messages.append(
        {"role":"assistant","content":answer}
    )