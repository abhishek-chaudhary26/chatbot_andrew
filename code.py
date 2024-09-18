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
st.set_page_config(page_title="Andrew The Bot")

# Side panel with chatbot name and description
with st.sidebar:
    st.image("https://your-image-url-here.com/logo.png", width=100)  # Optional: Add a logo
    st.title("Andrew The Bot")
    st.write("Hello! I'm Andrew, your virtual assistant. Ask me anything!")

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
    .stTextInput > div > input {
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

input_text = st.text_input("Your message:", key="input")
submit = st.button("Send")

if submit and input_text:
    response = get_gemini_response(input_text)
    # Add user query to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    
    st.subheader("Andrew's Response")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Andrew", chunk.text))

st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

