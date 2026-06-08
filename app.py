import streamlit as st
import google.generativeai as genai
import json

# Page Setup - Strict Title
st.set_page_config(page_title="AI Predictor Pro", page_icon="🤖", layout="centered")

# --- Professional UI Engine (Anti-Scroll & Premium Android Theme) ---
st.markdown("""
    <style>
    /* Absolute No-Scroll for Both Height and Width */
    html, body, [data-testid="stAppViewContainer"], .main {
        overflow: hidden !important;
        max-height: 100vh !important;
        max-width: 100vw !important;
        background-color: #0b0c10 !important;
    }
    .block-container {
        padding: 0.5rem 0.6rem !important;
    }
    
    /* Hide Streamlit Default Elements for Clean Look */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Dashboard Layout */
    .app-title {
        font-size: 19px;
        font-weight: 800;
        text-align: center;
        color: #66fcf1;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .section-title {
        font-size: 12px;
        color: #888888;
        font-weight: bold;
        margin: 6px 0px 4px 0px;
        text-transform: uppercase;
    }

    /* Grid layout that forces 3 items to fit exactly 100% width without breaking */
    .button-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 6px;
        width: 100%;
        box-sizing: border-box;
    }

    /* Custom Native Buttons */
    .stButton>button {
        width: 100% !important;
        height: 40px !important;
        border-radius: 8px !important;
        font-size: 12px !important;
        font-weight: bold !important;
        padding: 0px !important;
        margin: 0px !important;
        border: none !important;
        transition: all 0.2s ease;
    }

    /* Individual Color Styling for Input Buttons */
    div[data-testid="column"]:nth-of-type(1) .stButton>button {
        background: linear-gradient(135deg, #2e7d32, #4caf50) !important;
        color: white !important;
    }
    div[data-testid="column"]:nth-of-type(2) .stButton>button {
        background: linear-gradient(135deg, #ff8f00, #ffc107) !important;
        color: black !important;
    }
    div[data-testid="column"]:nth-of-type(3) .stButton>button {
        background: linear-gradient(135deg, #c62828, #f44336) !important;
        color: white !important;
    }

    /* Premium Styling for Accuracy Badges */
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) .stButton>button {
        background: #1f2833 !important;
        color: #66fcf1 !important;
        border: 1px solid #45f3ff !important;
        pointer-events: none !important; /* Visual display only */
    }

    /* Premium Final AI Target Card */
    .premium-box {
        background: linear-gradient(145deg, #1f2833, #151a21);
        padding: 10px 14px;
        border-radius: 10px;
        border-top: 3px solid #66fcf1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-top: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- AI API Configuration ---
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 

if API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
else:
    st.warning("⚠️ Configuration Required.")

# --- Session States Sync ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'ai_prediction' not in st.session_state:
    st.session_state.ai_prediction = {
        "prediction": "7Up", "probability": "50%", 
        "up_prob": "33%", "down_prob": "33%", "tie_prob": "34%",
        "analysis": "Data analysis system ready."
    }

def get_ai_prediction(history_list):
    if not history_list: return
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Analyze 7Up 7Down dice history sequence: {history_list}.
        Output STRICT JSON format:
        {{
            "prediction": "7Up or 7Down or Tie",
            "probability": "highest percentage e.g. 74%",
            "up_prob": "percentage e.g. 74%",
            "down_prob": "percentage e.g. 20%",
            "tie_prob": "percentage e.g. 6%",
            "analysis": "Short 1-line roman urdu logic pattern."
        }}
        """
        response = model.generate_content(prompt)
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        st.session_state.ai_prediction = json.loads(clean_text)
    except:
        pass

# --- Rendering the Main App Core ---
st.markdown('<div class="app-title">🤖 AI Predictor Pro</div>', unsafe_allow_html=True)

# Section 1: Tap Input Panel
st.markdown('<div class="section-title">📊 Tap Last Result</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔼 7Up", key="btn_up"):
        st.session_state.history.append("7Up")
        st.toast("🟢 Data Added 7Up Successfully!", icon="✅")
        get_ai_prediction(st.session_state.history)
with col2:
    if st.button("🎲 7Exit", key="btn_tie"):
        st.session_state.history.append("Tie")
        st.toast("裁 Data Added 7Exit Successfully!", icon="✅")
        get_ai_prediction(st.session_state.history)
with col3:
    if st.button("🔽 7Down", key="btn_down"):
        st.session_state.history.append("7Down")
        st.toast("🔴 Data Added 7Down Successfully!", icon="✅")
        get_ai_prediction(st.session_state.history)

# Section 2: Fixed Accuracy Matrix Panel
st.markdown('<div class="section-title">📈 Possible Accuracy</div>', unsafe_allow_html=True)
acc_col1, acc_col2, acc_col3 = st.columns(3)
with acc_col1:
    st.button(f"Up: {st.session_state.ai_prediction['up_prob']}", key="acc_up")
with acc_col2:
    st.button(f"Exit: {st.session_state.ai_prediction['tie_prob']}", key="acc_tie")
with acc_col3:
    st.button(f"Down: {st.session_state.ai_prediction['down_prob']}", key="acc_down")

# Section 3: Professional Target Panel
st.markdown('<div class="section-title">🎯 Final AI Target</div>', unsafe_allow_html=True)
pred = st.session_state.ai_prediction["prediction"]
prob = st.session_state.ai_prediction["probability"]
analysis = st.session_state.ai_prediction["analysis"]

if "7Up" in pred: color = "#4CAF50"
elif "7Down" in pred: color = "#FF5252"
else: color = "#FFC107"

st.markdown(f"""
<div class="premium-box" style="border-top-color: {color};">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="color:{color}; font-size:15px; font-weight:bold; letter-spacing:0.5px;">🎯 TARGET: {pred}</span>
        <span style="background-color:{color}; color:{"white" if color!="#FFC107" else "black"}; padding:2px 8px; border-radius:6px; font-size:11px; font-weight:bold; box-shadow: 0 2px 5px rgba(0,0,0,0.3);">{prob} ACCURATE</span>
    </div>
    <div style="margin-top: 6px; font-size: 11px; color: #a9b7c6; line-height: 1.3;">
        <b>AI Pattern:</b> {analysis}
    </div>
</div>
""", unsafe_allow_html=True)

# Clean Reset Utility
if st.session_state.history:
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
    if st.button("🧹 Clear Training Data", key="reset"):
        st.session_state.history = []
        st.session_state.ai_prediction = {
            "prediction": "7Up", "probability": "50%", 
            "up_prob": "33%", "down_prob": "33%", "tie_prob": "34%",
            "analysis": "Data analysis system ready."
        }
        st.rerun()
