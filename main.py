import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph.workflow import create_workflow

app = FastAPI(title="Multi AI Agent API")

# Initialize the workflow
graph = create_workflow()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    final_answer: str

@app.post("/ask", response_model=QueryResponse)
async def ask_query(request: QueryRequest):
    """Invoke the LangGraph workflow and return the final answer."""
    initial_state = {
        "query": request.query,
        "revision_count": 0
    }
    
    print(f"\n--- [API] New query: {request.query} ---")
    try:
        # Run the graph
        result = graph.invoke(initial_state)
        
        return QueryResponse(
            final_answer=result.get("answer", "No answer generated.")
        )
    except Exception as e:
        print(f"Error executing graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Multi-Agent LangGraph API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
