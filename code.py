from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
import random
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

# Custom CSS for dark theme and ChatGPT-like layout
st.markdown("""
    <style>
        /* Global settings */
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
            font-family: Arial, sans-serif;
        }
        /* Header */
        .header {
            font-size: 32px;
            color: #FFFFFF;
            text-align: center;
            margin: 20px;
            font-weight: bold;
        }
        /* Message bubbles */
        .message {
            padding: 10px;
            margin: 5px;
            border-radius: 10px;
            max-width: 75%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #4A90E2;
            color: #FFFFFF;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #333333;
            color: #FFFFFF;
            align-self: flex-start;
        }
        /* Input section */
        .input-container {
            display: flex;
            position: fixed;
            bottom: 0;
            width: 90%;
            max-width: 800px;
            background-color: #2D2D2D;
            padding: 10px;
            border-radius: 10px;
            margin: 0 auto;
        }
        .input-box {
            flex: 1;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #444444;
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .send-button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #4A90E2;
            color: #FFFFFF;
            font-weight: bold;
            cursor: pointer;
            margin-left: 10px;
        }
        .send-button:hover {
            background-color: #357ABD;
        }
        /* Animation for loading */
        .loading-animation {
            font-size: 14px;
            color: #4A90E2;
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
    st.title("About Andrew The Bot")
    st.markdown("""
        **Andrew The Bot** is an AI-powered chatbot built using the Gemini Pro model. 
        It can answer various questions and tell you some funny jokes to lighten the mood.

        ### Features:
        - AI text generation with Gemini LLM
        - Real-time response
        - Funny jokes to brighten your day

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
        alert('Welcome to Andrew The Bot! Ask me anything and enjoy some jokes along the way.');
        </script>
    """, unsafe_allow_html=True)

# Header for the app
st.markdown('<p class="header">Andrew The Bot</p>', unsafe_allow_html=True)

# Display chat messages
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Input section
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_area("Type your message...", "", placeholder="Type here...", key="input_box", height=50)
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Add user input to chat
    st.markdown(f'<div class="message user-message">{user_input}</div>', unsafe_allow_html=True)

    # Display thinking animation
    st.markdown('<div class="loading-animation">Andrew is thinking...</div>', unsafe_allow_html=True)

    # Simulate delay
    time.sleep(2)  # 2-second delay before showing the response

    # Get response
    response = get_gemini_response(user_input)

    # Add bot response to chat
    response_text = ""
    for chunk in response:
        response_text += chunk.text

    st.markdown(f'<div class="message bot-message">{response_text} </div>', unsafe_allow_html=True)

# Auto-scroll to the latest message
st.markdown('<script>document.querySelector(".chat-container").scrollTop = document.querySelector(".chat-container").scrollHeight;</script>', unsafe_allow_html=True)
