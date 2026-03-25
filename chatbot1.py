import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")

API_KEY = os.getenv("API_KEY")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (bottom)
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                url = "https://openrouter.ai/api/v1/chat/completions"

                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                }

                data = {
                    "model": "meta-llama/llama-3-8b-instruct",
                    "messages": [
                        {"role": "user", "content": user_input}
                    ]
                }

                response = requests.post(url, headers=headers, json=data)

                if response.status_code != 200:
                    reply = f"⚠️ Error {response.status_code}"
                else:
                    res = response.json()
                    reply = res["choices"][0]["message"]["content"]

            except Exception as e:
                reply = f"⚠️ Error: {e}"

        st.markdown(reply)

    # Save bot reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

port=int(os.environ.get("PORT",8501))
