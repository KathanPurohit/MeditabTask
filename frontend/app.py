import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
user_input = st.chat_input(
    "Type your message..."
)

if user_input:

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # API Request
    response = requests.post(
        API_URL,
        json={
            "message": user_input
        }
    )

    data = response.json()

    bot_response = data["response"]
    suggestions = data["suggestions"]

    # Save Assistant Response
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })

    with st.chat_message("assistant"):

        st.markdown(bot_response)

        st.subheader("Suggested Questions")

        for suggestion in suggestions:
            st.button(suggestion)