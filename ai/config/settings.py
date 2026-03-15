import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv("ai/config/.env") or load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# CORS Configuration
ALLOWED_ORIGINS: List[str] = os.getenv(
    "ALLOWED_ORIGINS"
).split(",")

# RAG Configuration
DATA_PATH = os.getenv("DATA_PATH", "ai/data/my-data.txt")
CHROMA_COLLECTION = "rag_docs"
CHROMA_PERSIST_PATH = "./ai/chroma_db"

# Indexing parameters
CHUNK_SIZE = 256
CHUNK_OVERLAP = 20

# GitHub API Configuration
GITHUB_API_BASE_URL = "https://api.github.com"
GITHUB_OWNER = os.getenv("GITHUB_OWNER")

# Documentation Generator Configuration
SOURCE_CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".c",
    ".cpp",
    ".h",
    ".cs",
    ".swift",
    ".kt",
}
MAX_SOURCE_CODE_CHARS = int(os.getenv("MAX_SOURCE_CODE_CHARS", "50000"))
MAX_FILE_CHARS = int(os.getenv("MAX_FILE_CHARS", "5000"))

# Prompts Configuration
CHATBOT_PROMPTS_PATH = "ai/prompts/chatbot_prompts.yaml"
DOC_GENERATOR_PROMPTS_PATH = "ai/prompts/doc_generator.yaml"
PROJECTS_PATH = "ai/config/projects.yaml"

# Documentation Cache
DOCS_CACHE_PATH = "ai/data/docs_cache"

# Openai Models
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class Settings:
    """Application settings with typed access."""

    def __init__(self) -> None:
        # API Keys
        self.openai_api_key: str = OPENAI_API_KEY
        self.github_token: str | None = GITHUB_TOKEN


        # OpenAI
        self.openai_model: str = OPENAI_MODEL
        self.openai_embedding_model: str = OPENAI_EMBEDDING_MODEL

        # CORS
        self.allowed_origins: List[str] = ALLOWED_ORIGINS

        # RAG
        self.data_path: str = DATA_PATH
        self.chroma_collection: str = CHROMA_COLLECTION
        self.chroma_persist_path: str = CHROMA_PERSIST_PATH
        self.chunk_size: int = CHUNK_SIZE
        self.chunk_overlap: int = CHUNK_OVERLAP
        self.github_api_base_url: str = GITHUB_API_BASE_URL
        self.github_owner: str = GITHUB_OWNER

        # Documentation Generator
        self.source_code_extensions: set[str] = SOURCE_CODE_EXTENSIONS
        self.max_source_code_chars: int = MAX_SOURCE_CODE_CHARS
        self.max_file_chars: int = MAX_FILE_CHARS

        # Prompts
        self.chatbot_prompts_path: str = CHATBOT_PROMPTS_PATH
        self.doc_generator_prompts_path: str = DOC_GENERATOR_PROMPTS_PATH
        self.projects_path: str = PROJECTS_PATH

        # Cache
        self.docs_cache_path: str = DOCS_CACHE_PATH


settings = Settings()
