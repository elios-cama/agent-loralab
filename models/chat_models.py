from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's question")
    agent_type: Literal["loralab"] = Field(..., description="Type of agent to query (only loralab is supported)")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID for continuing a chat")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Agent's response")
    conversation_id: str = Field(..., description="Conversation ID for continuing the chat") 