import streamlit as st

# Streamlit interface for input
st.title('Dice Roll Average Calculator')
num_rolls = st.number_input('Number of Rolls', min_value=1, value=10)
first_threshold = st.number_input('First Roll Threshold (4 or higher)', min_value=1, max_value=6, value=4)
second_threshold = st.number_input('Second Roll Threshold (3 or higher)', min_value=1, max_value=6, value=3)

# Calculate the average successful rolls
def calculate_average_successes(num_rolls, threshold):
    # Calculate the probability of success for a single roll
    probability_of_success = (7 - threshold) / 6.0
    # Calculate the expected number of successes
    expected_successes = num_rolls * probability_of_success
    return expected_successes

# Button to start calculation
if st.button('Calculate Average Successes'):
    # Calculate the average successes for the first roll
    first_roll_average_successes = calculate_average_successes(num_rolls, first_threshold)
    
    # Calculate the average successes for the second roll based on the first roll's successes
    second_roll_average_successes = calculate_average_successes(first_roll_average_successes, second_threshold)
    
    # Display the results
    st.write(f"Average first roll successes: {first_roll_average_successes}")
    st.write(f"Average second roll successes: {second_roll_average_successes}")
