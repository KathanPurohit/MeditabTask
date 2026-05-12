import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 Autonomous AI Chatbot")
st.markdown("I am powered by local Ollama models and have access to tools like a **Calculator** and **Current Time**.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def submit_suggestion(suggestion):
    st.session_state.suggestion_submitted = suggestion

if st.session_state.suggestions:
    st.write("💡 **Suggested follow-ups:**")
    for suggestion in st.session_state.suggestions:
        st.button(suggestion, on_click=submit_suggestion, args=(suggestion,), use_container_width=True)

user_input = st.chat_input("Type your message here...")

query = user_input
if "suggestion_submitted" in st.session_state:
    query = st.session_state.suggestion_submitted
    del st.session_state.suggestion_submitted

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.suggestions = [] # clear suggestions while loading
    
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and using tools..."):
            try:
                response = requests.post(API_URL, json={"message": query})
                response.raise_for_status()
                data = response.json()
                bot_response = data.get("response", "I couldn't process that.")
                st.session_state.suggestions = data.get("suggestions", [])
                
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"Error communicating with backend: {e}")
                
    st.rerun()