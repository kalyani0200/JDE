from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import uvicorn
from helper import process_query  # Importing your existing query processing function

# Initialize FastAPI app
app = FastAPI()
load_dotenv()

# Request body structure
class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def query_product(request: Request):
    """
    Accepts raw JSON input like: {"query": "your question here"}
    """
    try:
        body = await request.json()
        query = body.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="Missing 'query' in request body.")
        
        print(f"Received query: {query}")
        result = process_query(query)
        return {"status": "success", "result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health/")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
