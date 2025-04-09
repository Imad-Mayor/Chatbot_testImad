import streamlit as st
import os
import re

# ======================
# ENHANCED IMPORT HANDLING
# ======================
try:
    from groq import Groq
except ImportError:
    st.error("Missing required 'groq' package. Please add it to requirements.txt!")
    st.stop()

# ======================
# GROQ CLIENT INITIALIZATION
# ======================
if "GROQ_API_KEY" not in st.secrets:
    st.error("""
    Missing Groq API Key!
    1. Get key from https://console.groq.com/keys
    2. Add to Streamlit secrets as GROQ_API_KEY
    """)
    st.stop()

try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Failed to initialize Groq: {str(e)}")
    st.stop()

# ======================
# RESPONSE PROCESSING
# ======================
def clean_response(text):
    """Remove unwanted tags/signatures"""
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'Hi! I\'m DeepSeek-R1.*?documentation\.', '', text)
    return text.strip()

def generate_response(prompt):
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond directly without XML tags or signatures."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=1024
        )
        return clean_response(completion.choices[0].message.content)
    except Exception as e:
        return f"Error: {str(e)}"

# ======================
# STREAMLIT UI
# ======================
st.title("🚀 Groq-Powered Chatbot")
st.caption("Now with proper error handling and deployment setup")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.spinner("Generating response..."):
        response = generate_response(prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})