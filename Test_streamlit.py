import streamlit as st
import os
from datetime import datetime

# ======================
# 1. GROQ INITIALIZATION (CLEANED)
# ======================
try:
    from groq import Groq
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])  # Minimal initialization
except ImportError:
    st.error("Missing 'groq' package. Add to requirements.txt: groq==0.4")
    st.stop()
except Exception as e:
    st.error(f"Connection failed: {str(e)}")
    st.stop()

# ======================
# 2. STREAMLIT CHAT INTERFACE
# ======================
st.title("🚀 Groq-Powered Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("Thinking..."):
        try:
            # Clean API call without proxies
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"Error: {str(e)}"
        
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()  # Refresh to show new messages