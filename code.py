import streamlit as st
import os
from google.generative_ai import chat
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = st.secrets["GOOGLE_API_KEY"]

# Initialize chatbot
chatbot = chat.Chat(api_key)

# Set Page Configuration (title and icon)
st.set_page_config(
    page_title="Generative AI App",
    page_icon="🤖",
    layout="wide",  # Set to 'wide' for a full-screen layout
    initial_sidebar_state="expanded"  # Sidebar starts open
)

# Add a professional-looking header with a title
st.markdown("""
<style>
.header {
    font-size:40px;
    color:#0C6EFD;
    text-align:center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="header">Welcome to the Generative AI Web App</p>', unsafe_allow_html=True)

# Sidebar for settings and navigation
with st.sidebar:
    st.title("Settings")
    st.write("Configure your preferences here.")

# Main app
st.title("Generative AI - Ask Anything!")
st.write("This is an app using Google Generative AI and Streamlit.")

# Function to interact with AI
def ask_ai(question):
    response = chatbot.ask(question)
    return response['answer']

# Text input for user question
user_input = st.text_input("Ask the AI something:")

# Button to submit and display AI response
if st.button("Get Response"):
    if user_input:
        response = ask_ai(user_input)
        st.success(response)
    else:
        st.error("Please enter a question to get a response.")

# Footer
st.markdown("""
<hr style="border:1px solid #eee;" />
<footer>
    <p style="font-size:16px; text-align:center; color:gray;">© 2024 Generative AI App | Powered by Streamlit</p>
</footer>
""", unsafe_allow_html=True)
