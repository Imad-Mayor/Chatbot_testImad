import streamlit as st
import os
import re
import sys
from datetime import datetime

# ======================
# 1. PACKAGE VERIFICATION (BULLETPROOF)
# ======================
def ensure_package(package):
    """Guaranteed package installation with multiple fallbacks"""
    try:
        __import__(package.split('==')[0])
    except ImportError:
        import subprocess
        import pip
        
        # Try all installation methods
        for method in [
            lambda: pip.main(['install', package]),
            lambda: subprocess.check_call([sys.executable, '-m', 'pip', 'install', package]),
            lambda: subprocess.check_call(['pip', 'install', package])
        ]:
            try:
                method()
                __import__(package.split('==')[0])
                st.rerun()
                return
            except:
                continue
        
        st.error(f"""
        ❌ Critical: Failed to install '{package}'
        1. Add to requirements.txt:
        ```
        {package}
        ```
        2. Redeploy the app
        """)
        st.stop()

ensure_package("groq==0.3")
from groq import Groq

# ======================
# 2. GROQ SETUP (UNCHANGED)
# ======================
if not os.environ.get("GROQ_API_KEY") and "GROQ_API_KEY" not in st.secrets:
    st.error("""
    🔑 Missing API Key!
    1. Get key from console.groq.com
    2. Add to Streamlit secrets as GROQ_API_KEY
    """)
    st.stop()

try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"🔌 Connection Failed: {str(e)}")
    st.stop()

# ======================
# 3. CHAT FUNCTIONS (ENHANCED)
# ======================
def clean_response(text):
    """More robust response cleaning"""
    patterns = [
        r'<think>.*?</think>',
        r'As an? AI.*?',
        r'\[.*?\]',
        r'\(.*?\)',
        r'Note:.*'
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
# 4. STREAMLIT UI (OPTIMIZED)
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