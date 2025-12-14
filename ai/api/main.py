from fastapi import FastAPI
from contextlib import asynccontextmanager

from ai.config.settings import ALLOWED_ORIGINS, OPENAI_API_KEY, CHATBOT_API_KEY
from ai.api.routers.chat import router as chat_router
from ai.api.routers.health import router as health_router
from ai.core.rag_manager import RAGManager
from ai.utils.logger import get_logger
from fastapi.middleware.cors import CORSMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Validate required environment variables
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY is not configured")
        raise RuntimeError("OPENAI_API_KEY environment variable is required")

    if not CHATBOT_API_KEY:
        logger.error("CHATBOT_API_KEY is not configured")
        raise RuntimeError("CHATBOT_API_KEY environment variable is required")

    RAGManager.initialize()
    logger.info("RAG manager initialized and data loaded")
    yield
    logger.info("Application shutting down")


def create_app() -> FastAPI:
    app = FastAPI(
        title="RAG Chatbot API",
        description="Retrieval-Augmented Generation API for intelligent chatbot",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-API-Key"],
    )

    app.include_router(health_router)
    app.include_router(chat_router)

    logger.info("FastAPI application created successfully")
    return app


app = create_app()
