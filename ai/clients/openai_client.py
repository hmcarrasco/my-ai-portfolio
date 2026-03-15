from openai import OpenAI

from ai.utils.logger import get_logger

logger = get_logger(__name__)


class OpenaiClient:
    def __init__(
        self,
        openai_api_key: str,
        model: str = "gpt-4.1-mini",
        temperature: float = 0.0,
        system_prompt: str = "",
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt

    def get_response(self, prompt: str) -> str:
        """
        Generate a response with the system prompt context.

        Args:
            prompt: The prompt to send to the model.

        Returns:
            str: Model response content.
        """
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = self._call_chat_completion(messages)
            logger.info("Response generated successfully")
            return response
        except Exception as e:
            logger.error("Error generating response: %s", e)
            raise

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
