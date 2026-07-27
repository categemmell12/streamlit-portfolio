import os
import streamlit as st
import requests
from google import genai

st.set_page_config(page_title="AI Poetry Generator")

api_key = st.secrets["api_key"]

if not api_key:
    st.error("Missing API key.")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("AI Poetry Generator")
st.write("Generate a new poem inspired by real authors")

# User input
author = st.text_input("Enter an author name:")
tone = st.selectbox(
    "Choose a tone:",
    ["Romantic", "Dark", "Hopeful", "Funny", "Dramatic"]
)
length = st.slider("Number of lines", 4, 20, 8)

# Same API
def get_poems(author):
    try:
        r = requests.get(f"https://poetrydb.org/author/{author}")
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []

# Button
if st.button("Generate Poem"):

    poems = get_poems(author)

    if not poems:
        st.error("Author not found.")
    else:
        # Use real API data
        sample = " ".join(
            " ".join(p["lines"]) for p in poems[:5]
        )[:1000]

        try:
            prompt = f"""
            Here are examples of poems by {author}:
            {sample}

            Write a NEW original poem inspired by this author.

            Tone: {tone}
            Length: about {length} lines
            """

            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )

            st.subheader("Generated Poem")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
