import os
import uuid
import time
import requests
import json
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AGENT_BASE_URL = os.environ.get("AGENT_BASE_URL")

# Set page configuration
st.set_page_config(
    page_title="AWS Bedrock Agent Frontend",
    page_icon=":scroll:",
    layout="centered"
)

# Set toolbar mode to viewer
st.set_option("client.toolbarMode", "viewer")

# Create a session state variable to store messages
def create_session():
    st.session_state.session_id = uuid.uuid4().hex[:4]  # Replace with actual session ID logic
    st.session_state.messages = []

def send_message(message):
    if not st.session_state.get("session_id"):
        st.error("No session found. Please create a session first.")
        return False

    st.session_state.messages.append({"role": "user", "content": message})

    response = requests.post(
        f"{AGENT_BASE_URL}/generate",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "session_id": st.session_state.session_id,
            "current_message": message
        })
    )

    if response.status_code != 200:
        st.error(f"Error: {response.status_code} - {response.text}")
        return False

    data = response.json()

    assistant_message = None

    if isinstance(data, dict) and data.get("role") == "assistant":
        content = data.get("content", [])
        if content and isinstance(content[0], dict) and "text" in content[0]:
            assistant_message = content[0]["text"]

    if assistant_message:
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    return True

st.title("AWS Bedrock Agent Frontend")

with st.sidebar:
    st.header("Session Management")
    if st.session_state.get("session_id") is not None:
        st.success(f"Active session: {st.session_state.session_id}")
        if st.button("Create Session", icon=":material/add:"):
            create_session()
    else:
        st.warning("No active session")
        if st.button("Create Session", icon=":material/add:"):
            create_session()

st.divider()

for msg in st.session_state.get("messages", []):
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

if st.session_state.get("session_id") is not None:
    user_input = st.chat_input("Type your message here...", max_chars=500)
    if user_input:
        send_message(user_input)
        st.rerun()
else:
    st.info("👈 Please create a session to start chatting with the agent.")