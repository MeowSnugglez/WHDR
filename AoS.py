import streamlit as st

# Streamlit interface for input
st.title("Meow's AoS Damage Calculator")

# Attacker Profile
st.subheader("Attacker Profile")
num_rolls = st.number_input('Number of Attacks', min_value=1, value=10)
hits_threshold = st.number_input('Hitting on', min_value=1, max_value=6, value=4)
wounds_threshold = st.number_input('Wounding on', min_value=1, max_value=6, value=3)
damage = st.number_input('Damage', min_value=1, value=1)  # Damage input field
crit_auto_wound = st.checkbox('Crit Auto-Wound')  # Crit Auto-Wound checkbox

# Defender Profile
st.subheader("Defender Profile")
saves_threshold = st.number_input('Armor Save', min_value=1, max_value=6, value=3)
ward_threshold = st.number_input('Ward', min_value=1, max_value=6, value=4)  # Ward input field

# Calculate the average successful rolls
def calculate_average_successes(num_rolls, threshold, remove_success=False, auto_wound=False):
    # Calculate the probability of success or failure for a single roll
    if remove_success:
        probability = (threshold - 1) / 6.0  # Probability of failure (rolls below the threshold)
    else:
        probability = (7 - threshold) / 6.0  # Probability of success (rolls equal to or above the threshold)
    # Calculate the expected number of successes or failures
    expected_outcomes = num_rolls * probability

    # Adjust for auto-wounds on a hit roll of 6
    if auto_wound:
        auto_wounds = num_rolls / 6.0  # One-sixth of the rolls auto-wound
        expected_outcomes += auto_wounds  # Add auto-wounds to expected outcomes

    rounded_outcomes = round(expected_outcomes)
    return rounded_outcomes

# Button to start calculation
if st.button('Calculate Average Successes'):
    # Calculate the average successes for hits
    hits_average_successes = calculate_average_successes(num_rolls, hits_threshold)
    
    # Adjust the number of dice rolling for wounds if Crit Auto-Wound is checked
    auto_wounds = 0
    if crit_auto_wound:
        auto_wounds = num_rolls / 6.0  # One-sixth of the rolls auto-wound
    adjusted_rolls_for_wounds = num_rolls - round(auto_wounds)
    
    # Calculate the average successes for wounds based on the adjusted hits' successes
    wounds_average_successes = calculate_average_successes(adjusted_rolls_for_wounds, wounds_threshold) + round(auto_wounds)
    
    # Calculate the average unsaved wounds based on the wounds' successes
    unsaved_wounds_average_successes = calculate_average_successes(wounds_average_successes, saves_threshold, remove_success=True)
    
    # Calculate total damage
    total_damage = unsaved_wounds_average_successes * damage
    
    # Calculate the number of wounds that fail the ward save
    ward_failures = calculate_average_successes(total_damage, ward_threshold, remove_success=True)
    
    # Display the results
    st.write(f"Average hits successes: {hits_average_successes}")
    st.write(f"Average wounds successes: {wounds_average_successes}")
    st.write(f"Average unsaved wounds: {unsaved_wounds_average_successes}")
    st.write(f"Total damage before ward saves: {total_damage}")
    st.write(f"Damage after ward saves: {ward_failures}")
