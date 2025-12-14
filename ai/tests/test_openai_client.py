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

    def test_memory_is_condensed_after_summarization(self, openai_client, mock_openai):
        """When summarization triggers, memory should not grow unbounded."""
        openai_client.max_messages = 4
        
        # Fill memory to just under the limit
        openai_client.memory = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "msg1"},
            {"role": "assistant", "content": "resp1"},
        ]

        mock_answer1 = MagicMock()
        mock_answer1.choices[0].message.content = "answer1"
        mock_openai.chat.completions.create.return_value = mock_answer1

        # This adds user + assistant, making memory = 5 items
        out1 = openai_client.generate_response_with_memory("msg2")
        assert out1 == "answer1"
        assert len(openai_client.memory) == 5

        # Next message would make it 6 (5 + 1), which exceeds limit of 4
        # Should trigger summarization BEFORE adding user message
        mock_summary = MagicMock()
        mock_summary.choices[0].message.content = "User asked questions"

        mock_answer2 = MagicMock()
        mock_answer2.choices[0].message.content = "answer2"

        mock_openai.chat.completions.create.side_effect = [mock_summary, mock_answer2]

        out2 = openai_client.generate_response_with_memory("msg3")
        assert out2 == "answer2"

        # Memory should be condensed to 3 items
        assert len(openai_client.memory) == 3
        assert openai_client.memory[0]["role"] == "system"
        assert "Conversation summary:" in openai_client.memory[0]["content"]
        assert openai_client.memory[1]["role"] == "user"
        assert openai_client.memory[1]["content"] == "msg3"
        assert openai_client.memory[2]["role"] == "assistant"
        assert openai_client.memory[2]["content"] == "answer2"
