import streamlit as st
import os
import re
from groq import Groq  # Official Groq client

# =============================================
# GROQ INITIALIZATION (WITH ERROR HANDLING)
# =============================================
try:
    if "GROQ_API_KEY" not in st.secrets:
        st.error("Missing Groq API key! Add GROQ_API_KEY to secrets.")
        st.stop()
    
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

# =============================================
# RESPONSE CLEANER (FIXES <think> TAGS)
# =============================================
def clean_response(response):
    """Remove unwanted tags and signatures"""
    if not response:
        return ""
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    response = re.sub(r'Hi! I\'m DeepSeek-R1.*?documentation\.', '', response)
    return response.strip()

# =============================================
# GROQ RESPONSE GENERATOR
# =============================================
def groq_generate_response(prompt):
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Respond concisely without XML tags."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=1024
        )
        return clean_response(response.choices[0].message.content)
    except Exception as e:
        return f"Error: {str(e)}"

# =============================================
# STREAMLIT UI (UNCHANGED)
# =============================================
st.title("🤖 Groq-Powered Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Thinking..."):
        response = groq_generate_response(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})