import streamlit as st
import google.generativeai as genai
import json

# Page Configuration for Mobile
st.set_page_config(page_title="AI 7Up 7Down Predictor", page_icon="🤖", layout="centered")

# --- CSS for Mobile UI Optimization ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }
    .result-box {
        background-color: #1e1e1e;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00f2fe;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- AI API Setup ---
# Apni Gemini API Key yahan dalein ya Streamlit secrets ka istemal karein
# (Aap Google AI Studio se free API key le sakte hain)
API_KEY = "YOUR_GEMINI_API_KEY_HERE" 

if API_KEY != "YOUR_GEMINI_API_KEY_HERE":
    genai.configure(api_key=API_KEY)
else:
    st.warning("⚠️ Please configure your Gemini API Key in the code.")

# --- Session State Management ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'ai_prediction' not in st.session_state:
    st.session_state.ai_prediction = {"prediction": "Waiting for data...", "probability": "--", "analysis": "Enter past rounds to start AI analysis."}

# --- Functions ---
def get_ai_prediction(history_list):
    """Gemini AI se probability aur analysis mangne ka function"""
    if not history_list:
        return
        
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # AI ko strict instruction dene ke liye prompt
        prompt = f"""
        You are an expert mathematical and probability analyzer for the dice game 7Up 7Down.
        Here is the sequence of the last recent game rounds (ordered from oldest to newest):
        {history_list}
        
        Analyze the streaks, repetition patterns, and standard deviation probabilities. 
        Predict the most likely NEXT outcome (7Up, 7Down, or Tie).
        
        Provide your response strictly in the following JSON format so I can parse it:
        {{
            "prediction": "7Up or 7Down or Tie",
            "probability": "percentage e.g. 68%",
            "analysis": "A brief 2-line explanation in simple Urdu/Hindi language (using english alphabet/roman urdu) explaining the pattern."
        }}
        """
        
        response = model.generate_content(prompt)
        # JSON parse karna
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        data = json.loads(clean_text)
        st.session_state.ai_prediction = data
    except Exception as e:
        st.session_state.ai_prediction = {
            "prediction": "Error",
            "probability": "0%",
            "analysis": f"AI Connection issue or invalid API Key."
        }

# --- App UI Layout ---
st.title("🤖 AI Game Predictor Pro")
st.caption("AI-powered pattern analyzer for 7Up 7Down")

# Step 1: Manual History Input Buttons
st.subheader("📊 Tap Last Result")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔼 7Up", key="btn_up"):
        st.session_state.history.append("7Up")
        if len(st.session_state.history) > 12: st.session_state.history.pop(0) # Keep last 12
        get_ai_prediction(st.session_state.history)

with col2:
    if st.button("🎲 Tie (7)", key="btn_tie"):
        st.session_state.history.append("Tie")
        if len(st.session_state.history) > 12: st.session_state.history.pop(0)
        get_ai_prediction(st.session_state.history)

with col3:
    if st.button("🔽 7Down", key="btn_down"):
        st.session_state.history.append("7Down")
        if len(st.session_state.history) > 12: st.session_state.history.pop(0)
        get_ai_prediction(st.session_state.history)

# Live History Tracker Display
if st.session_state.history:
    st.markdown(f"**Current History Sequence:** `{' -> '.join(st.session_state.history)}`")
    if st.button("🧹 Clear History"):
        st.session_state.history = []
        st.session_state.ai_prediction = {"prediction": "Waiting for data...", "probability": "--", "analysis": "Enter past rounds to start AI analysis."}
        st.rerun()
else:
    st.info("Tap the buttons above as rounds finish in your live game to train the AI.")

st.markdown("---")

# Step 2: AI Live Prediction Dashboard
st.subheader("🎯 Live AI Forecast")

pred = st.session_state.ai_prediction["prediction"]
prob = st.session_state.ai_prediction["probability"]
analysis = st.session_state.ai_prediction["analysis"]

# Color code predictions dynamically
if "7Up" in pred:
    color = "#4CAF50" # Green
elif "7Down" in pred:
    color = "#FF5252" # Red
else:
    color = "#FFC107" # Yellow/Orange

st.markdown(f"""
<div class="result-box" style="border-left-color: {color};">
    <h3 style="margin:0; color:{color};">Next Target: {pred}</h3>
    <h4 style="margin:5px 0 0 0; color:#ffffff;">Probability Accuracy: {prob}</h4>
    <p style="margin:10px 0 0 0; font-size:14px; color:#cccccc;"><b>AI Analysis:</b> {analysis}</p>
</div>
""", unsafe_allow_html=True)
