import streamlit as st
import os
import re
import sys
import subprocess  # NEW: For package installation fallback
from datetime import datetime  # NEW: For deployment timestamp

# ======================
# ENHANCED IMPORT WITH FALLBACK (UPDATED)
# ======================
def install_package(package):
    """NEW: Fallback package installer"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from groq import Groq
    groq_available = True
except ImportError:
    groq_available = False
    st.error("""
    Critical: 'groq' package missing!
    Attempting automatic installation...
    """)
    try:
        install_package("groq==0.3")
        from groq import Groq
        groq_available = True
        st.rerun()  # NEW: Restart app after install
    except Exception as e:
        st.error(f"Installation failed: {str(e)}\n\nManually add to requirements.txt:")
        st.code("groq==0.3")
        st.stop()

# ======================
# GROQ SETUP (UNCHANGED)
# ======================
if not os.environ.get("GROQ_API_KEY") and "GROQ_API_KEY" not in st.secrets:
    st.error("""
    Missing API Key!
    1. Get key from console.groq.com
    2. Add to Streamlit secrets as GROQ_API_KEY
    """)
    st.stop()

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"API Connection Failed: {str(e)}")
    st.stop()

# ======================
# CHAT FUNCTIONS (UPDATED CLEANER)
# ======================
def clean_response(text):
    """Enhanced cleaner with more patterns"""
    if not text:
        return ""
    
    patterns = [
        r'<think>.*?</think>',
        r'Hi! I\'m DeepSeek-R1.*?documentation\.',
        r'As an AI.*?assistance\.',
        r'\[.*?\]'  # Removes any [annotations]
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL)
    return text.strip()

def generate_response(prompt):
    """Added timeout and better error handling"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "Respond concisely without disclaimers or XML tags."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            timeout=10  # NEW: Prevents hanging
        )
        return clean_response(chat_completion.choices[0].message.content)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ======================
# STREAMLIT UI (ENHANCED)
# ======================
st.set_page_config(page_title="Groq Chatbot")  # NEW: Better tab title
st.title("💥 Groq Chatbot")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")  # NEW: Timestamp

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}  # NEW: Welcome message
    ]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Generating response..."):
        response = generate_response(prompt)
    
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})