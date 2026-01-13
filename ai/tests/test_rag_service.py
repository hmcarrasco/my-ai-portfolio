from unittest.mock import MagicMock, patch

import pytest

from ai.clients.rag_service import RAGService


@pytest.fixture
def mock_chroma_collection():
    collection = MagicMock()
    collection.count.return_value = 0
    return collection


@pytest.fixture
def mock_chroma_client(mock_chroma_collection):
    client = MagicMock()
    client.get_or_create_collection.return_value = mock_chroma_collection
    return client


@pytest.fixture
def mock_openai_client():
    client = MagicMock()
    client.generate_response_with_memory.return_value = "mock-answer"
    return client


@pytest.fixture
def mock_embedding_function():
    """Mock OpenAI embedding function."""
    with patch("ai.clients.rag_service.OpenAIEmbeddingFunction") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance


def test_add_document_defaults_metadata_when_none(
    mock_openai_client,
    mock_chroma_client,
    mock_chroma_collection,
    mock_embedding_function,
):
    with patch(
        "ai.clients.rag_service.PersistentClient", return_value=mock_chroma_client
    ):
        service = RAGService(
            openai_client=mock_openai_client,
            openai_api_key="test-key",
            persist_path="/tmp/chroma",
        )
        service.add_document("doc1", "hello", metadata=None)

    mock_chroma_collection.add.assert_called_once()
    _, kwargs = mock_chroma_collection.add.call_args
    assert kwargs["metadatas"] == [{"source": "ingest"}]


def test_add_document_uses_metadata_when_provided(
    mock_openai_client,
    mock_chroma_client,
    mock_chroma_collection,
    mock_embedding_function,
):
    with patch(
        "ai.clients.rag_service.PersistentClient", return_value=mock_chroma_client
    ):
        service = RAGService(
            openai_client=mock_openai_client,
            openai_api_key="test-key",
            persist_path="/tmp/chroma",
        )
        service.add_document("doc1", "hello", metadata={"source": "unit"})

    _, kwargs = mock_chroma_collection.add.call_args
    assert kwargs["metadatas"] == [{"source": "unit"}]


def test_retrieve_returns_documents(
    mock_openai_client,
    mock_chroma_client,
    mock_chroma_collection,
    mock_embedding_function,
):
    mock_chroma_collection.query.return_value = {"documents": [["a", "b"]]}

    with patch(
        "ai.clients.rag_service.PersistentClient", return_value=mock_chroma_client
    ):
        service = RAGService(
            openai_client=mock_openai_client,
            openai_api_key="test-key",
            persist_path="/tmp/chroma",
        )
        docs = service.retrieve("q", n_results=2)

    assert docs == ["a", "b"]


def test_answer_with_rag_builds_prompt_and_calls_openai(
    mock_openai_client,
    mock_chroma_client,
    mock_chroma_collection,
    mock_embedding_function,
):
    mock_chroma_collection.query.return_value = {"documents": [["ctx1", "ctx2"]]}

    with patch(
        "ai.clients.rag_service.PersistentClient", return_value=mock_chroma_client
    ):
        service = RAGService(
            openai_client=mock_openai_client,
            openai_api_key="test-key",
            persist_path="/tmp/chroma",
        )
        out = service.answer_with_rag("my question")

    assert out == "mock-answer"
    called_prompt = mock_openai_client.generate_response_with_memory.call_args[0][0]
    assert "Context:" in called_prompt
    assert "ctx1" in called_prompt
    assert "ctx2" in called_prompt
    assert "Question: my question" in called_prompt
