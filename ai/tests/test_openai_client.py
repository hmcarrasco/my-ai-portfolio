import pytest
from unittest.mock import MagicMock, patch
from ai.clients.openai_client import OpenaiClient


class TestOpenaiClient:
    """Test suite for OpenaiClient class."""

    @pytest.fixture
    def mock_openai(self):
        """Mock OpenAI client."""
        with patch("ai.clients.openai_client.OpenAI") as mock:
            mock_instance = MagicMock()
            mock.return_value = mock_instance
            yield mock_instance

    @pytest.fixture
    def openai_client(self, mock_openai):
        """Create an OpenaiClient instance for testing."""
        return OpenaiClient(
            openai_api_key="test-key",
            system_prompt="You are a helpful assistant.",
        )

    def test_initialization(self, openai_client):
        """Test OpenaiClient initialization."""
        assert openai_client.model == "gpt-4.1-mini"
        assert openai_client.temperature == 0.0

    @pytest.mark.parametrize(
        "model,temperature",
        [
            ("gpt-4", 0.5),
            ("gpt-3.5-turbo", 0.0),
            ("gpt-4.1-mini", 0.7),
        ],
    )
    def test_initialization_with_parameters(self, mock_openai, model, temperature):
        """Test OpenaiClient initialization with custom parameters."""
        client = OpenaiClient(
            openai_api_key="test-key",
            model=model,
            temperature=temperature,
            system_prompt="You are a helpful assistant.",
        )

        assert client.model == model
        assert client.temperature == temperature

    def test_get_response_includes_system_prompt(self, openai_client, mock_openai):
        """Test that get_response includes system prompt."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello! How can I help?"
        mock_openai.chat.completions.create.return_value = mock_response

        response = openai_client.get_response("Hello")

        assert response == "Hello! How can I help?"
        call_args = mock_openai.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "You are a helpful assistant."
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "Hello"

    def test_get_response_without_system_prompt(self, mock_openai):
        """Test get_response works without system prompt."""
        client = OpenaiClient(openai_api_key="test-key")
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hi"
        mock_openai.chat.completions.create.return_value = mock_response

        response = client.get_response("Hello")

        assert response == "Hi"
        call_args = mock_openai.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        assert len(messages) == 1
        assert messages[0]["role"] == "user"

    def test_get_response_error_handling(self, openai_client, mock_openai):
        """Test error handling in response generation."""
        mock_openai.chat.completions.create.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="API Error"):
            openai_client.get_response("Test message")
