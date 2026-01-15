from openai import OpenAI

from ai.utils.logger import get_logger

logger = get_logger(__name__)


class OpenaiClient:
    def __init__(
        self,
        openai_api_key: str,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.2,
        max_messages: int = 6,
        system_prompt: str = "",
        summary_prompt: str = "",
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
        self.temperature = temperature
        self.max_messages = max_messages
        self.system_prompt = system_prompt
        self.summary_prompt = summary_prompt
        self.memory: list[dict[str, str]] = []
        self.summary: str | None = None

    def generate_response_with_memory(self, user_prompt: str) -> str:
        """
        Generate a response considering session memory. If memory exceeds max_messages,
        summarize previous messages to reduce token usage.

        Args:
            user_prompt: User's prompt.

        Returns:
            str: Model response content.
        """
        if not self.memory:
            self.memory.append({"role": "system", "content": self.system_prompt})

        # Check if adding user message would exceed limit
        if len(self.memory) + 1 > self.max_messages:
            # Summarize before adding new message
            self.summary = self._summarize_memory(self.memory)

            # Reset memory to condensed version
            self.memory = [
                {
                    "role": "system",
                    "content": f"{self.system_prompt}\nConversation summary: {self.summary}",
                }
            ]

        self.memory.append({"role": "user", "content": user_prompt})

        try:
            assistant_response = self._call_chat_completion(self.memory)
            self.memory.append({"role": "assistant", "content": assistant_response})

            logger.info(
                "Response generated successfully for user prompt: '%s'", user_prompt
            )
            return assistant_response
        except Exception as e:
            logger.error(
                "Error generating response for user prompt '%s': %s", user_prompt, e
            )
            return "[Error generating response]"

    def get_response(self, prompt: str) -> str:
        """
        Generate a single response without memory (stateless).
        Use for one-off requests.

        Args:
            prompt: The prompt to send to the model.

        Returns:
            str: Model response content.
        """
        messages = [{"role": "user", "content": prompt}]

        try:
            response = self._call_chat_completion(messages)
            logger.info("Stateless response generated successfully")
            return response
        except Exception as e:
            logger.error("Error generating stateless response: %s", e)
            raise

    def clear_memory(self) -> None:
        """Clear session memory and summary."""
        self.memory = []
        self.summary = None

    def _call_chat_completion(self, messages: list[dict[str, str]]) -> str:
        """
        Internal method to call Chat Completions API.

        Args:
            messages: List of messages (dict with 'role' and 'content').

        Returns:
            str: Model response content.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("OpenAI API call failed: %s", e, exc_info=True)
            raise

    def _summarize_memory(self, memory_to_summarize: list[dict[str, str]]) -> str:
        """
        Generate a summary of old messages to reduce token usage.

        Args:
            memory_to_summarize: List of messages to summarize.

        Returns:
            str: Summary text.
        """
        try:
            prompt = self.summary_prompt + "\n\n"
            for msg in memory_to_summarize:
                prompt += f"{msg['role']}: {msg['content']}\n"
            summary = self._call_chat_completion([{"role": "user", "content": prompt}])
            logger.info("Memory summarized successfully.")
            return summary
        except Exception as e:
            logger.error("Error summarizing memory: %s", e, exc_info=True)
            raise
