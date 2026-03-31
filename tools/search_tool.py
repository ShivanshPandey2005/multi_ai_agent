import os
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool

@tool
def search_tool(query: str) -> str:
    """Useful to search the internet for information."""
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key or api_key == "your_serper_api_key_here":
        return f"MOCK SEARCH RESULTS for '{query}'. Please set a valid SERPER_API_KEY in the .env file to get real results."
    
    # Real serper API call
    search = GoogleSerperAPIWrapper(serper_api_key=api_key)
    return search.run(query)
