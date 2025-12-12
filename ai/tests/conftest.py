import pytest
import os
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    with patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "CHATBOT_API_KEY": "test-chatbot-key",
        "ALLOWED_ORIGINS": "http://localhost:3000",
    }):
        yield


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client to avoid real API calls."""
    with patch("ai.clients.openai_client.OpenAI") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_chroma_client():
    """Mock ChromaDB client to avoid real database operations."""
    with patch("ai.clients.rag_service.PersistentClient") as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance
