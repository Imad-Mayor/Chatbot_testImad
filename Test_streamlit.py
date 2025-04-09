import streamlit as st
from groq import Groq  # Official Groq client (no proxies)
import os

# ======================
# 1. MINIMAL GROQ SETUP
# ======================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ_API_KEY in secrets")
    st.stop()

try:
    # Pure initialization without any proxy parameters
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Connection failed: {str(e)}")
    st.stop()

# ======================
# 2. STREAMLIT CHAT UI
# ======================
st.title("🚀 Groq Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {str(e)}"
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()