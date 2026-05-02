import os
import time
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.retrieve import RAGRetriever

# Initialize FastAPI app
app = FastAPI(title="BIS Recommendation Engine API")

# Mount the static directory to serve HTML/CSS/JS
base_dir = os.path.dirname(__file__)
static_dir = os.path.join(base_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Load RAG Retriever globally
index_path = os.path.join(base_dir, "standards.index")
meta_path = os.path.join(base_dir, "metadata.json")

# It will print an error if the files don't exist, but won't crash until searched
retriever = None
if os.path.exists(index_path) and os.path.exists(meta_path):
    print("Loading RAG Retriever...")
    retriever = RAGRetriever(index_path, meta_path)
    print("Retriever loaded successfully.")

class SearchQuery(BaseModel):
    query: str

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.post("/search")
async def search_standards(request: SearchQuery):
    if not retriever:
        return {"error": "RAG Retriever not initialized. Please build the index first."}
    
    start_time = time.time()
    
    # Retrieve top 5 but return top 3
    retrieved = retriever.retrieve(request.query, top_k=5)
    top_standards = retrieved[:3]
    
    end_time = time.time()
    latency = round(end_time - start_time, 3)
    
    results = []
    for res in top_standards:
        results.append({
            "id": res["standard"]["id"],
            "title": res["standard"]["title"],
            "rationale": res["standard"]["description"],
            "confidence": f"{int((1 - res['distance']) * 100)}%"  # Pseudo confidence
        })
        
    return {
        "latency": latency,
        "results": results
    }
