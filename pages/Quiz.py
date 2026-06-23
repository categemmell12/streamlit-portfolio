import streamlit as st

# Title
st.title("Which Workout Style Fits You?")

st.write(
    "Answer the questions below to discover which workout style best matches your personality and fitness goals!"
)

# Images
st.image("images/pilates.jpg", width=250)
st.image("images/yoga.jpg", width=250)
st.image("images/running.jpg", width=250)

# Score Variables
pilates = 0
yoga = 0
strength = 0
running = 0

# Question 1
#NEW
q1 = st.radio(
    "What is your main fitness goal?",
    [
        "Build strength",
        "Improve flexibility",
        "Reduce stress",
        "Increase endurance"
    ]
)

if q1 == "Build strength":
    strength += 1
elif q1 == "Improve flexibility":
    pilates += 1
elif q1 == "Reduce stress":
    yoga += 1
elif q1 == "Increase endurance":
    running += 1

# Question 2
#NEW
q2 = st.slider(
    "How intense do you like your workouts?",
    1,
    10,
    5
)

if q2 >= 8:
    strength += 1
    running += 1
elif q2 >= 5:
    pilates += 1
else:
    yoga += 1

# Question 3
#NEW
q3 = st.selectbox(
    "Choose your ideal workout location:",
    [
        "Gym",
        "Yoga Studio",
        "Pilates Studio",
        "Outdoor Trail"
    ]
)

if q3 == "Gym":
    strength += 1
elif q3 == "Yoga Studio":
    yoga += 1
elif q3 == "Pilates Studio":
    pilates += 1
elif q3 == "Outdoor Trail":
    running += 1

# Question 4
#NEW
q4 = st.number_input(
    "How many days per week do you typically exercise?",
    min_value=0,
    max_value=7,
    value=3
)

if q4 >= 5:
    strength += 1
    running += 1
elif q4 >= 3:
    pilates += 1
else:
    yoga += 1

# Question 5
#NEW
q5 = st.multiselect(
    "Which qualities are most important to you in a workout?",
    [
        "Balance",
        "Flexibility",
        "Power",
        "Mental Wellness",
        "Stamina"
    ]
)

if "Balance" in q5:
    pilates += 1

if "Flexibility" in q5:
    yoga += 1

if "Power" in q5:
    strength += 1

if "Mental Wellness" in q5:
    yoga += 1

if "Stamina" in q5:
    running += 1

# Quiz Button
if st.button("Find My Workout Style"):

    scores = {
        "Pilates": pilates,
        "Yoga": yoga,
        "Strength Training": strength,
        "Running": running
    }

    result = max(scores, key=scores.get)

    st.header("Your Result")

    if result == "Pilates":
        st.success("Pilates")
        st.write(
            "You enjoy mindful movement, core strength, flexibility, and balance. Pilates is the perfect workout style for you!"
        )
        st.image("images/pilates.jpg", width=300)

    elif result == "Yoga":
        st.success("Yoga")
        st.write(
            "You value flexibility, stress relief, and mind-body connection. Yoga is your ideal workout!"
        )
        st.image("images/yoga.jpg", width=300)

    elif result == "Strength Training":
        st.success("Strength Training")
        st.write(
            "You enjoy challenging yourself and building power. Strength training is a great fit for your goals!"
        )
        st.image("images/strength.jpg", width=300)

    elif result == "Running":
        st.success("Running")
        st.write(
            "You thrive on endurance, energy, and staying active. Running is the workout style that best matches you!"
        )
        st.image("images/running.jpg", width=300)

    #NEW
    st.balloons()
