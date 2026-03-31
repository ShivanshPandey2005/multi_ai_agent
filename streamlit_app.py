import streamlit as st
import os

# 1. Load API Keys (MUST BE BEFORE ANY LANGCHAIN IMPORTS)
# Streamlit Community Cloud uses st.secrets for production deployment
try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
    if "SERPER_API_KEY" in st.secrets:
        os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
except Exception:
    # Secrets not configured yet in the dashboard
    pass

# For local development if secrets are not available
if not os.environ.get("GROQ_API_KEY"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

import time
from graph.workflow import create_workflow

# For local development if secrets are not available
if not os.environ.get("GROQ_API_KEY"):
    from dotenv import load_dotenv
    load_dotenv()

# 3. Custom CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 4. App Title
st.title("🧠 Multi AI Agent (Unified)")
st.caption("Direct Service Deployment via Streamlit Cloud")
st.markdown("---")

# 5. Initialize Workflow
@st.cache_resource
def get_graph():
    return create_workflow()

graph = get_graph()

# 6. Sidebar
with st.sidebar:
    st.header("⚙️ Status")
    if os.environ.get("GROQ_API_KEY") and os.environ.get("SERPER_API_KEY"):
        st.success("API Keys Loaded")
    else:
        st.warning("API Keys Missing (Check Secrets)")
    
    st.markdown("### Workflow Agents")
    st.write("📍 Planner")
    st.write("🔍 Researcher (Serper + FAISS)")
    st.write("✍️ Summarizer")
    st.write("⚖️ Critic")

# 7. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask the Multi AI Agent..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        
        try:
            # Execute LangGraph Directly
            inputs = {"query": prompt, "revision_count": 0}
            
            # Simple synchronous execution for the UI
            # (In a more advanced version, we could stream the status of each node)
            status_placeholder.markdown("⏳ **Planner** is working...")
            state = graph.invoke(inputs)
            
            # Final result extraction
            answer = state.get("answer", "No answer generated.")
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"Execution Error: {e}")
        finally:
            status_placeholder.empty()
