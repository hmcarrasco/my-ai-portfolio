from fastapi import APIRouter, Depends, HTTPException, Request

from ai.api.main import limiter
from ai.api.schemas.chat import QuestionRequest, AnswerResponse
from ai.api.security import verify_api_key
from ai.core.chat_service import ChatService
from ai.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service() -> ChatService:
    """
    Dependency to get ChatService instance.

    Returns:
        ChatService: Initialized chat service.
    """
    return ChatService.get_instance()


@router.post(
    "/ask", response_model=AnswerResponse, dependencies=[Depends(verify_api_key)]
)
@limiter.limit("5/minute")
def ask_question(
    request: Request,
    req: QuestionRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> AnswerResponse:
    """
    Ask a question and receive an answer using RAG.

    Args:
        req (QuestionRequest): The user's question.
        chat_service (ChatService): Chat service instance (auto-injected).

    Returns:
        AnswerResponse: The question and generated answer.

    Raises:
        HTTPException: If an error occurs during answer generation.
    """
    logger.info("Received question: %s", req.question)
    try:
        answer = chat_service.answer_question(req.question)
        logger.info("Answer generated successfully for question: %s", req.question)
        return AnswerResponse(question=req.question, answer=answer)
    except Exception as e:
        logger.error("Error generating answer: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {type(e).__name__}.",
        )
