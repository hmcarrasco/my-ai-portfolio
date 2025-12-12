import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv("ai/config/.env")

# API Configuration
CHATBOT_API_KEY = os.getenv("CHATBOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# CORS Configuration
ALLOWED_ORIGINS: List[str] = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000"
).split(",")

# RAG Configuration
DATA_PATH = "ai/data/my-data.txt"
CHROMA_COLLECTION = "rag_docs"
CHROMA_PERSIST_PATH = "./chroma_db"

# Indexing parameters
CHUNK_SIZE = 256
CHUNK_OVERLAP = 20
