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
    def mock_prompts(self):
        """Mock prompts loading."""
        with patch(
            "ai.clients.openai_client.load_yaml",
            return_value={
                "chatbot_system_prompt": "You are a helpful assistant.",
                "chatbot_summary_prompt": "Summarize the conversation:",
            },
        ):
            yield

    @pytest.fixture
    def openai_client(self, mock_openai, mock_prompts):
        """Create an OpenaiClient instance for testing."""
        return OpenaiClient(openai_api_key="test-key")

    def test_initialization(self, openai_client):
        """Test OpenaiClient initialization."""
        assert openai_client.model == "gpt-4.1-mini"
        assert openai_client.temperature == 0.2
        assert openai_client.max_messages == 6
        assert openai_client.memory == []
        assert openai_client.summary is None

    @pytest.mark.parametrize(
        "model,temperature,max_messages",
        [
            ("gpt-4", 0.5, 10),
            ("gpt-3.5-turbo", 0.0, 5),
            ("gpt-4.1-mini", 0.7, 15),
        ],
    )
    def test_initialization_with_parameters(
        self, mock_openai, mock_prompts, model, temperature, max_messages
    ):
        """Test OpenaiClient initialization with custom parameters."""
        client = OpenaiClient(
            openai_api_key="test-key",
            model=model,
            temperature=temperature,
            max_messages=max_messages,
        )

        assert client.model == model
        assert client.temperature == temperature
        assert client.max_messages == max_messages

    def test_clear_memory(self, openai_client):
        """Test clearing memory."""
        openai_client.memory = [{"role": "user", "content": "test"}]
        openai_client.summary = "Test summary"

        openai_client.clear_memory()

        assert openai_client.memory == []
        assert openai_client.summary is None

    def test_generate_response_with_memory_first_message(
        self, openai_client, mock_openai
    ):
        """Test generating response for first message."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Hello! How can I help?"
        mock_openai.chat.completions.create.return_value = mock_response

        response = openai_client.generate_response_with_memory("Hello")

        assert response == "Hello! How can I help?"
        assert len(openai_client.memory) == 3  # system + user + assistant

    def test_generate_response_error_handling(self, openai_client, mock_openai):
        """Test error handling in response generation."""
        mock_openai.chat.completions.create.side_effect = Exception("API Error")

        response = openai_client.generate_response_with_memory("Test message")

        assert response == "[Error generating response]"
