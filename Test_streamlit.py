import streamlit as st
import os
import re
from datetime import datetime

# ======================
# 1. PACKAGE HANDLING (SIMPLIFIED)
# ======================
try:
    from groq import Groq
except ImportError:
    st.error("""
    ❌ Missing required 'groq' package
    
    SOLUTION:
    1. Create file 'requirements.txt' in your repository root
    2. Add this line:
    ```
    groq==0.4
    ```
    3. Redeploy your app
    """)
    st.stop()

# ======================
# 2. GROQ SETUP
# ======================
if "GROQ_API_KEY" not in st.secrets:
    st.error("""
    🔑 Missing API Key!
    1. Get key from console.groq.com
    2. Add to Streamlit secrets as GROQ_API_KEY
    """)
    st.stop()

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"🔌 Connection Failed: {str(e)}")
    st.stop()

# ======================
# 3. CHAT FUNCTIONS
# ======================
def clean_response(text):
    """Remove unwanted tags/signatures"""
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
            timeout=10
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
