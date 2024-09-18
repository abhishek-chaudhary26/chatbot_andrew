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

# Function to get responses from the Gemini Pro model
def get_gemini_response(question):
    chat = genai.start_chat()
    response = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    return response_text

# List of funny thinking messages
thinking_messages = [
    "Andrew is brewing up some wisdom...",
    "Andrew is putting on his thinking cap...",
    "Andrew is consulting his magic 8-ball...",
    "Andrew is busy plotting world domination (or maybe just your answer)...",
    "Andrew is sharpening his pencils for a great response...",
    "Andrew is decoding your question with the help of his crystal ball...",
    "Andrew is Googling... just kidding, he’s all AI!",
    "Andrew is summoning his inner genius...",
    "Andrew is deep in thought (or maybe just daydreaming)...",
    "Andrew is working hard to not give you a generic response..."
]

def get_random_thinking_message():
    return random.choice(thinking_messages)

# Initialize Streamlit app configuration
st.set_page_config(
    page_title="Meet Andrew",
    page_icon="🤖",
    layout="centered",
)

# Custom CSS for theme
st.markdown("""
    <style>
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
            font-family: Arial, sans-serif;
        }
        .header {
            font-size: 32px;
            color: #007BFF;
            text-align: center;
            margin: 20px;
            font-weight: bold;
        }
        .message {
            padding: 10px;
            margin: 5px;
            border-radius: 10px;
            max-width: 75%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #007BFF;
            color: #FFFFFF;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #4A90E2;
            color: #FFFFFF;
            align-self: flex-start;
        }
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
        .loading-animation {
            font-size: 16px;
            color: #007BFF;
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

# Sidebar content
with st.sidebar:
    st.title("About Andrew")
    st.markdown("""
        **Andrew** is an AI-powered chatbot built using the Gemini Pro model. 
        It can answer various questions and tell you some funny jokes to lighten the mood.
    """)

# Show a welcome modal on app load
if 'first_visit' not in st.session_state:
    st.session_state['first_visit'] = True

if st.session_state['first_visit']:
    st.session_state['first_visit'] = False
    st.markdown("""
        <script>
        alert('Welcome to Andrew! Ask me anything.');
        </script>
    """, unsafe_allow_html=True)

# Header for the app
st.markdown('<p class="header">Andrew</p>', unsafe_allow_html=True)

# Input section
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_area("What's on your mind?", "", placeholder="Type your message here...", key="input_box", height=50)
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    # Add user input to chat
    st.markdown(f'<div class="message user-message">{user_input}</div>', unsafe_allow_html=True)

    # Display thinking animation
    thinking_message = get_random_thinking_message()
    st.markdown(f'<div class="loading-animation">{thinking_message}</div>', unsafe_allow_html=True)

    # Simulate delay
    time.sleep(2)

    # Get response from the bot
    response_text = get_gemini_response(user_input)

    # Add bot response to chat
    st.markdown(f'<div class="message bot-message">{response_text}</div>', unsafe_allow_html=True)

# Auto-scroll to the latest message
st.markdown('<script>document.querySelector(".chat-container").scrollTop = document.querySelector(".chat-container").scrollHeight;</script>', unsafe_allow_html=True)
