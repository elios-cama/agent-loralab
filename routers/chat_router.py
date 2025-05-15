import uuid
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
import time
from fastapi import Request
from fastapi.responses import JSONResponse

from models.chat_models import ChatRequest, ChatResponse
from agents.loralab_agent import LoraLabAgent

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize agent
loralab_agent = LoraLabAgent()

# Simple conversation storage
conversations: Dict[str, str] = {}

# Rate limiting implementation
class RateLimiter:
    def __init__(self, max_calls: int = 10, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.requests = {}  # IP to list of timestamps
        
    async def __call__(self, request: Request):
        ip = request.client.host
        now = time.time()
        
        # Initialize if IP not seen
        if ip not in self.requests:
            self.requests[ip] = []
            
        # Clean old requests outside time window
        self.requests[ip] = [t for t in self.requests[ip] if t > now - self.window_seconds]
        
        # Check if limit exceeded
        if len(self.requests[ip]) >= self.max_calls:
            raise HTTPException(
                status_code=429, 
                detail=f"Rate limit exceeded. Maximum {self.max_calls} requests per {self.window_seconds} seconds."
            )
            
        # Add current request timestamp
        self.requests[ip].append(now)
        
        return True

# Create rate limiter instance (10 requests per minute)
rate_limiter = RateLimiter(max_calls=10, window_seconds=60)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, is_allowed: bool = Depends(rate_limiter)):
    """Process a chat request using the LoraLab agent"""
    try:
        # Create conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Store conversation context (simplified version)
        if conversation_id in conversations:
            conversations[conversation_id] += f"\nUser: {request.query}"
        else:
            conversations[conversation_id] = f"User: {request.query}"
        
        # Process with LoraLab agent
        if request.agent_type == "loralab":
            response = await loralab_agent.chat(request.query)
        else:
            raise HTTPException(status_code=400, detail="Invalid agent type. Only 'loralab' is supported.")
        
        # Update conversation
        conversations[conversation_id] += f"\nAssistant: {response}"
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}") 