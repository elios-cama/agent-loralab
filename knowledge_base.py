from phi.knowledge.text import TextKnowledgeBase
from phi.vectordb.pgvector import PgVector
from phi.embedder.google import GeminiEmbedder
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Gemini embedder
embedder = GeminiEmbedder()

# Get database connection string from environment variable or use default
# This allows for different configurations in local and Railway environments
db_url = os.getenv("PG_DB_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")

# For Railway with PostgreSQL addon:
# Railway automatically sets DATABASE_URL when using their PostgreSQL addon
if os.getenv("DATABASE_URL"):
    # Use the Railway-provided DATABASE_URL
    db_url = os.getenv("DATABASE_URL")

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