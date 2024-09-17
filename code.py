from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

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
    page_title="Gemini Chat",
    page_icon="🤖",
    layout="centered",
)

# Custom CSS for ChatGPT-like layout and styling
st.markdown("""
    <style>
        .header {
            font-size: 36px;
            color: #0C6EFD;
            text-align: center;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 70vh;
            max-height: 70vh;
            overflow-y: auto;
            background-color: #F0F2F6;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .message {
            padding: 10px;
            margin: 5px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background-color: #D3E3F0;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #FFFFFF;
            align-self: flex-start;
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
    </style>
""", unsafe_allow_html=True)

# Sidebar content for app introduction
with st.sidebar:
    st.title("Welcome to Gemini Chat")
    st.markdown("""
        **Gemini Chat** is an AI-powered chatbot built using the Gemini Pro model. 
        This chatbot can answer a wide variety of questions and assist with code-related problems.
        
        ### Features:
        - AI text generation with Gemini LLM
        - Chat interface similar to ChatGPT
        - Easy-to-use text input system
        - Session-based chat history
        
        Feel free to start asking your questions on the main chat interface!
    """)
    st.info("Developed by [Your Name].")

# Show a welcome modal on app load
if 'first_visit' not in st.session_state:
    st.session_state['first_visit'] = True

if st.session_state['first_visit']:
    st.session_state['first_visit'] = False
    st.markdown("""
        <script>
        alert('Welcome to Gemini Chat! Ask me anything, and I will do my best to respond.');
        </script>
    """, unsafe_allow_html=True)

# Header for the app
st.markdown('<p class="header">Gemini Chat</p>', unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for role, text in st.session_state['chat_history']:
    message_class = "user-message" if role == "You" else "bot-message"
    st.markdown(f'<div class="message {message_class}">{text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input and submit button (Now outside a form to avoid delays)
user_input = st.text_input("Type your message...", key="input", placeholder="Type here...")

if user_input:
    # Add user input to chat history
    st.session_state['chat_history'].append(("You", user_input))

    # Fetch bot response
    with st.spinner('Getting response...'):
        response = get_gemini_response(user_input)
    
    response_text = ""
    for chunk in response:
        response_text += chunk.text
        st.session_state['chat_history'].append(("Bot", chunk.text))

    # Clear input after sending
    st.session_state.input = ""

# Auto-scroll to the latest message
st.markdown('<script>document.querySelector(".chat-container").scrollTop = document.querySelector(".chat-container").scrollHeight;</script>', unsafe_allow_html=True)
