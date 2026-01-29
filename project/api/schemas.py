from pydantic import BaseModel
from typing import Optional, List

class QueryRequest(BaseModel):
    question: str
    user_id: str = "default_user"
    session_id: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    latency: float  # We track this as our primary metric

class IngestionResponse(BaseModel):
    filename: str
    status: str
    message: str