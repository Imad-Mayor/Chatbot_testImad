import streamlit as st
import os
from datetime import datetime

# ======================
# 1. GROQ INITIALIZATION (FIXED)
# ======================
try:
    from groq import Groq
except ImportError:
    st.error("Missing 'groq' package. Add to requirements.txt: groq==0.4")
    st.stop()

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing GROQ_API_KEY in secrets")
    st.stop()

try:
    # Updated initialization without 'proxies'
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"],
        # timeout=30  # Optional: Add timeout if needed
    )
except Exception as e:
    st.error(f"Connection failed: {str(e)}")
    st.stop()

# ======================
# 2. CHAT FUNCTIONS (SIMPLIFIED)
# ======================
def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ======================
# 3. STREAMLIT UI
# ======================
st.title("🚀 Groq Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        response = generate_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()