import streamlit as st
import ollama
import base64
import os

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(page_title="Mental Health Chatbot", layout="wide")

# ----------------------------
# Background image setup
# ----------------------------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

background_path = "background.png"  # Image must exist
if os.path.exists(background_path):
    bin_str = get_base64(background_path)
    st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.warning("⚠️ 'background.png' not found. Please add the image to the project folder.")

# ----------------------------
# Session state initialization
# ----------------------------
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# ----------------------------
# Model selection (lightweight)
# ----------------------------
MODEL_NAME = "tinyllama"

# ----------------------------
# Chat response generation
# ----------------------------
def generate_response(user_input):
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    try:
        response = ollama.chat(model=MODEL_NAME, messages=st.session_state.conversation_history)
        ai_response = response['message']['content']
    except Exception as e:
        ai_response = f"❌ Error: {str(e)}"
    st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
    return ai_response

# ----------------------------
# Cached tools
# ----------------------------
@st.cache_data(show_spinner=False)
def generate_affirmation():
    prompt = "Give a short, encouraging affirmation for someone feeling down."
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"❌ Error: {str(e)}"

@st.cache_data(show_spinner=False)
def generate_meditation_guide():
    prompt = "Give a 5-minute guided meditation script for stress relief."
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ----------------------------
# App Title
# ----------------------------
st.title("🧠 Mental Health Support Agent")

# ----------------------------
# Display conversation history
# ----------------------------
for msg in st.session_state.conversation_history:
    role = "🧍 You" if msg['role'] == "user" else "🤖 AI"
    st.markdown(f"**{role}:** {msg['content']}")

# ----------------------------
# Chat input
# ----------------------------
user_message = st.text_input("💬 How can I help you today?", placeholder="Ask anything about mental wellness...")

if user_message:
    with st.spinner("🧠 Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**🤖 AI:** {ai_response}")

# ----------------------------
# Extra tools
# ----------------------------
st.subheader("✨ Self-Care Tools")

col1, col2 = st.columns(2)

with col1:
    if st.button("💖 Give me a positive affirmation"):
        with st.spinner("Fetching a warm affirmation..."):
            affirmation = generate_affirmation()
            st.markdown(f"**💡 Affirmation:** {affirmation}")

with col2:
    if st.button("🧘‍♀️ Guide me through meditation"):
        with st.spinner("Preparing a calming session..."):
            meditation_guide = generate_meditation_guide()
            st.markdown(f"**🌿 Guided Meditation:** {meditation_guide}")
