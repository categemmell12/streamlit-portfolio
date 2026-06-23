import streamlit as st

# Page Title
st.title("Cate Gemmell")

# Course Information
st.header("CS 1301 - Web Development Lab 01")

# Welcome Message
st.write("""
Welcome to my Streamlit web application!

This website contains multiple pages that showcase my portfolio and an interactive quiz. Use the navigation menu on the left to explore each page.
""")

# Page Descriptions
st.subheader("Website Pages")

st.write("""
**Home Page:** Provides an overview of the website and explains the purpose of each page.

**Portfolio:** Highlights my education, leadership experiences, work experience, skills, and future career goals.

**Which Workout Style Fits You? Quiz:** Answer a series of questions to discover which workout style best matches your personality, fitness goals, and preferences.
""")

# Optional Divider
st.divider()

# Optional Closing Message
st.write("Thank you for visiting my website!")

