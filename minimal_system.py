import os
from typing import List, TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

# Load environment variables
load_dotenv()

# Initialize the LLM (Groq)
llm = ChatGroq(model="llama-3.1-8b-instant")

# 1. Define the State
class AgentState(TypedDict):
    query: str
    plan: str
    research: str
    answer: str

# 2. Define the Agent Nodes (Real LLM calls)

def planner_node(state: AgentState):
    """Planner: Breaks the user query into research steps."""
    print("--- [PLANNER] Generating research plan ---")
    query = state["query"]
    prompt = ChatPromptTemplate.from_template("Break this query into steps: {query}")
    chain = prompt | llm
    response = chain.invoke({"query": query})
    return {"plan": response.content}

def researcher_node(state: AgentState):
    """Researcher: Fetches detailed information about the query."""
    print("--- [RESEARCHER] Gathering information ---")
    query = state["query"]
    prompt = ChatPromptTemplate.from_template("Provide detailed information about: {query}")
    chain = prompt | llm
    response = chain.invoke({"query": query})
    return {"research": response.content}

def summarizer_node(state: AgentState):
    """Summarizer: Compiles research data into a final answer."""
    print("--- [SUMMARIZER] Generating final answer ---")
    research = state["research"]
    prompt = ChatPromptTemplate.from_template("Summarize this clearly: {research}")
    chain = prompt | llm
    response = chain.invoke({"research": research})
    return {"answer": response.content}

# 3. Build the Graph
def create_graph():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("summarizer", summarizer_node)

    # Add Edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "summarizer")
    workflow.add_edge("summarizer", END)

    # Compile Graph
    return workflow.compile()

# 4. Entry Point for Testing
if __name__ == "__main__":
    app = create_graph()
    
    # Run a test query
    initial_state = {"query": "Tell me about LangGraph and Multi-Agent systems."}
    
    print("\n--- Starting Workflow Execution ---\n")
    try:
        result = app.invoke(initial_state)
        print("\n--- Final Output ---\n")
        print(result["answer"])
    except Exception as e:
        print(f"\n--- Error Occurred ---\n{e}")
        print("\nMake sure your GROQ_API_KEY is correctly set in the .env file.")
