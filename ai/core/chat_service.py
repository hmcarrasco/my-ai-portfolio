from ai.core.rag_manager import RAGManager
from ai.clients.rag_service import RAGService
from ai.utils.logger import get_logger

logger = get_logger(__name__)


class ChatService:
    """
    Service layer for chat/RAG operations.
    Encapsulates business logic for answering questions using RAG.
    """

    def __init__(self, rag_service: RAGService):
        """
        Initialize ChatService with a RAG service instance.

        Args:
            rag_service (RAGService): The RAG service to use for queries.
        """
        self.rag_service = rag_service

    @staticmethod
    def get_instance() -> "ChatService":
        """
        Get a ChatService instance with the initialized RAG manager.

        Returns:
            ChatService: A new ChatService instance.
        """
        rag_service = RAGManager.get_rag_service()
        return ChatService(rag_service)

    def answer_question(self, question: str) -> str:
        """
        Answer a question using RAG.

        Args:
            question (str): The user's question.

        Returns:
            str: The generated answer.
        """
        logger.info("Answering question: %s", question)
        return self.rag_service.answer_with_rag(question)
