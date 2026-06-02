import streamlit as st

# --- Page Configuration & No-Scroll CSS ---
st.set_page_config(page_title="7Up 7Down Pro", page_icon="🎲", layout="centered")

# CSS se margins aur text size ko mobile ke mutabiq chota aur tight kiya hai
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    h1 { font-size: 24px !important; margin-bottom: 5px !important; text-align: center; }
    div.stButton > button { padding: 8px 5px !important; font-size: 14px !important; }
    .stToast { bottom: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Top Header & Reset Row ---
head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    st.markdown("<h1>🎲 7Up 7Down Pro</h1>", unsafe_allow_html=True)
with head_col2:
    if st.button("🔄 Clear", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# --- Session State ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Data Input Buttons ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔽 DOWN", use_container_width=True):
        st.session_state.history.append('down')
        st.toast("Data Added [ 7 DOWN ] Successfully.! ✅", icon="🟢")

with col2:
    if st.button("🎯 EXACT 7", use_container_width=True):
        st.session_state.history.append('7')
        st.toast("Data Added [ EXACT 7 ] Successfully.! ✅", icon="🟢")

with col3:
    if st.button("🔼 UP", use_container_width=True):
        st.session_state.history.append('up')
        st.toast("Data Added [ 7 UP ] Successfully.! ✅", icon="🟢")

history = st.session_state.history
total = len(history)

# --- Default Percentages ---
p_down, p_seven, p_up = 41.7, 16.6, 41.7

if total >= 3:
    up_count, down_count, seven_count = history.count('up'), history.count('down'), history.count('7')
    
    weight_down = 41.66 + (up_count - down_count) * 5
    weight_up = 41.66 + (down_count - up_count) * 5
    weight_seven = 16.66
    
    if history[-2:] == ['up', 'up']:
        weight_down += 15; weight_up -= 15
    elif history[-2:] == ['down', 'down']:
        weight_up += 15; weight_down -= 15

    weight_down = max(10, min(80, weight_down))
    weight_up = max(10, min(80, weight_up))
    
    total_weight = weight_down + weight_up + weight_seven
    p_down = round((weight_down / total_weight) * 100, 1)
    p_up = round((weight_up / total_weight) * 100, 1)
    p_seven = round((weight_seven / total_weight) * 100, 1)

# --- 3 Stylish Boxes Layout ---
st.markdown("<p style='margin: 8px 0 2px 0; font-weight:bold; font-size:14px;'>🔮 Probabilities:</p>", unsafe_allow_html=True)
box_col1, box_col2, box_col3 = st.columns(3)

with box_col1:
    st.markdown(f"""
    <div style="padding: 8px; background-color: #1E3A8A; border-radius: 8px; border: 2px solid #3B82F6; text-align: center;">
        <p style="font-size: 12px; margin: 0; color: #93C5FD; font-weight: bold;">7 DOWN</p>
        <p style="font-size: 20px; margin: 0; color: #FFFFFF; font-weight: bold;">{p_down}%</p>
    </div>
    """, unsafe_allow_html=True)

with box_col2:
    st.markdown(f"""
    <div style="padding: 8px; background-color: #7F1D1D; border-radius: 8px; border: 2px solid #EF4444; text-align: center;">
        <p style="font-size: 12px; margin: 0; color: #FCA5A5; font-weight: bold;">EXACT 7</p>
        <p style="font-size: 20px; margin: 0; color: #FFFFFF; font-weight: bold;">{p_seven}%</p>
    </div>
    """, unsafe_allow_html=True)

with box_col3:
    st.markdown(f"""
    <div style="padding: 8px; background-color: #064E3B; border-radius: 8px; border: 2px solid #10B981; text-align: center;">
        <p style="font-size: 12px; margin: 0; color: #A7F3D0; font-weight: bold;">7 UP</p>
        <p style="font-size: 20px; margin: 0; color: #FFFFFF; font-weight: bold;">{p_up}%</p>
    </div>
    """, unsafe_allow_html=True)

# --- Best Recommendation Banner ---
if total >= 3:
    highest_prob = max(p_down, p_up, p_seven)
    if highest_prob == p_down:
        rec_text = "BET: [ 7 DOWN ]"; rec_color = "#3B82F6"
    elif highest_prob == p_up:
        rec_text = "BET: [ 7 UP ]"; rec_color = "#10B981"
    else:
        rec_text = "BET: [ EXACT 7 ]"; rec_color = "#EF4444"
        
    st.markdown(f"""
    <div style="margin-top: 8px; padding: 6px; background-color: #262626; border-radius: 5px; text-align: center; border-left: 5px solid {rec_color};">
        <p style="font-size: 14px; margin: 0; color: #FFFFFF; font-weight: bold;">🎯 {rec_text}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"<p style='color: gray; font-size:12px; margin-top:5px;'>⚠️ Enter {3-total} more rounds...</p>", unsafe_allow_html=True)

# --- Compact History Log ---
if total > 0:
    st.markdown(f"<p style='margin: 8px 0 0 0; font-size:12px;'><b>History:</b> {' ➡️ '.join(history[-6:])}</p>", unsafe_allow_html=True)
    
