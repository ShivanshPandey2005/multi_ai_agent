import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Initialize local embeddings (zero cost, no API key)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Path to store the FAISS index locally
DB_FAISS_PATH = "vectorstore/db_faiss"

def save_to_memory(text: str, metadata: dict = None):
    """Saves a research snippet to the local FAISS vector store."""
    doc = Document(page_content=text, metadata=metadata or {})
    
    if os.path.exists(DB_FAISS_PATH):
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        db.add_documents([doc])
    else:
        db = FAISS.from_documents([doc], embeddings)
    
    db.save_local(DB_FAISS_PATH)
    print(f"--- [MEMORY] Saved new research snippet to FAISS ---")

def search_memory(query: str, k: int = 3):
    """Searches long-term memory for relevant research snippets."""
    if not os.path.exists(DB_FAISS_PATH):
        return "No existing memory found."
    
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    results = db.similarity_search(query, k=k)
    
    context = "\n".join([res.page_content for res in results])
    print(f"--- [MEMORY] Retrieved {len(results)} relevant snippets ---")
    return context
