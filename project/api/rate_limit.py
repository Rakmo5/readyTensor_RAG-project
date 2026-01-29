import time
from fastapi import HTTPException, Request

# Simple In-Memory Store: {user_id: [timestamps]}
usage_data = {}

def rate_limit_check(user_id: str, limit: int = 5, window: int = 60):
    now = time.time()
    if user_id not in usage_data:
        usage_data[user_id] = []
    
    # Clean up old timestamps
    usage_data[user_id] = [t for t in usage_data[user_id] if now - t < window]
    
    if len(usage_data[user_id]) >= limit:
        raise HTTPException(status_code=429, detail="Too many requests. Please wait a minute.")
    
    usage_data[user_id].append(now)