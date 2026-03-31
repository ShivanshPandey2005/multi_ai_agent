from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState

llm = ChatGroq(model="llama-3.1-8b-instant")

def summarizer_node(state: AgentState):
    print("--- [SUMMARIZER] Generating drafted answer ---")
    query = state["query"]
    research = state["research"]
    critique = state.get("critique", "")
    
    if critique and critique != "APPROVED":
        prompt = ChatPromptTemplate.from_template(
            "Answer this query: '{query}' based on this research: {research}.\n"
            "Revise your answer to address this critique: {critique}.\nFormat cleanly."
        )
        chain = prompt | llm
        response = chain.invoke({"query": query, "research": research, "critique": critique})
    else:
        prompt = ChatPromptTemplate.from_template("Summarize this clearly: {research}\n\nQuery: {query}")
        chain = prompt | llm
        response = chain.invoke({"query": query, "research": research})
        
    return {"answer": response.content}
