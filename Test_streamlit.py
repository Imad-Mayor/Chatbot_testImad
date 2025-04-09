import streamlit as st
import os
import re
import sys
import subprocess
from datetime import datetime

# ======================
# 1. PACKAGE ENFORCEMENT (BULLETPROOF)
# ======================
def enforce_package(package):
    """Guaranteed package installation with all fallbacks"""
    package_name = package.split('==')[0]
    
    # First try normal import
    try:
        __import__(package_name)
        return True
    except ImportError:
        pass
    
    # Try all installation methods
    installation_methods = [
        [sys.executable, "-m", "pip", "install", package],
        ["pip", "install", package],
        ["pip3", "install", package]
    ]
    
    for method in installation_methods:
        try:
            subprocess.check_call(method)
            __import__(package_name)
            st.success(f"✅ Successfully installed {package}")
            st.rerun()
            return True
        except:
            continue
    
    # If all methods fail
    st.error(f"""
    ❌ CRITICAL: Failed to install '{package}'
    
    REQUIRED ACTION:
    1. Create file 'requirements.txt' in your repository root with:
    ```
    {package}
    ```
    2. Push to GitHub
    3. Delete and redeploy your Streamlit app
    """)
    st.stop()

enforce_package("groq==0.3")
from groq import Groq

# ======================
# 2. GROQ SETUP
# ======================
if "GROQ_API_KEY" not in st.secrets:
    st.error("""
    🔑 MISSING API KEY!
    1. Get key from console.groq.com
    2. Add to Streamlit secrets as GROQ_API_KEY
    """)
    st.stop()

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"🔌 CONNECTION FAILED: {str(e)}")
    st.stop()

# ======================
# 3. CHAT FUNCTIONS
# ======================
def clean_response(text):
    """Remove unwanted tags/formatting"""
    patterns = [
        r'<think>.*?</think>',
        r'As an? AI.*?',
        r'\[.*?\]'
    ]
    for pattern in patterns:
        text = re.sub(pattern, '', text, flags=re.DOTALL)
    return text.strip()

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Respond concisely without disclaimers."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            timeout=15
        )
        return clean_response(response.choices[0].message.content)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ======================
# 4. STREAMLIT UI
# ======================
st.set_page_config(page_title="Groq Chatbot")
st.title("🚀 Groq Chatbot")
st.caption(f"Deployed: {datetime.now().strftime('%m/%d %H:%M')}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Generating..."):
        response = generate_response(prompt)
    
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})