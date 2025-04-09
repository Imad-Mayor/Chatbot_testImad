import streamlit as st
import os
import re  # NEW IMPORT FOR CLEANING RESPONSES
from groq import Groq  # type: ignore # Official Groq client

# ===================================================
# GROQ INITIALIZATION (API KEY SETUP)
# ===================================================
if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing Groq API key! Add GROQ_API_KEY to secrets.")
    st.stop()

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===================================================
# FIX FOR <THINK> TAGS AND DEEPSEEK SIGNATURE - SOLUTION APPLIED IN 2 PLACES:
# 1. SYSTEM PROMPT TELLS MODEL NOT TO GENERATE THEM
# 2. CLEANER FUNCTION REMOVES THEM IF THEY STILL APPEAR
# ===================================================
def clean_response(response):
    """REMOVES UNWANTED TAGS AND SIGNATURES"""
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    response = re.sub(r'Hi! I\'m DeepSeek-R1.*?documentation\.', '', response)
    return response.strip()

def groq_generate_response(prompt):
    """GENERATES RESPONSE WITH BUILT-IN PROTECTION AGAINST <THINK> TAGS"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                # SYSTEM PROMPT SOLUTION - TELL MODEL TO AVOID UNWANTED FORMATTING
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond directly without XML tags like <think> or company signatures."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=1024
        )
        raw_response = chat_completion.choices[0].message.content
        # SECONDARY CLEANER SOLUTION - ENSURES NO TAGS REMAIN
        return clean_response(raw_response)
    except Exception as e:
        return f"Error: {str(e)}"

# ===================================================
# STREAMLIT CHAT INTERFACE (ORIGINAL CODE)
# ===================================================
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
        # THIS IS WHERE THE FIXED FUNCTION IS CALLED
        response = groq_generate_response(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})