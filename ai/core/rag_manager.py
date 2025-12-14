import threading
from typing import Optional
from fastapi import HTTPException

from ai.clients.openai_client import OpenaiClient
from ai.clients.rag_service import RAGService
from ai.clients.chunker import TextChunker
from ai.config.settings import (
    OPENAI_API_KEY,
    CHROMA_COLLECTION,
    CHROMA_PERSIST_PATH,
    DATA_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)
from ai.utils.logger import get_logger

logger = get_logger(__name__)


class RAGManager:
    """
    Singleton manager for RAG service initialization and data ingestion.
    Handles lazy loading and caching of the RAG service.
    """

    _instance: Optional["RAGManager"] = None
    _rag_service: Optional[RAGService] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls) -> None:
        """
        Initialize the RAG manager and load/ingest data if needed.
        Called once on application startup.
        """
        manager = cls()
        manager._initialize_rag_service()

    @classmethod
    def get_rag_service(cls) -> RAGService:
        """
        Get the initialized RAG service instance.

        Returns:
            RAGService: Initialized RAG service.

        Raises:
            HTTPException: If RAG service is not initialized or OpenAI key is missing.
        """
        manager = cls()

        if manager._rag_service is None:
            manager._initialize_rag_service()

        if manager._rag_service is None:
            raise HTTPException(
                status_code=500, detail="RAG service initialization failed"
            )

        return manager._rag_service

    def _initialize_rag_service(self) -> None:
        """
        Private method to initialize RAG service and ingest data if needed.
        """
        with self._lock:
            if self._rag_service is not None:
                return

            logger.info("Initializing OpenAI client...")
            openai_client = OpenaiClient(openai_api_key=OPENAI_API_KEY)

            logger.info("Initializing RAG service...")
            self._rag_service = RAGService(
                openai_client=openai_client,
                chroma_collection=CHROMA_COLLECTION,
                persist_path=CHROMA_PERSIST_PATH,
            )

            # Ingest data if collection is empty
            doc_count = self._rag_service.collection.count()
            if doc_count == 0:
                self._ingest_data()
            else:
                logger.info("RAG service loaded with %d documents", doc_count)

    def _ingest_data(self) -> None:
        """
        Private method to ingest data from file into ChromaDB.
        """
        logger.info("ChromaDB collection empty, ingesting data from %s", DATA_PATH)

        try:
            chunker = TextChunker(chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
            chunks = chunker.chunk_file(DATA_PATH)

            for idx, chunk in enumerate(chunks):
                doc_id = f"doc_{idx}"
                self._rag_service.add_document(doc_id, chunk)

            logger.info("Data ingestion complete: %d chunks added.", len(chunks))
        except FileNotFoundError:
            logger.error("Data file not found: %s", DATA_PATH)
            raise HTTPException(
                status_code=500, detail=f"Data file not found: {DATA_PATH}"
            )
        except Exception as e:
            logger.error("Error during data ingestion: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail="Data ingestion failed")
