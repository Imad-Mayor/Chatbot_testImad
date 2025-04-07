import streamlit as st # For building the web app
import random # For random response selection
from datetime import datetime  # Added for time functionality

def generate_response(user_input):
    """Generate more sophisticated responses""" 
    user_input = user_input.lower().strip(" ?!.,") # Force lowercase for case-insensitive matching
    #1- user_input = user_input.lower().strip(" ?!.,")
    #2- This line forces all input to lowercase immediately when received.
    #3- Example: If the user types "JOKE", it becomes "joke".
    #4- This means all checks afterward are case-insensitive by default because the input is already lowercase.
    #5 Your code already handles case insensitivity because of .lower().
    #5s No need to worry about "Joke", "JOKE", etc.—they all become "joke".
    #6 If you removed .lower(), the bot would only respond to exact lowercase "joke" and ignore "Joke" or "JOKE".

 # Expanded response patterns
    greeting_responses = [
        "Hello there! How can I assist you today?",
        "Hi! What brings you here?",
        "Hey! Ready to chat? 😊"
    ]

    feeling_responses = [
        "I'm just a program, but I'm operating perfectly! How about you?",
        "Leave me alone Imad!"
    ]
    

    randomChatter_responses = [
        "Nothing much just hanging around",
        "What are you up to?",
    ]

    thanks_responses = [
        "You're very welcome!",
        "Happy to help! 😊",
        "My pleasure! What else can I do for you?"
    ]

    joke_responses = [
"because haleeb bil loze",
" hiky jowy ani",
    ]
    
    farewell_responses = [
        "Goodbye! Come back anytime!",
        "See you later! 👋",
        "Until next time!"
    ]
    
    help_responses = [
        "I can chat about general topics. Try asking me anything!",
        "I'm a basic chatbot. You can ask me about: greetings, feelings, or just chat!",
        "Need help? I can respond to greetings, farewells, and general questions."
    ]
    # Check user input against keywords/phrases
    # Expanded decision logic
    if any(word in user_input for word in ["hi", "hello", "hey", "greetings"]):
        return random.choice(greeting_responses)
    
    elif any(phrase in user_input for phrase in ["how are you", "how's it going", "how do you feel"]):
        return random.choice(feeling_responses)
    

    elif "thank" in user_input:
        return random.choice(thanks_responses) #see difference in line 71 & 72
    elif any(word in user_input for word in ["bye", "goodbye", "see you", "later"]):
        return random.choice(farewell_responses)
    elif any(phrase in user_input for phrase in ["help", "what can you do", "support"]):
        return random.choice(help_responses)
    elif any(word in user_input for word in ["what's up", "Talk to me", "how are ya"]): # <-- Your randomChatter trigger
        return random.choice(randomChatter_responses)
    elif any(word in user_input for word in ["name", "who are you", "identify"]):
        return "I'm StreamBot, your friendly Streamlit chatbot!" # you can also do this method if you wanted a fixed response
    elif any(word in user_input for word in ["time", "date", "day"]):
        now = datetime.now()
    elif any(word in user_input for word in ["time", "date", "day"]):
        now = datetime.now()  # <-- Critical: Call datetime.now() INSIDE the function
        return f"I checked my clock ⏰ - it's currently {now.strftime('%H:%M on %A, %B %d')}"
    ##########
    #see difference in line 57 & 58
    elif "joke" in user_input: # if user typed joke, the return is the following
        return random.choice(joke_responses)
    
    else: 
         # Default engagement if no keywords match
        engagement_questions = [
            "That's interesting! Can you tell me more?",
            "I'm still learning. Could you rephrase that?",
            "Hmm, I'm not sure I understand. Maybe ask me something else?",
            "Interesting point! What else would you like to discuss?"
        ]
        return random.choice(engagement_questions)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
# The input bar appears at the bottom with placeholder text "What's up?"
if prompt := st.chat_input("Type what's on your mind here?"): # <-- THIS IS THE INPUT BAR


# Display the user's message
    with st.chat_message("user"):
        st.markdown(prompt)
         # Save to message history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Generate and display bot response
    with st.chat_message("assistant"):
        response = generate_response(prompt) # Calls your response function
        st.markdown(response)
        # Save bot response to history
    st.session_state.messages.append({"role": "assistant", "content": response})

#Add Memory (Context Awareness)
#Make the bot remember previous messages:
