from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure the API key for Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
def get_gemini_response(question):
    try:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat(history=[])
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Initialize the Streamlit app
st.set_page_config(page_title="Meet Andrew")

# Side panel with chatbot name and description
with st.sidebar:
    st.title("Andrew The Bot")
    st.markdown("""
    # Meet Andrew: Your Friendly Chatbot

    **Andrew** is your intelligent chatbot powered by the **Gemini API**! Designed to engage in meaningful conversations, Andrew provides insightful answers and assists you with a wide range of topics.

    ## Features

    - **Interactive Conversations**: Andrew engages in dynamic dialogues, making each interaction feel personal and tailored to you.
    - **Knowledgeable Responses**: Leverage the power of the Gemini API for accurate information across various subjects, from science and history to entertainment and lifestyle.
    - **24/7 Availability**: Andrew is always online, ready to assist you anytime, anywhere.
    - **User-Friendly Interface**: Enjoy a seamless chatting experience with an intuitive interface that makes it easy to ask questions and get answers.

    Discover the joy of chatting with Andrew, your go-to chatbot for information, advice, and friendly conversation!
    """)

# Custom CSS styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #333;
        color: #fff;
    }
    .stTextArea > div > textarea {
        border-radius: 20px;
        border: 1px solid #ccc;
    }
    .stButton > button {
        border-radius: 20px;
        background-color: #007bff;
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

st.title("Chat with Andrew")

# Use only one input area
input_text = st.text_area("Curious about something? Ask away!", key="input", height=100)

submit = st.button("Get Response")

if submit and input_text:
    response = get_gemini_response(input_text)
    st.session_state['chat_history'].append(("You", input_text))

    st.subheader("Andrew's Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Andrew", chunk.text))

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
