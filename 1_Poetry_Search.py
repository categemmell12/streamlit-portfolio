import streamlit as st
import requests
import altair as alt
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.title("Poetry Time...")



# === Retrieving API data

def authorSearch(author):
    baseURL = "https://poetrydb.org/author/"
    endpoint = baseURL + author.lower()
    try:
        r = requests.get(endpoint)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, dict):
            return None
        return data
    
    except requests.exceptions.RequestException:
        st.error("Please enter an author name.")

def titleSearch(title):
    baseURL = "https://poetrydb.org/title/"
    endpoint = baseURL + title.lower()
    try:
        r = requests.get(endpoint)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, dict):
            return None
        return data
    
    except requests.exceptions.RequestException:
        st.error("Network error. Please try again later.")
        
st.title("📚 Poetry Search")

author_input = st.text_input("""Enter an author's name.
If you don't know where to start, try searching for Shakespeare, Emily Dickinson, or John
Donne.""")

if st.button("Search by author."):
    if author_input.strip() == "":
        st.warning("Please enter an author name.")
    else:
        poems = authorSearch(author_input)

        if poems == "error":
            st.error("Network error. Try again later.")

        elif poems is None:
            st.error("Author not found.")

        else:
            st.success(f"Showing poems by {author_input.title()}")

            for poem in poems[:10]:
                title = poem["title"]
                author_name = poem["author"]
                lines = poem["lines"]

                st.header(title)
                st.subheader(f"by {author_name}")

                poem_text = "\n".join(lines)
                st.markdown(poem_text)

                st.divider()

title_input = st.text_input("Enter the title of a poem:")

if st.button("Search by poem title."):
    if title_input.strip() == "":
        st.warning("Please enter a poem title.")
    else:
        poems = titleSearch(title_input)

        if poems == "error":
            st.error("Network error. Try again later.")

        elif poems is None:
            st.error("Poem not found.")

        else:
            

            for poem in poems:
                title = poem["title"]
                authorName = poem["author"]
                lines = poem["lines"]
                st.success(f"Showing **{title}** by {authorName}")
                
                poem_text = "\n".join(lines)
                st.text(poem_text)

                st.divider()
st.divider()

if st.button("Feeling Indecisive?"):
    r = requests.get("https://poetrydb.org/random")
    poem = r.json()[0]

    st.header(poem["title"])
    st.subheader(f'by {poem["author"]}')
    st.text("\n".join(poem["lines"]))


# === User Inputs (2 Required)
    # longest and shortest poems



# === Dynamic Visual Representation (2 Required)
    # (can be images, graph, plots)
    # could be used to display a specific poem?
    # 1. random poem button
    # 2. Search for a poem
    # 3. top 5 poets and how many poems they've writen



# === Dynamic/Interactable Chart or Graph
    # display how many poems have certain linecounts?

st.divider()

st.subheader("📊 Linecount Graph")
st.write("Here, you can see specific linecount data for the author you have searched.")

def linecountData(poems):
    line_counts = [int(poem["linecount"]) for poem in poems]

    df = pd.DataFrame(line_counts, columns=["linecount"])
    freq = df["linecount"].value_counts().reset_index()
    freq.columns = ["linecount", "count"]

    return df, freq.sort_values("linecount")


df = None
freq = None 

poems = authorSearch(author_input)



if poems == "error":
    st.warning("Please input an author's name.")

elif poems:
    df, freq = linecountData(poems)


if freq is not None:
    st.subheader("📊 Line Count Distribution (Histogram)")

    line_counts = [int(poem["linecount"]) for poem in poems]
    avg = np.mean(line_counts)

    bin_size = st.slider("Number of bins", 5, 50, 20)

    hist = alt.Chart(df).mark_bar().encode(
        alt.X("linecount:Q", bin=alt.Bin(maxbins=bin_size), title="Line Count"),
        alt.Y("count()", title="Number of Poems"),
        alt.Color("count():Q", scale=alt.Scale(scheme="spectral")),
        tooltip=["count()"]
)
    avg_line = alt.Chart(pd.DataFrame({"avg": [avg]})).mark_rule(color="green", size=3).encode(
    x="avg:Q")

    avg_text = alt.Chart(pd.DataFrame({"avg": [avg]})).mark_text(
    text="Average",
    dy=-10,
    color="black"
).encode(
    x="avg:Q"
)

    chart = (hist + avg_line + avg_text).interactive()
    st.altair_chart(chart, use_container_width=True)
    st.write(f"📌 Average line count: {avg:.2f}")

st.divider()

st.subheader("📦 Line Count Summary (Box Plot)")

st.write("**How to read a boxplot**")
st.write(""" A box plot divides your data into quadrants, with the box part representing
the middle 50% of your data. The lines sticking out of the box show the range of most poem
lengths, while any dots way off the line represent outliers in the data.
""")

boxplot = alt.Chart(df).mark_boxplot(color="#4E792A").encode(
x=alt.X("linecount:Q", title="Line Count"))

st.altair_chart(boxplot, use_container_width=True)


st.divider()

st.subheader("☁️ Poetry Wordcloud")
st.write("Once you have searched for an author, you can see here which words they use the most in their poetry!"
)



if not author_input or author_input.strip() == "":
    st.warning("Please enter an author's name to see their wordcloud.")
    st.stop()

if poems == "error" or not poems:
    st.error("No poems found or network error.")
    st.stop()
text = " ".join(
    " ".join(poem["lines"]) for poem in poems)

wordcloud = WordCloud(width=800, height=400,
                      background_color="#DBEDCC",
                      colormap = "viridis"
                      ).generate(text)

fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig)

if st.checkbox("Show raw data"):
    st.dataframe(freq)



    

    
