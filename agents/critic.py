from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState

llm = ChatGroq(model="llama-3.1-8b-instant")

def critic_node(state: AgentState):
    """Critic: Reviews the answer for accuracy and completeness."""
    print("--- [CRITIC] Reviewing answer ---")
    query = state["query"]
    answer = state["answer"]
    
    prompt = ChatPromptTemplate.from_template(
        "You are an expert critic. Review this answer for the query: '{query}'\n\n"
        "Answer: {answer}\n\n"
        "If the answer is excellent, respond with 'APPROVED'. "
        "Otherwise, provide specific feedback on how to improve it."
    )
    chain = prompt | llm
    response = chain.invoke({"query": query, "answer": answer})
    
    # Track revision count
    count = state.get("revision_count", 0)
    return {"critique": response.content, "revision_count": count + 1}
