
import os
import streamlit as st
from google import genai
from google.genai import types
import requests
import time

# set_page_config MUST be first
st.set_page_config(page_title="Poetry Whiz")

api_key = st.secrets["api_key"]

if not api_key:
    st.error("Missing API key.")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("Poetry Assistant Chatbot")
st.write("Have a question about the Poetry Database? Ask away!")
st.write("""Examples of what you can ask include:
- What is Shakespeare's longest poem?
- Find me a poem about grief
- Is Maya Angelou in the Poetry Database?
- Find the poem called 'I Wandered Lonely as a Cloud'
""")

# -----------------------------
# 🔹 TOOL FUNCTIONS
# -----------------------------
def get_poems_by_author(author):
    try:
        r = requests.get(f"https://poetrydb.org/author/{author}")
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []

def get_poem_by_title(title):
    try:
        r = requests.get(f"https://poetrydb.org/title/{title}")
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []

def search_poems_by_keyword(keyword):
    try:
        r = requests.get(f"https://poetrydb.org/lines/{keyword}")
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []

def get_longest_poem(author):
    poems = get_poems_by_author(author)
    if not poems:
        return None
    return max(poems, key=lambda p: len(p.get("lines", [])))


# TOOL SCHEMA 

tools = types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="get_poems_by_author",
        description="Get poems written by a specific author",
        parameters=types.Schema(
            type="OBJECT",
            properties={"author": types.Schema(type="STRING")},
            required=["author"]
        )
    ),
    types.FunctionDeclaration(
        name="get_poem_by_title",
        description="Get a poem by its title",
        parameters=types.Schema(
            type="OBJECT",
            properties={"title": types.Schema(type="STRING")},
            required=["title"]
        )
    ),
    types.FunctionDeclaration(
        name="search_poems_by_keyword",
        description="Search poems containing a keyword",
        parameters=types.Schema(
            type="OBJECT",
            properties={"keyword": types.Schema(type="STRING")},
            required=["keyword"]
        )
    ),
    types.FunctionDeclaration(
        name="get_longest_poem",
        description="Find the longest poem by a given author",
        parameters=types.Schema(
            type="OBJECT",
            properties={"author": types.Schema(type="STRING")},
            required=["author"]
        )
    ),
])


# TOOL EXECUTION HANDLER

def call_tool(tool_name, args):
    if tool_name == "get_poems_by_author":
        return get_poems_by_author(args["author"])
    elif tool_name == "get_poem_by_title":
        return get_poem_by_title(args["title"])
    elif tool_name == "search_poems_by_keyword":
        return search_poems_by_keyword(args["keyword"])
    elif tool_name == "get_longest_poem":
        return get_longest_poem(args["author"])
    return None


# SAFE GEMINI CALL 

def safe_generate(**kwargs):
    for i in range(3):
        try:
            return client.models.generate_content(**kwargs)
        except Exception as e:
            err = str(e)
            if "503" in err:
                time.sleep(2 * (i + 1))
            elif "429" in err:
                wait = 10 * (i + 1)  # 10s, 20s, 30s
                st.toast(f"Rate limit hit — retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise e
    raise Exception("Rate limit exceeded — please wait a moment and try again.")


# MAIN CHAT FUNCTION

def run_chat(history):
    # Build contents list from full conversation history
    contents = [
        types.Content(
            role="user" if msg["role"] == "user" else "model",
            parts=[types.Part(text=msg["content"])]
        )
        for msg in history
    ]

    try:
        response = safe_generate(
            model="models/gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(tools=[tools])
        )

        # Check for tool call in response parts
        part = response.candidates[0].content.parts[0]

        if hasattr(part, "function_call") and part.function_call:
            fc = part.function_call
            tool_result = call_tool(fc.name, dict(fc.args))

            # Send tool result back with full context
            follow_up = safe_generate(
                model="models/gemini-2.5-flash",
                contents=contents + [
                    types.Content(
                        role="model",
                        parts=[types.Part(function_call=fc)]
                    ),
                    types.Content(
                        role="user",
                        parts=[types.Part(
                            function_response=types.FunctionResponse(
                                name=fc.name,
                                response={"result": str(tool_result)}
                            )
                        )]
                    )
                ],
                config=types.GenerateContentConfig(tools=[tools])
            )
            return follow_up.text

        return response.text

    except Exception as e:
        if "overloaded" in str(e):
            return "⚠️ The model is busy right now. Try again in a few seconds."
        elif "Rate limit" in str(e):
            return "⚠️ You've hit the API rate limit. Please wait a moment before sending another message."
        return f"Error: {str(e)}"

# Conversation memory

if "conversation" not in st.session_state:
    st.session_state.conversation = []


# User input

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.conversation.append({"role": "user", "content": user_input})
    bot_reply = run_chat(st.session_state.conversation)  # pass full history
    st.session_state.conversation.append({"role": "assistant", "content": bot_reply})


# Display chat

for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])






        
