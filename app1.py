import streamlit as st
import os
import time
from dotenv import load_dotenv
from google import genai

# ======================
# LOAD ENV
# ======================
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# ======================
# GEMINI CLIENT
# ======================
client = genai.Client(api_key=api_key)

# ======================
# MODELS FALLBACK
# ======================
MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-lite-latest"
]

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="DevwithAK",
    page_icon="🤖",
    layout="wide"
)

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>
/* App background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

/* Header */
.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.2rem;
    letter-spacing: 1px;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

/* Glass card */
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    margin-bottom: 20px;
}

/* Chat bubbles */
.user-bubble {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    font-size: 15px;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
}

.bot-bubble {
    background: rgba(255,255,255,0.10);
    color: #f8fafc;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    font-size: 15px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.20);
}

/* Labels */
.role-label {
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 4px;
    margin-left: 4px;
    font-weight: 600;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #111827);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Button */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    font-weight: 600;
    padding: 0.7rem 1rem;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
}

/* Chat input styling */
div[data-testid="stChatInput"] {
    border-radius: 14px;
}

/* Hide Streamlit default menu/footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ======================
# SESSION STATE
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []


# ======================
# HEADER
# ======================
st.markdown('<div class="main-title">🤖 DevwithAK</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your Premium AI Chat Experience</div>', unsafe_allow_html=True)

# ======================
# API KEY CHECK
# ======================
if not api_key:
    st.error("GEMINI_API_KEY not found. Please add it in your .env file.")
    st.stop()

# ======================
# AI FUNCTION
# ======================
def get_ai_response(user_text):
    for model_name in MODELS:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_text
                )
                if hasattr(response, "text") and response.text:
                    return response.text
                return "⚠️ Empty response received from AI."

            except Exception as e:
                error_text = str(e)
                if "429" in error_text or "503" in error_text:
                    time.sleep(2)
                else:
                    break

    return "⚠️ AI is busy right now. Please try again."

# ======================
# CHAT DISPLAY
# ======================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding: 30px;">
        <h3 style="color:white;">Welcome to DevwithAK ✨</h3>
        <p style="color:#cbd5e1;">Ask anything and enjoy a premium AI chat experience.</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown('<div class="role-label">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="role-label">DevwithAK AI</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ======================
# USER INPUT
# ======================
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("DevwithAK is typing..."):
        reply = get_ai_response(user_input)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()