import os
import streamlit as st
from google import genai

# API key 
key = st.secrets["api_key"]

if not key:
    st.error("Missing API key. Set GENAI_API_KEY in CMD first.")
    st.stop()

client = genai.Client(api_key=key)

# Setup
st.set_page_config(page_title="AI Chatbot")
st.title("Poetry Assistant Chatbot")
st.caption("Chat with your AI poetry assistant")

# Conversation memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Store user message
    st.session_state.conversation.append({
        "role": "user",
        "content": user_input
    })

    # Build prompt from memory
    conversation_prompt = "\n".join(
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.conversation
    )

    # Call Gemini 
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=conversation_prompt
        )
        bot_reply = response.text

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    # Store response
    st.session_state.conversation.append({
        "role": "assistant",
        "content": bot_reply
    })

# Display chat
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
