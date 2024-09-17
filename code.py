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
    page_title="Meet Andrew",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern look
st.markdown("""
    <style>
        .header {
            font-size: 36px;
            color: #0C6EFD;
            text-align: center;
            font-weight: bold;
        }
        .subheader {
            font-size: 24px;
            color: #0C6EFD;
            font-weight: bold;
        }
        .stTextInput input {
            font-size: 18px;
        }
        .stButton button {
            background-color: #0C6EFD;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #084298;
        }
        .stWrite {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Header for the app
st.markdown('<p class="header">Andrew AI chat-bot</p>', unsafe_allow_html=True)

# Sidebar for additional controls
with st.sidebar:
    st.header("Instructions")
    st.write("Ask any question from Andrew and get instant responses.")
    st.write("The chat history will be displayed below the conversation.")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input and submit button
with st.form(key='chat_form'):
    user_input = st.text_input("Ask a question:", key="input", placeholder="Type your question here...")
    submit_button = st.form_submit_button("Ask")

# Handle user input and display response
if submit_button and user_input:
    with st.spinner('Getting response...'):
        response = get_gemini_response(user_input)
    
    st.session_state['chat_history'].append(("You", user_input))
    
    # Display response
    st.subheader("Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
