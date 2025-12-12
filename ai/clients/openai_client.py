from openai import OpenAI
from ai.utils.loaders import load_yaml
from ai.utils.logger import get_logger

logger = get_logger(__name__)


class OpenaiClient:
    def __init__(
        self,
        openai_api_key: str,
        prompts_path: str = "ai/prompts.yaml",
        model: str = "gpt-4.1-mini",
        temperature: float = 0.2,
        max_messages: int = 6,
    ):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model
        self.temperature = temperature
        self.max_messages = max_messages
        self.memory = []
        self.summary = None

        prompts = load_yaml(prompts_path)
        self.system_prompt = prompts.get("chatbot_system_prompt", "")
        self.summary_prompt_template = prompts.get("chatbot_summary_prompt", "")

    def generate_response_with_memory(self, user_prompt: str) -> str:
        """
        Generate a response considering session memory. If memory exceeds max_messages,
        summarize previous messages to reduce token usage.

        Args:
            user_prompt (str): User's prompt.

        Returns:
            str: Model response content.
        """
        if not self.memory:
            self.memory.append({"role": "system", "content": self.system_prompt})

        self.memory.append({"role": "user", "content": user_prompt})

        try:
            if len(self.memory) > self.max_messages:
                self.summary = self._summarize_memory(self.memory[:-1])

                # Prepare memory for API: system prompt + summary + latest user message
                memory_for_api = [
                    {
                        "role": "system",
                        "content": f"{self.system_prompt}\nConversation summary: {self.summary}",
                    },
                    {"role": "user", "content": user_prompt},
                ]
            else:
                # Use full memory if under max_messages
                memory_for_api = self.memory.copy()

            assistant_response = self._call_api(memory_for_api)
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

    def clear_memory(self):
        """
        Clear session memory and summary.
        """
        self.memory = []
        self.summary = None

    def _call_api(self, messages: list) -> str:
        """
        Internal method to call ChatCompletion API.

        Args:
            messages (list): List of messages (dict with 'role' and 'content').

        Returns:
            str: Model response content.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("OpenAI API call failed: %s", e, exc_info=True)
            raise

    def _summarize_memory(self, memory_to_summarize: list) -> str:
        """
        Generate a summary of old messages to reduce token usage.

        Args:
            memory_to_summarize (list): List of messages to summarize.

        Returns:
            str: Summary text.
        """
        try:
            prompt = self.summary_prompt_template + "\n\n"
            for msg in memory_to_summarize:
                prompt += f"{msg['role']}: {msg['content']}\n"
            summary = self._call_api([{"role": "user", "content": prompt}])
            logger.info("Memory summarized successfully.")
            return summary
        except Exception as e:
            logger.error("Error summarizing memory: %s", e, exc_info=True)
            raise
