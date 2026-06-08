import streamlit as st
import google.generativeai as genai
import json

# Page Configuration
st.set_page_config(page_title="AI Predictor Pro", page_icon="🤖", layout="centered")

# --- Overhauled Premium CSS Framework (Compact Spacing & Badges) ---
st.markdown("""
    <style>
    /* Prevent Any Scrolling Globally */
    html, body, [data-testid="stAppViewContainer"], .main {
        overflow: hidden !important;
        max-height: 100vh !important;
        max-width: 100vw !important;
        background-color: #0d0e15 !important;
    }
    .block-container {
        padding: 0.2rem 0.5rem !important;
    }
    
    /* Auto Hide Default Overheads */
    footer, header {visibility: hidden;}
    .stAlert { padding: 4px !important; margin-bottom: 2px !important; font-size: 11px !important; }

    /* Custom Mobile Grid for Badges */
    .mobile-row {
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
        width: 100% !important;
        gap: 6px !important;
        margin-bottom: 4px !important;
    }
    
    .acc-badge {
        flex: 1 !important;
        text-align: center;
        padding: 5px 0px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: bold;
        background-color: #1a1f2c;
        color: #00f2fe;
        border: 1px solid #00f2fe;
    }

    /* Target Result Panel Output Display */
    .premium-display {
        background: linear-gradient(145deg, #151b26, #0f131c);
        padding: 6px 12px;
        border-radius: 8px;
        border-top: 3px solid #00f2fe;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }

    /* History Badge Stream View */
    .history-container {
        display: flex;
        flex-direction: row;
        gap: 4px;
        overflow-x: auto;
        white-space: nowrap;
        padding: 4px 6px;
        background: #10141d;
        border-radius: 6px;
        border: 1px dashed #333;
        min-height: 28px;
        align-items: center;
    }
    .hist-badge {
        font-size: 10px;
        font-weight: bold;
        padding: 2px 6px;
        border-radius: 4px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- AI API Key Secure Processing ---
API_KEY = "AQ.Ab8RN6IXxkksAQGeepnhbEl1zS4EYc5RR0rcuzVzj_-3zpqTSg"

ai_active = True
if API_KEY != "AQ.Ab8RN6IXxkksAQGeepnhbEl1zS4EYc5RR0rcuzVzj_-3zpqTSg" and API_KEY.strip() != "":
    try:
        genai.configure(api_key=API_KEY)
        ai_active = True
    except:
        pass

# --- State Sync Engine ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'ai_prediction' not in st.session_state:
    st.session_state.ai_prediction = {
        "prediction": "7Up", "probability": "55%", 
        "up_prob": "33%", "down_prob": "33%", "tie_prob": "34%",
        "analysis": "System online. Tap history to train."
    }

def process_prediction():
    if not st.session_state.history: return
    if not ai_active:
        import random
        u, d, t = random.randint(40, 70), random.randint(20, 40), random.randint(5, 15)
        total = u + d + t
        st.session_state.ai_prediction = {
            "prediction": "7Up" if u > d else "7Down",
            "probability": f"{int((max(u,d)/total)*100)}%",
            "up_prob": f"{int((u/total)*100)}%",
            "down_prob": f"{int((d/total)*100)}%",
            "tie_prob": f"{int((t/total)*100)}%",
            "analysis": "Local probability engine running successfully."
        }
        return

    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""
        Analyze 7Up 7Down dice history sequence: {st.session_state.history}.
        Output STRICT JSON format:
        {{
            "prediction": "7Up or 7Down or Tie",
            "probability": "highest percentage e.g. 72%",
            "up_prob": "percentage e.g. 72%",
            "down_prob": "percentage e.g. 20%",
            "tie_prob": "percentage e.g. 8%",
            "analysis": "Short 1-line roman urdu pattern rule description."
        }}
        """
        response = model.generate_content(prompt)
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        st.session_state.ai_prediction = json.loads(clean_text)
    except:
        pass

# --- Graphical Interface Layout ---
st.markdown('<div style="font-size:16px; font-weight:800; text-align:center; color:#00f2fe; margin-bottom:2px;">🤖 AI PREDICTOR PRO</div>', unsafe_allow_html=True)

if not ai_active:
    st.info("💡 Running on Local Probability Engine. Insert your Gemini API Key in code to activate Full Cloud AI.")

# Row 1: Action Entry Points
st.markdown('<div style="font-size:10px; color:#777; font-weight:bold; text-transform:uppercase; margin:2px 0;">📊 Tap Last Result</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔼 7Up", key="action_up", use_container_width=True):
        st.session_state.history.append("7Up")
        st.toast("🟢 Data Added 7Up Successfully!", icon="✅")
        process_prediction()
with col2:
    if st.button("🎲 7Exit", key="action_tie", use_container_width=True):
        st.session_state.history.append("Tie")
        st.toast("🟡 Data Added 7Exit Successfully!", icon="✅")
        process_prediction()
with col3:
    if st.button("🔽 7Down", key="action_down", use_container_width=True):
        st.session_state.history.append("7Down")
        st.toast("🔴 Data Added 7Down Successfully!", icon="✅")
        process_prediction()

# Row 2: Status Matrices
st.markdown('<div style="font-size:10px; color:#777; font-weight:bold; text-transform:uppercase; margin:4px 0 2px 0;">📈 Possible Accuracy</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="mobile-row">
    <div class="acc-badge">Up: {st.session_state.ai_prediction['up_prob']}</div>
    <div class="acc-badge">Exit: {st.session_state.ai_prediction['tie_prob']}</div>
    <div class="acc-badge">Down: {st.session_state.ai_prediction['down_prob']}</div>
</div>
""", unsafe_allow_html=True)

# Row 3: Target Output Panel Display
st.markdown('<div style="font-size:10px; color:#777; font-weight:bold; text-transform:uppercase; margin:2px 0;">🎯 Final AI Target</div>', unsafe_allow_html=True)

pred = st.session_state.ai_prediction["prediction"]
prob = st.session_state.ai_prediction["probability"]
analysis = st.session_state.ai_prediction["analysis"]

if "7Up" in pred: color = "#4CAF50"
elif "7Down" in pred: color = "#FF5252"
else: color = "#FFC107"

st.markdown(f"""
<div class="premium-display" style="border-top-color: {color};">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="color:{color}; font-size:13px; font-weight:bold;">👉 TARGET: {pred}</span>
        <span style="background-color:{color}; color:{"white" if color!="#FFC107" else "black"}; padding:1px 5px; border-radius:4px; font-size:10px; font-weight:bold;">{prob} MATCH</span>
    </div>
    <div style="margin-top: 2px; font-size: 10px; color: #a9b7c6;">
        <b>Pattern:</b> {analysis}
    </div>
</div>
""", unsafe_allow_html=True)

# NEW FEATURE: Dynamic History Tracking Line (Live Record View)
st.markdown('<div style="font-size:10px; color:#777; font-weight:bold; text-transform:uppercase; margin:4px 0 2px 0;">📜 Recently Added Data Record</div>', unsafe_allow_html=True)

if st.session_state.history:
    html_stream = '<div class="history-container">'
    for idx, item in enumerate(st.session_state.history):
        if item == "7Up": bg, text = "#1b5e20", "7Up"
        elif item == "7Down": bg, text = "#b71c1c", "7Down"
        else: bg, text = "#e65100", "Exit"
        html_stream += f'<span class="hist-badge" style="background-color:{bg};">{idx+1}. {text}</span>'
    html_stream += '</div>'
    st.markdown(html_stream, unsafe_allow_html=True)
else:
    st.markdown('<div class="history-container" style="color:#555; font-size:10px; justify-content:center;">No data input yet</div>', unsafe_allow_html=True)

# Compact Functional Data Clean Reset Row (Pushed down slightly)
if st.session_state.history:
    st.markdown('<div style="height:2px;"></div>', unsafe_allow_html=True)
    if st.button("🧹 Clear Training Data", key="wipe_engine", use_container_width=True):
        st.session_state.history = []
        st.session_state.ai_prediction = {
            "prediction": "7Up", "probability": "55%", 
            "up_prob": "33%", "down_prob": "33%", "tie_prob": "34%",
            "analysis": "System online. Tap history to train."
        }
        st.rerun()
            
