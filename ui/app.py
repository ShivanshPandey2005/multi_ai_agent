import streamlit as st
import requests
import time

# Page Configuration
st.set_page_config(
    page_title="Multi AI Agent",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .agent-status {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 5px solid #4CAF50;
        background-color: #1e2130;
    }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.title("🧠 Multi AI Agent")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check for API URL via environment variable first (for Docker compatibility)
    import os
    default_url = os.environ.get("API_URL", "http://localhost:8000/ask")
    api_url = st.text_input("API URL", value=default_url)
    
    st.info("Ensure the FastAPI server is running before sending queries.")
    
    st.markdown("### Agents in Workflow")
    st.write("📍 Planner")
    st.write("🔍 Researcher (Serper)")
    st.write("✍️ Summarizer")
    st.write("⚖️ Critic")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        
        # Simulate active agent flow
        agents = ["Planner", "Researcher", "Summarizer", "Critic"]
        for agent in agents:
            status_placeholder.markdown(f"⏳ **{agent}** is processing...")
            time.sleep(1)
            
        try:
            # Call FastAPI Backend
            response = requests.post(api_url, json={"query": prompt})
            if response.status_code == 200:
                answer = response.json().get("final_answer", "No answer found.")
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
        finally:
            status_placeholder.empty()
