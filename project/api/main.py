from fastapi import FastAPI
import os
from dotenv import load_dotenv
from pathlib import Path
from project.api.routes import router as api_router
import warnings
# Calculate the path to the .env file inside the 'project' folder
# Since main.py is in project/api, we go up one level
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Verify the key is loaded (for debugging)
if not os.environ.get("GROQ_API_KEY"):
    print("⚠️ Warning: GROQ_API_KEY not found in .env file")
    
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

app = FastAPI(
    title="RAG-Based QA System API",
    description="Backend API for document ingestion and retrieval-augmented generation.",
    version="1.0.0"
)

# Include the router we just created
app.include_router(api_router)

@app.get("/health", tags=["General"])
async def health_check():
    return {"status": "healthy", "message": "RAG API is operational"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)