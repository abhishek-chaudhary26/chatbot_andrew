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
    layout="wide",
)

# Custom CSS for a ChatGPT-like look
st.markdown("""
    <style>
        .header {
            font-size: 36px;
            color: #0C6EFD;
            text-align: center;
            font-weight: bold;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 80vh;
            max-height: 80vh;
            overflow-y: auto;
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
            background-color: #F0F2F6;
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

# Input and submit button
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input("Type your message...", key="input", placeholder="Type here...")
    submit_button = st.form_submit_button("Send", use_container_width=True, help="Press Enter to submit")

# Handle user input and display response
if submit_button and user_input:
    with st.spinner('Getting response...'):
        response = get_gemini_response(user_input)
    
    st.session_state['chat_history'].append(("You", user_input))
    
    # Display response
    st.subheader("Response")
    response_text = ""
    for chunk in response:
        response_text += chunk.text
        st.session_state['chat_history'].append(("Bot", chunk.text))
    
    # Update chat history with bot response
    st.markdown('<div class="message bot-message">{}</div>'.format(response_text), unsafe_allow_html=True)
    
    # Auto-scroll to the latest message
    st.markdown('<script>document.querySelector(".chat-container").scrollTop = document.querySelector(".chat-container").scrollHeight;</script>', unsafe_allow_html=True)
