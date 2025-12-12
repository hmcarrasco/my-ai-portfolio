from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Schema for RAG question requests."""

    question: str = Field(min_length=3, max_length=256)


class AnswerResponse(BaseModel):
    """Schema for RAG answer responses."""

    question: str
    answer: str
