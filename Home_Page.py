import streamlit as st

# Title of App
st.title("Web Development Lab03 and Lab04")

# Assignment Data 
# TODO: Fill out class and name

st.header("CS 1301")
st.subheader("Web Development")
st.subheader("Cate Gemmell")



st.write("""
Welcome to our Streamlit Web Development Lab03 Poetry app! You can navigate between the pages using the sidebar to the left. The following pages are:""")
st.divider()

st.page_link("pages/1_Poetry_Search.py", label = "Poetry Search", icon = "📚") 
st.write("Search for poems by author or by title! Data has been pulled from the Poetry Database API (https://poetrydb.org/).")
st.divider()
st.page_link("pages/2_Chatbot.py", label = "Poetry Chatbot", icon = "🗣️") 
st.write("Ask any question about poetry, poets, the history of poetry, and more!")
st.divider()
st.page_link("pages/3_Poetry_AI_Generator.py", label = "Poetry AI Generator", icon = "✏️") 
st.write("Generate a new poem inspired by real authors using AI and PoetryDB data.")
st.divider()
st.page_link("pages/4_Poetry_Whiz.py", label = "Poetry Whiz", icon = "💡") 
st.write("Ask questions about poems and authors using AI with live API data.")


