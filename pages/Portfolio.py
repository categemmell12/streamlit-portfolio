import streamlit as st
import info

# Name
st.title(info.name)

# Profile Picture
st.image("images/profile.jpg", width=250)

# About Me
st.header("About Me")
st.write(info.about_me)

# Education
st.header("Education")

for key, value in info.education_data.items():
    st.write(f"**{key}:** {value}")

# Coursework
st.header("Relevant Coursework")

for i in range(len(info.course_data["code"])):
    st.write(
        f"**{info.course_data['code'][i]}** - "
        f"{info.course_data['names'][i]}"
    )

# Experience
st.header("Experience")

for job, details in info.experience_data.items():
    st.subheader(job)

    # Display image
    st.image(details[1], width=300)

    # Display bullets
    for bullet in details[0]:
        st.write(bullet)

# Projects
st.header("Projects")

for project, description in info.projects_data.items():
    st.subheader(project)
    st.write(description)

# Programming Skills
st.header("Programming Skills")

for skill, level in info.programming_data.items():
    st.write(f"{skill}: {level}%")

# Languages
st.header("Languages")

for language, level in info.spoken_data.items():
    st.write(f"{language}: {level}")

# Leadership
st.header("Leadership")

for position, details in info.leadership_data.items():
    st.subheader(position)

    # Display image
    st.image(details[1], width=300)

    for bullet in details[0]:
        st.write(bullet)

# Activities
st.header("Activities")

for activity, bullets in info.activity_data.items():
    st.subheader(activity)

    for bullet in bullets:
        st.write(bullet)

# Career Goal
st.header("Career Goal")
st.write(info.career_goal)

# Contact Information
st.header("Contact Information")

st.markdown(
    f"[LinkedIn]({info.my_linkedin_url})"
)

st.markdown(
    f"[GitHub]({info.my_github_url})"
)

st.write(info.my_email_address)
