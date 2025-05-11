from phi.knowledge.text import TextKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.embedder.google import GeminiEmbedder
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Gemini embedder
embedder = GeminiEmbedder()

# Database connection string
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Create a knowledge base for the LoraLab information
knowledge_base = TextKnowledgeBase(
    path="data/txt_files",
    formats=[".txt"],
    vector_db=PgVector(
        table_name="loralab_documents",
        db_url=db_url,
        embedder=embedder,  # Use Gemini embedder
    ),
    num_documents=5,  # Number of relevant documents to return for each query
) 