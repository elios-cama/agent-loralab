import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import traceback

from routers.chat_router import router as chat_router
from agents.loralab_agent import LoraLabAgent

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Portfolio AI Assistant API",
    description="API for interacting with AI agents that provide information about my portfolio",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Initialize knowledge base on startup
@app.on_event("startup")
async def startup_event():
    print("=== Starting Portfolio AI Application ===")
    try:
        print("Initializing LoraLab knowledge base...")
        agent = LoraLabAgent()
        success = agent.load_knowledge(recreate=False)  # Set to True to recreate on startup
        if success:
            print("Knowledge base loaded successfully!")
        else:
            print("Failed to load knowledge base!")
    except Exception as e:
        print(f"Critical error initializing knowledge base: {str(e)}")
        traceback.print_exc()
        print("Application will start but knowledge base functionality may be limited.")
    print("=== Startup complete ===")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 