import streamlit as st # type: ignore
import groq  
# =============================================
# GROQ-SPECIFIC CODE START (LLM Integration)
# =============================================
# Initialize Groq client - requires GROQ_API_KEY in secrets

if "GROQ_API_KEY" not in st.secrets:
    st.error("Missing Groq API key. Please add GROQ_API_KEY to your secrets!")
    st.stop()

groq_client = groq.Client(api_key=st.secrets["GROQ_API_KEY"])

def groq_generate_response(prompt):
    """Generate response using Groq's fast LLM"""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="allam-2-7b",  # Groq's fastest model
            temperature=0.7,
            max_tokens=1024
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Groq API Error: {str(e)}"
# =============================================
# GROQ-SPECIFIC CODE END
# =============================================

# Simple non-LLM responses (original chatbot code)
def get_simple_response(user_input):
    """Handle basic greetings without calling Groq"""
    greetings = ["hi", "hello", "hey"]
    if any(greet in user_input.lower() for greet in greetings):
        return "Hello! How can I help you today?"
    return None

# Streamlit app UI (original code)
st.title("🤖 Imad AI Chatbot")
st.caption("Simple mode for greetings, Groq LLM for complex questions")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate response
    with st.spinner("Thinking..."):
        # First try simple responses
        response = get_simple_response(prompt)
        
        # If not a simple query, use Groq
        if response is None:
            # =============================================
            # GROQ-SPECIFIC CODE START (LLM Call)
            # =============================================
            response = groq_generate_response(prompt)
            # =============================================
            # GROQ-SPECIFIC CODE END
            # =============================================
    
    # Display response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})