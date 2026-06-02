import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="7Up 7Down Pro Predictor", page_icon="🎲", layout="centered")

st.title("🎲 7Up 7Down Pro Predictor")
st.write("Pehle 3 ya us se zyada rounds ka data enter karein taake live percentages calculate ho sakein.")

# --- Session State ---
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

history = st.session_state.history
total = len(history)

# --- Default Percentages (Jab data na ho) ---
p_down = 41.7
p_seven = 16.6
p_up = 41.7

if total >= 3:
    up_count = history.count('up')
    down_count = history.count('down')
    seven_count = history.count('7')
    
    # Base Math Probability (Jo asal mein hoti hai)
    # Ismein hum history ka weightage add kar rahe hain taake live prediction bane
    weight_down = 41.66 + (up_count - down_count) * 5
    weight_up = 41.66 + (down_count - up_count) * 5
    weight_seven = 16.66
    
    # Agar kisi side ki streak chal rahi ho to probability balance karne ke liye adjustment
    if history[-2:] == ['up', 'up']:
        weight_down += 15
        weight_up -= 15
    elif history[-2:] == ['down', 'down']:
        weight_up += 15
        weight_down -= 15

    # Negative values ko rokne ke liye guard rails
    weight_down = max(10, min(80, weight_down))
    weight_up = max(10, min(80, weight_up))
    
    # Total percentage ko 100 par balance karna
    total_weight = weight_down + weight_up + weight_seven
    p_down = round((weight_down / total_weight) * 100, 1)
    p_up = round((weight_up / total_weight) * 100, 1)
    p_seven = round((weight_seven / total_weight) * 100, 1)

st.markdown("---")
st.subheader("🔮 Live Prediction & Probability")

# --- 3 Stylish Boxes Layout ---
box_col1, box_col2, box_col3 = st.columns(3)

with box_col1:
    st.markdown(f"""
    <div style="padding: 15px; background-color: #1E3A8A; border-radius: 10px; border: 2px solid #3B82F6; text-align: center;">
        <p style="font-size: 16px; margin: 0; color: #93C5FD; font-weight: bold;">7 DOWN</p>
        <p style="font-size: 28px; margin: 5px 0 0 0; color: #FFFFFF; font-weight: bold;">{p_down}%</p>
    </div>
    """, unsafe_allow_html=True)

with box_col2:
    st.markdown(f"""
    <div style="padding: 15px; background-color: #7F1D1D; border-radius: 10px; border: 2px solid #EF4444; text-align: center;">
        <p style="font-size: 16px; margin: 0; color: #FCA5A5; font-weight: bold;">EXACT 7</p>
        <p style="font-size: 28px; margin: 5px 0 0 0; color: #FFFFFF; font-weight: bold;">{p_seven}%</p>
    </div>
    """, unsafe_allow_html=True)

with box_col3:
    st.markdown(f"""
    <div style="padding: 15px; background-color: #064E3B; border-radius: 10px; border: 2px solid #10B981; text-align: center;">
        <p style="font-size: 16px; margin: 0; color: #A7F3D0; font-weight: bold;">7 UP</p>
        <p style="font-size: 28px; margin: 5px 0 0 0; color: #FFFFFF; font-weight: bold;">{p_up}%</p>
    </div>
    """, unsafe_allow_html=True)

# --- Best Recommendation Banner ---
if total >= 3:
    highest_prob = max(p_down, p_up, p_seven)
    if highest_prob == p_down:
        rec_text = "RECOMMENDATION: Place bet on [ 7 DOWN ]"
        rec_color = "#3B82F6"
    elif highest_prob == p_up:
        rec_text = "RECOMMENDATION: Place bet on [ 7 UP ]"
        rec_color = "#10B981"
    else:
        rec_text = "RECOMMENDATION: Small bet on [ EXACT 7 ]"
        rec_color = "#EF4444"
        
    st.markdown(f"""
    <div style="margin-top: 15px; padding: 10px; background-color: #262626; border-radius: 5px; text-align: center; border-left: 5px solid {rec_color};">
        <p style="font-size: 16px; margin: 0; color: #FFFFFF; font-weight: bold;">{rec_text}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info(f"⚠️ Shuruati data add ho raha hai. Kam se kam 3 rounds enter karein. (Abhi tak: {total})")

# --- History Log ---
if total > 0:
    st.markdown("---")
    st.write(f"**Recent History (Last 10 Rounds):**")
    st.write(" ➡️ ".join(history[-10:]))
