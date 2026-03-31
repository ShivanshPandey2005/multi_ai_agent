from typing import TypedDict, List

class AgentState(TypedDict):
    query: str
    plan: str
    research: str
    answer: str
    critique: str
    revision_count: int
    memory_context: str
