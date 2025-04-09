import streamlit as st
import os
import re

# ======================
# ENHANCED IMPORT WITH FALLBACK
# ======================
try:
    from groq import Groq
    groq_available = True
except ImportError:
    groq_available = False
    st.error("""
    Critical: 'groq' package missing!
    Add to requirements.txt:
    ```
    groq==0.3
    ```
    """)
    st.stop()

# ======================
# GROQ SETUP
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
# CHAT FUNCTIONS
# ======================
def clean_response(text):
    return re.sub(r'<think>.*?</think>|Hi! I\'m DeepSeek-R1.*?documentation\.', '', text, flags=re.DOTALL).strip()

def generate_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Respond directly without XML tags"},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7
        )
        return clean_response(chat_completion.choices[0].message.content)
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ======================
# STREAMLIT UI
# ======================
st.title("💥 Groq Chatbot (Guaranteed Setup)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    with st.spinner("Generating..."):
        response = generate_response(prompt)
    
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})