import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv("ai/config/.env") or load_dotenv()

# API Configuration
CHATBOT_API_KEY = os.getenv("CHATBOT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

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

# GitHub API Configuration
GITHUB_API_BASE_URL = "https://api.github.com"

# Documentation Generator Configuration
DOCS_CACHE_DIR = "ai/data/docs_cache"
DOCS_CACHE_MAX_AGE_DAYS = 30

# Prompts Configuration
CHATBOT_PROMPTS_PATH = "ai/prompts/chatbot.yaml"
DOC_GENERATOR_PROMPTS_PATH = "ai/prompts/doc_generator.yaml"


class Settings:
    """Application settings with typed access."""

    def __init__(self) -> None:
        # API Keys
        self.openai_api_key: str = OPENAI_API_KEY or ""
        self.chatbot_api_key: str = CHATBOT_API_KEY or ""
        self.github_token: str | None = GITHUB_TOKEN

        # OpenAI
        self.openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        # CORS
        self.allowed_origins: List[str] = ALLOWED_ORIGINS

        # RAG
        self.data_path: str = DATA_PATH
        self.chroma_collection: str = CHROMA_COLLECTION
        self.chroma_persist_path: str = CHROMA_PERSIST_PATH
        self.chunk_size: int = CHUNK_SIZE
        self.chunk_overlap: int = CHUNK_OVERLAP

        # GitHub API
        self.github_api_base_url: str = GITHUB_API_BASE_URL

        # Documentation Generator
        self.docs_cache_dir: str = DOCS_CACHE_DIR
        self.docs_cache_max_age_days: int = DOCS_CACHE_MAX_AGE_DAYS

        # Prompts
        self.chatbot_prompts_path: str = CHATBOT_PROMPTS_PATH
        self.doc_generator_prompts_path: str = DOC_GENERATOR_PROMPTS_PATH


settings = Settings()
