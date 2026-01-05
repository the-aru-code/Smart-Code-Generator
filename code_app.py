import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("API key not found. Please set GOOGLE_API_KEY in .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Page config
st.set_page_config(page_title="Gemini Code Generator", page_icon="🤖")
st.title("🧠 Smart CG")
st.write("Describe the code you want, and select a programming language.")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.text_area("Describe your code:")
language = st.selectbox(
    "Choose a programming language",
    ["Python", "JavaScript", "Java", "C++"]
)

# Generate button
if st.button("Generate Code"):
    if user_prompt.strip() == "":
        st.warning("Please enter a description.")
    else:
        # Store user message
        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )

        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Gemini response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full_prompt = f"""
Generate clean, well-commented {language} code for the following request:

{user_prompt}
"""
                response = st.session_state.chat.send_message(full_prompt)
                assistant_reply = response.text

                placeholder = st.empty()
                typed_text = ""

                for char in assistant_reply:
                    typed_text += char
                    placeholder.markdown(typed_text)
                    time.sleep(0.002)

        # Store assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

# Reset button
if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []
    st.rerun()

st.markdown("**Designed and developed by: Arushi Pandey**")
