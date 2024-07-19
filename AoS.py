# a simple python application that calculates the chance of rolling certain numbers on a 6 sided die twice in a row
# should be able to set the values of the dice and the number of rolls
# values should be different between rolls
# for instance, if you have 10 dice rolls, for the hits you want to see how many dice on average using integers would be 4 or higher, after that for the wounds it would only be the number of dice that had 4 or higher on hits and wounds would check how many are 3 or higher

import streamlit as st

# Streamlit interface for input
st.title('Dice Roll Average Calculator')
num_rolls = st.number_input('Number of Rolls', min_value=1, value=10)
hits_threshold = st.number_input('Hits Threshold (4 or higher)', min_value=1, max_value=6, value=4)
wounds_threshold = st.number_input('Wounds Threshold (3 or higher)', min_value=1, max_value=6, value=3)

# Calculate the average successful rolls
def calculate_average_successes(num_rolls, threshold):
    # Calculate the probability of success for a single roll
    probability_of_success = (7 - threshold) / 6.0
    # Calculate the expected number of successes
    expected_successes = num_rolls * probability_of_success

    rounded_successes = round(expected_successes)
    return rounded_successes

# Button to start calculation
if st.button('Calculate Average Successes'):
    # Calculate the average successes for hits
    hits_average_successes = calculate_average_successes(num_rolls, hits_threshold)
    
    # Calculate the average successes for wounds based on the hits' successes
    wounds_average_successes = calculate_average_successes(hits_average_successes, wounds_threshold)
    
    # Display the results
    st.write(f"Average hits successes: {hits_average_successes}")
    st.write(f"Average wounds roll successes: {wounds_average_successes}")
