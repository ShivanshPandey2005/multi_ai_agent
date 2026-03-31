from langgraph.graph import StateGraph, START, END
from agents.state import AgentState
from agents.planner import planner_node
from agents.researcher import researcher_node
from agents.summarizer import summarizer_node
from agents.critic import critic_node

def should_continue(state: AgentState):
    """Conditional edge from critic back to summarizer or researcher."""
    critique = state.get("critique", "").strip().upper()
    count = state.get("revision_count", 0)
    
    if "APPROVED" in critique or count >= 2:
        return "end"
    else:
        return "revise"

def create_workflow():
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("summarizer", summarizer_node)
    workflow.add_node("critic", critic_node)

    # Add Edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "summarizer")
    workflow.add_edge("summarizer", "critic")
    
    # Conditional Edge from Critic
    workflow.add_conditional_edges(
        "critic",
        should_continue,
        {
            "revise": "summarizer",
            "end": END
        }
    )

    # Compile Graph
    return workflow.compile()
