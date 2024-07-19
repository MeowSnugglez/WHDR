import streamlit as st

# Streamlit interface for input
st.title("Meow's AoS Damage Calculator")

# Attacker Profile
st.subheader("Attacker Profile")
num_rolls = st.number_input('Number of Attacks', min_value=1, value=10)
hits_threshold = st.number_input('Hitting on', min_value=1, max_value=6, value=4)
wounds_threshold = st.number_input('Wounding on', min_value=1, max_value=6, value=3)
rend = st.number_input('Rend', min_value=-6, max_value=6, value=0)  # Rend input field
damage = st.number_input('Damage', min_value=1, value=1)  # Damage input field
crits_threshold = st.number_input('Crit on ', min_value=1, max_value=6, value=6)  # Crits input field
# Add a checkbox for the "Crit 2-Attack" feature
crit_2_attack_enabled = st.checkbox('Crit 2 Hits')
crit_auto_wound_enabled = st.checkbox('Crit Auto-wound')
crit_mortal_enabled = st.checkbox('Crit Mortal')
# Defender Profile
st.subheader("Defender Profile")
saves_threshold = st.number_input('Armor Save', min_value=1, max_value=6, value=3)
ward_threshold = st.number_input('Ward', min_value=1, max_value=7, value=7)  # Adjust max_value if you want to allow values higher than 6

# Calculate the average successful rolls
def calculate_average_successes(num_rolls, threshold, crits_threshold, remove_success=False):
    # Calculate the probability of success or failure for a single roll
    if remove_success:
        probability = (threshold - 1) / 6.0  # Probability of failure (rolls below the threshold)
    else:
        probability = (7 - threshold) / 6.0  # Probability of success (rolls equal to or above the threshold)
    # Calculate the expected number of successes or failures
    expected_outcomes = num_rolls * probability

    # Calculate critical hits separately
    crit_hits = num_rolls * (1 / 6.0) * (7 - crits_threshold) if crits_threshold <= 6 else 0

    rounded_outcomes = round(expected_outcomes)
    rounded_crit_hits = round(crit_hits)
    return rounded_outcomes, rounded_crit_hits


# Button to start calculation
if st.button('Calculate Average Successes'):


    # Calculate the average successes for hits, including critical hits
    hits_average_successes, crit_hits = calculate_average_successes(num_rolls, hits_threshold, crits_threshold)
    total_hits = hits_average_successes
    automatic_wounds = 0
    if crit_2_attack_enabled:
        total_hits += crit_hits

    #Remove auto wounds from total hits    
    if crit_auto_wound_enabled:
        total_hits -= crit_hits
        automatic_wounds = crit_hits
    # Calculate the average successes for wounds based on the hits' successes
    wounds_average_successes, _ = calculate_average_successes(total_hits, wounds_threshold, crits_threshold)
    
    # Adjust the saves_threshold based on rend
    adjusted_saves_threshold = saves_threshold + rend
    # If the adjusted saves_threshold is 7 or higher, consider every armor save as unsuccessful
    if adjusted_saves_threshold >= 7:
        # When armor save + rend is 7 or greater, all wounds are unsaved
        unsaved_wounds_average_successes = wounds_average_successes
    else:
        # Calculate the average unsaved wounds based on the wounds' successes
        unsaved_wounds_average_successes, _ = calculate_average_successes(wounds_average_successes, adjusted_saves_threshold, crits_threshold, remove_success=True)
    
    total_wounds_received = unsaved_wounds_average_successes
    if crit_auto_wound_enabled:
        total_wounds_received += automatic_wounds
    # Calculate total damage
    total_damage = total_wounds_received * damage
    
    # Calculate the number of wounds that fail the ward save
    if ward_threshold >= 7:
    # If the ward value is 7 or greater, all damage bypasses the ward save
        ward_failures = total_damage
    else:
    # Calculate the number of wounds that fail the ward save
        ward_failures, _ = calculate_average_successes(total_damage, ward_threshold, crits_threshold, remove_success=True)

    
    # Display the results
    st.write(f"Hits")
    st.write(f"Normal:{hits_average_successes - crit_hits} | Critical: {crit_hits} | Total after Crit Modifiers: {total_hits}")
    if crit_auto_wound_enabled:
        st.write(f"Auto Wounds: {automatic_wounds}")
    st.write(f"Wounds: {wounds_average_successes}")
    st.write(f"Unsaved Wounds: {total_wounds_received}")
    st.write(f"Total damage before ward saves: {total_damage}")
    st.write(f"Damage after ward saves: {ward_failures}")
