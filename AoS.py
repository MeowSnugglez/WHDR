import streamlit as st
import random

# Streamlit interface for input
st.title('Dice Roll Simulator')
num_rolls = st.number_input('Number of Rolls', min_value=1, value=10)
first_threshold = st.number_input('First Roll Threshold (4 or higher)', min_value=1, max_value=6, value=4)
second_threshold = st.number_input('Second Roll Threshold (3 or higher)', min_value=1, max_value=6, value=3)

# Button to start simulation
if st.button('Simulate Rolls'):
    # Simulate the first roll
    first_roll_successes = sum(random.randint(1, 6) >= first_threshold for _ in range(num_rolls))

    # Simulate the second roll only for the successful ones from the first roll
    second_roll_successes = sum(random.randint(1, 6) >= second_threshold for _ in range(first_roll_successes))

    # Display the results
    st.write(f"First roll successes: {first_roll_successes}")
    st.write(f"Second roll successes: {second_roll_successes}")
