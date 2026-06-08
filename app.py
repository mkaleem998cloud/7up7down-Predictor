import streamlit as st
import google.generativeai as genai
import json

# Page Configuration - Strictly Centered
st.set_page_config(page_title="AI Predictor Pro", page_icon="🤖", layout="centered")

# --- Overhauled Mobile UI Framework (No-Scroll & Flex-Row) ---
st.markdown("""
    <style>
    /* Pure Web Page Scrolling Block */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        max-height: 100vh !important;
    }
    .main .block-container {
        padding: 0.4rem 0.6rem !important;
    }
    div[data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    
    /* Headers Adjustment */
    h1 { font-size: 18px !important; margin: 0px !important; padding: 0px !important; text-align: center; color: #fff; }
    h3 { font-size: 13px !important; margin: 4px 0px 2px 0px !important; padding: 0px !important; color: #aaa; }
    
    /* Force 3 Elements to Stay in a Horizontal Row Always */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        gap: 5px !important;
    }
    div[data-testid="column"] {
        flex: 1 !important;
        width: 33.33% !important;
        min-width: 0px !important;
    }
    
    /* Button Customizer (Full Width & Grid Adaptive) */
    .stButton>button {
        width: 100% !important;
        border-radius: 6px !important;
        font-weight: bold !important;
        height: 36px !important;
        font-size: 12px !important;
        padding: 0px !important;
        margin: 0px !important;
    }
    
    /* Accuracy Badge Custom Styling */
    div[data-testid="column"] .stButton>button[key^="acc_"] {
        background-color: #151515 !important;
        color: #00f2fe !important;
        border: 1px solid #00f2fe !important;
        pointer-events: none !important; /* Visual Badge Format */
    }
    
    /* Compact Result Dashboard Card */
    .result-box {
        background-color: #121212;
        padding: 6px 10px;
        border-radius: 6px;
        border-left: 4px solid #00f2fe;
        margin-top: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# --- AI API Configuration ---
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 

if API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
else:
    st.warning("⚠️ Enter Gemini API Key.")

# --- Persisting Session States Safely ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'ai_prediction' not in st.session_state:
    st.session_state.ai_prediction = {
        "prediction": "7Up", "probability": "50%", 
        "up_prob": "33%", "down_prob": "33%", "tie_prob": "34%",
        "analysis": "Enter history rounds."
    }

def get_ai_prediction(history_list):
    if not history_list: return
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Analyze 7Up 7Down history sequence: {history_list}.
        Output STRICT JSON format:
        {{
            "prediction": "7Up or 7Down or Tie",
            "probability": "highest percentage e.g. 70%",
            "up_prob": "percentage e.g. 70%",
            "down_prob": "percentage e.g. 20%",
            "tie_prob": "percentage e.g. 10%",
            "analysis": "1-line text pattern in roman urdu."
        }}
        """
        response = model.generate_content(prompt)
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        st.session_state.ai_prediction = json.loads(clean_text)
    except:
        pass # Keep existing state if connection lags

# --- Core Graphical UI ---
st.title("🤖 AI Predictor Pro")

# Row 1: Action Data Inputs
st.markdown("<h3>📊 Tap Last Result</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔼 7Up", key="btn_up"):
        st.session_state.history.append("7Up")
        st.toast("🟢 Data Added 7Up Successfully!", icon="✅")
        get_ai_prediction(st.session_state.history)
with col2:
    if st.button("🎲 7Exit", key="btn_tie"):
        st.session_state.history.append("Tie")
        st.toast("🟡 Data Added 7Exit Successfully!", icon="✅")
        get_ai_prediction(st.session_state.history)
with col3:
    if st.button("🔽 7Down", key="btn_down"):
        st.session_state.history.append("7Down")
        st.toast("🔴 Data Added 7Down Successfully!", icon="✅")
        get_ai_prediction(st.session_state.history)

# Row 2: Possible Probability Status Matrix
st.markdown("<h3>📈 Possible Accuracy</h3>", unsafe_allow_html=True)
acc_col1, acc_col2, acc_col3 = st.columns(3)
with acc_col1:
    st.button(f"Up: {st.session_state.ai_prediction['up_prob']}", key="acc_up")
with acc_col2:
    st.button(f"Exit: {st.session_state.ai_prediction['tie_prob']}", key="acc_tie")
with acc_col3:
    st.button(f"Down: {st.session_state.ai_prediction['down_prob']}", key="acc_down")

# Row 3: Final Output Display System
st.markdown("<h3>🎯 Final AI Target</h3>", unsafe_allow_html=True)
pred = st.session_state.ai_prediction["prediction"]
prob = st.session_state.ai_prediction["probability"]
analysis = st.session_state.ai_prediction["analysis"]

if "7Up" in pred: color = "#4CAF50"
elif "7Down" in pred: color = "#FF5252"
else: color = "#FFC107"

st.markdown(f"""
<div class="result-box" style="border-left-color: {color};">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="color:{color}; font-size:16px; font-weight:bold;">👉 {pred}</span>
        <span style="background-color:{color}; color:white; padding:1px 6px; border-radius:4px; font-size:12px; font-weight:bold;">{prob} Match</span>
    </div>
    <p style="margin:2px 0 0 0; font-size:11px; color:#cccccc;"><b>Pattern:</b> {analysis}</p>
</div>
""", unsafe_allow_html=True)

# Ultra-Compact Clean Reset Trigger
if st.session_state.history:
    st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)
    if st.button("🧹 Clear History", key="reset"):
        st.session_state.history = []
        st.session_state.ai_prediction = {
            "prediction": "7Up", "probability": "50%", 
            "up_prob": "33%", "down_prob": "33%", "tie_prob": "34%",
            "analysis": "Enter history rounds."
        }
        st.whitespace = "" # Safe dummy assignment
        st.rerun()
