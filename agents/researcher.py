import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from agents.state import AgentState
from tools.search_tool import search_tool
from tools.memory_tool import save_to_memory, search_memory

# Initialize the LLM (Groq)
llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tools = llm.bind_tools([search_tool])

def researcher_node(state: AgentState):
    """Researcher: Fetches information from memory first, then the web."""
    print("--- [RESEARCHER] Checking memory and gathering information ---")
    query = state["query"]
    plan = state["plan"]
    
    # 1. SEARCH MEMORY FIRST
    memory_context = search_memory(query)
    
    # 2. RUN SEARCH TOOL (if needed)
    prompt = ChatPromptTemplate.from_template(
        "Original Query: {query}\n"
        "Plan: {plan}\n"
        "Existing Memory: {memory}\n\n"
        "Use the search tool to get NEW data for the plan. "
        "Focus on gaps in the existing memory."
    )
    chain = prompt | llm_with_tools
    response = chain.invoke({"query": query, "plan": plan, "memory": memory_context})
    
    research_results = ""
    if response.tool_calls:
        for tool_call in response.tool_calls:
            print(f"--- [RESEARCHER] Calling tool: {tool_call['name']} ---")
            tool_output = str(search_tool.invoke(tool_call['args']))
            research_results += tool_output
            
            # 3. SAVE NEW RESULTS TO MEMORY
            save_to_memory(tool_output, metadata={"query": query})
    else:
        research_results = response.content
        
    return {
        "research": research_results, 
        "memory_context": memory_context
    }
