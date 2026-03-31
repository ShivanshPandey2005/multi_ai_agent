import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState

# Initialize the LLM (Groq)
llm = ChatGroq(model="llama-3.1-8b-instant")

def planner_node(state: AgentState):
    """Planner: Breaks the user query into research steps."""
    print("--- [PLANNER] Generating research plan ---")
    query = state["query"]
    prompt = ChatPromptTemplate.from_template("Break this query into steps: {query}")
    chain = prompt | llm
    response = chain.invoke({"query": query})
    return {"plan": response.content}
