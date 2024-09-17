from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app configuration
st.set_page_config(
    page_title="Andrew The Bot",
    page_icon="🤖",
    layout="centered",
)

# Custom CSS for dark theme and ChatGPT-like layout, styling, and animations
st.markdown("""
    <style>
        /* Remove extra spacing */
        .css-18e3th9 {
            padding-top: 0px;
            padding-bottom: 0px;
            padding-left: 0px;
            padding-right: 0px;
        }
        /* Dark theme settings */
        body {
            background-color: #1E1E1E;
        }
        .header {
            font-size: 36px;
            color: #FFFFFF;
            text-align: center;
            font-weight: bold;
            margin-top: 10px;
            margin-bottom: 10px;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 70vh;
            max-height: 70vh;
            overflow-y: auto;
            background-color: #333333;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            color: white;
        }
        .message {
            padding: 10px;
            margin: 5px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background-color: #4A4A4A;
            align-self: flex-end;
            color: white;
        }
        .bot-message {
            background-color: #2D2D2D;
            align-self: flex-start;
            color: white;
        }
        .input-container {
            display: flex;
            margin-top: 10px;
        }
        .input-box {
            flex: 1;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            margin-right: 10px;
            background-color: #1E1E1E;
            color: white;
        }
        .send-button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #0C6EFD;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        .send-button:hover {
            background-color: #084298;
        }
        /* Animation for loading */
        .loading-animation {
            font-size: 14px;
            color: #0C6EFD;
            text-align: center;
            margin-top: 20px;
            animation: loading 1s infinite;
        }
        @keyframes loading {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar content for app introduction
with st.sidebar:
    st.title("Welcome to Andrew The Bot")
    st.markdown("""
        **Andrew The Bot** is an AI-powered chatbot built using the Gemini Pro model. 
        This chatbot can answer a wide variety of questions and assist with code-related problems.
        
        ### Features:
        - AI text generation with Gemini LLM
        - Chat interface similar to ChatGPT
        - Easy-to-use text input system
        - Session-based chat history
        
        Developed by **ABHISHEK**.
    """)
    st.info("Developed by ABHISHEK.")

# Show a welcome modal on app load
if 'first_visit' not in st.session_state:
    st.session_state['first_visit'] = True

if st.session_state['first_visit']:
    st.session_state['first_visit'] = False
    st.markdown("""
        <script>
        alert('Welcome to Andrew The Bot! Ask me anything, and I will do my best to respond.');
        </script>
    """, unsafe_allow_html=True)

# Header for the app with white color for Andrew The Bot's name
st.markdown('<p class="header">Andrew The Bot</p>', unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history with dark theme
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, text in st.session_state['chat_history']:
    message_class = "user-message" if role == "You" else "bot-message"
    st.markdown(f'<div class="message {message_class}">{text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Reset the input after receiving the response
if 'input' not in st.session_state:
    st.session_state['input'] = ""

# Input and submit button (Now using a local variable to reset input)
user_input = st.text_input("Type your message...", value="", placeholder="Type here...", label_visibility='collapsed')

# If user submits input
if st.button("Send"):
    if user_input:
        # Add user input to chat history
        st.session_state['chat_history'].append(("You", user_input))

        # Display loading animation while getting response
        with st.spinner('Getting response...'):
            st.markdown('<div class="loading-animation">Andrew is thinking...</div>', unsafe_allow_html=True)
            time.sleep(1)  # Simulate a slight delay for effect
            response = get_gemini_response(user_input)

        # Add bot response to the chat history
        response_text = ""
        for chunk in response:
            response_text += chunk.text
            st.session_state['chat_history'].append(("Bot", chunk.text))

# Auto-scroll to the latest message
st.markdown('<script>document.querySelector(".chat-container").scrollTop = document.querySelector(".chat-container").scrollHeight;</script>', unsafe_allow_html=True)
