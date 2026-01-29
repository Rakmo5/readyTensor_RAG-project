from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from project.api.schemas import IngestionResponse, QueryRequest, QueryResponse
from project.ingestion.background import process_document_ingestion
from project.app.rag import generate_rag_answer
from project.api.rate_limit import rate_limit_check
import os
import time

router = APIRouter()
UPLOAD_DIR = "project/data/uploads"

@router.post("/upload", response_model=IngestionResponse, tags=["Ingestion"])
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # 1. Basic Validation
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="Only .txt and .md are supported currently.")
    
    # 2. Save file locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # 3. Trigger the background ingestion
    background_tasks.add_task(process_document_ingestion, file_path, "default_user")
    
    return {
        "filename": file.filename, 
        "status": "processing", 
        "message": "File uploaded. Processing in background..."
    }
# Change this import at the top of routes.py
# From: from project.app.rag import generate_rag_answer
# To:
from project.app.chat import answer_question 
@router.post("/ask", response_model=QueryResponse, tags=["RAG"])
async def ask_question(request: QueryRequest):
    start_time = time.time()
    
    # 1. Check Rate Limiting first to save API costs
    try:
        rate_limit_check(request.user_id, limit=5, window=60)
    except HTTPException as e:
        # Re-raise the 429 error if limit is hit
        raise e

    try:
        # 2. Call the Conversational RAG engine
        response_content = answer_question(request.user_id, request.question)
        
        latency = time.time() - start_time
        return {
            "answer": response_content,
            "sources": [], 
            "latency": round(latency, 4)
        }

    except ConnectionError:
        # Handle cases where Groq or HF cannot be reached
        raise HTTPException(status_code=503, detail="AI Service is currently unreachable. Please try again later.")
    
    except Exception as e:
        # Catch-all for unexpected errors (DB locks, file permission issues, etc.)
        # Log the error on the server side for debugging
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal error occurred while processing your request.")