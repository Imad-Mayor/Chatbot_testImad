import streamlit as st
import os
import sys
import subprocess

# ======================
# PACKAGE INSTALLATION CHECK
# ======================
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import groq
except ImportError:
    st.warning("Installing missing 'groq' package...")
    install_package("groq==0.3")
    import groq

# ======================
# GROQ INITIALIZATION
# ======================
if "GROQ_API_KEY" not in st.secrets:
    st.error("""
    Missing Groq API Key!
    1. Get key from https://console.groq.com/keys
    2. Add to Streamlit secrets as GROQ_API_KEY
    """)
    st.stop()

try:
    client = groq.Client(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

# ======================
# CHAT FUNCTIONS
# ======================
def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ======================
# STREAMLIT UI
# ======================
st.title("💥 Guaranteed Working Groq Chatbot")

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
        response = generate_response(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})