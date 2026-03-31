# Multi AI Agent 🧠
A production-ready Multi AI Agent System built with LangGraph, LangChain, Groq (LLaMA-3.1), and FastAPI, featuring a beautiful Streamlit UI.

## 🌟 Features
- **LangGraph Stateful Workflow**: A robust graph that coordinates multiple specialized agents.
- **Planner Agent**: Breaks complex user queries into logical research steps.
- **Researcher Agent**: Tool-enabled agent that searches the web (via Serper).
- **Summarizer Agent**: Synthesizes the final answer.
- **Critic Agent & Revision Loop**: Reviews the answer for accuracy and completeness. Prompts revisions if the answer is inadequate.
- **FastAPI Backend**: A highly performant async API (`/ask`).
- **Streamlit Frontend**: A sleek, modern chat interface.
- **Docker Ready**: One-command deployment via Docker Compose.

## 🏗️ Architecture
The system uses LangGraph to manage the control flow between agents.

```mermaid
graph TD
    User([User Query]) --> Planner
    Planner --> Researcher
    Researcher --> Summarizer
    Summarizer --> Critic
    Critic -- "If 'APPROVED'" --> Final([Final Output])
    Critic -- "If 'NEEDS REVISION'" --> Summarizer
```

## 🚀 Setup & Installation

### Option 1: Using Docker (Recommended)
1. Ensure Docker and Docker Compose are installed.
2. Clone this repository or copy the files.
3. Open the `.env` file and insert your API keys:
   ```env
   GROQ_API_KEY=your_groq_key_here
   SERPER_API_KEY=your_serper_key_here
   ```
4. Run the application:
   ```bash
   docker-compose up --build
   ```
5. Open your browser and navigate to **http://localhost:8501** for the UI. (The API is at `http://localhost:8000`).

### Option 2: Local Python Environment
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Update the `.env` file with your API keys.
3. Start the FastAPI Server:
   ```bash
   python main.py
   ```
4. In a new terminal, start the Streamlit UI:
   ```bash
   streamlit run ui/app.py
   ```
5. Access the UI at **http://localhost:8501**.

## 🛠️ Built With
- [LangGraph](https://python.langchain.com/docs/langgraph)
- [LangChain](https://python.langchain.com/)
- [Groq](https://groq.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
