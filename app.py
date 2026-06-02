import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="7Up 7Down Predictor", page_icon="🎲", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    .big-font { font-size:26px !important; font-weight: bold; color: #4CAF50; text-align: center; }
    .prediction-box { padding: 20px; background-color: #1E1E1E; border-radius: 10px; border: 2px solid #4CAF50; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎲 7Up 7Down Smart Web Predictor")
st.write("Pehle pichle 3 rounds ka data enter karein, system agla round automatic predict karega.")

# --- Session State (Data ko yaad rakhne ke liye) ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Buttons Layout ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔽 7 DOWN (2-6)", use_container_width=True):
        st.session_state.history.append('down')

with col2:
    if st.button("🎯 EXACT 7", use_container_width=True):
        st.session_state.history.append('7')

with col3:
    if st.button("🔼 7 UP (8-12)", use_container_width=True):
        st.session_state.history.append('up')

# --- Reset Button ---
if st.button("🔄 Clear History / Reset", type="secondary"):
    st.session_state.history = []
    st.rerun()

# --- Prediction & Stats Logic ---
history = st.session_state.history
total = len(history)

if total >= 3:
    up_count = history.count('up')
    down_count = history.count('down')
    seven_count = history.count('7')

    # Display Stats
    st.subheader("📊 Live Statistics")
    st.write(f"**7 Up:** {round((up_count/total)*100, 1)}% | **7 Down:** {round((down_count/total)*100, 1)}% | **Exact 7:** {round((seven_count/total)*100, 1)}%")

    # Prediction Algorithm
    if history[-2:] == ['up', 'up']:
        prediction = "💥 NEXT PREDICTION: [ 7 DOWN ] (Streak Break Chance)"
    elif history[-2:] == ['down', 'down']:
        prediction = "💥 NEXT PREDICTION: [ 7 UP ] (Streak Break Chance)"
    elif up_count < down_count:
        prediction = "🔮 NEXT PREDICTION: [ 7 UP ] (Due to lower volume)"
    else:
        prediction = "🔮 NEXT PREDICTION: [ 7 DOWN ] (Due to lower volume)"

    # Show Prediction
    st.markdown("---")
    st.markdown(f"<div class='prediction-box'><p class='big-font'>{prediction}</p></div>", unsafe_allow_html=True)

else:
    st.info(f"⚠️ Data kam hai! Prediction ke liye kam se kam 3 rounds enter karein. (Abhi tak: {total})")

# --- History Log ---
if total > 0:
    st.markdown("---")
    st.write(f"**Recent History (Pichle {total} Rounds):**")
    st.write(" ➡️ ".join(history[-10:]))
    
