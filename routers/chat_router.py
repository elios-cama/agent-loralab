import uuid
from fastapi import APIRouter, HTTPException
from typing import Dict

from models.chat_models import ChatRequest, ChatResponse
from agents.loralab_agent import LoraLabAgent

router = APIRouter(prefix="/api", tags=["chat"])

# Initialize agent
loralab_agent = LoraLabAgent()

# Simple conversation storage
conversations: Dict[str, str] = {}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
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