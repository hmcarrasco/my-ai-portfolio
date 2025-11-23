import openai

from api.utils.loaders import load_yaml


class Openaiclient:
    def __init__(
        self,
        openai_api_key: str,
        prompts_path: str = "api/prompts.yaml",
        model: str = "gpt-4.1",
        temperature: float = 0.2,
        max_messages: int = 10,
    ):
        openai.openai_api_key = openai_api_key
        self.model = model
        self.temperature = temperature
        self.max_messages = max_messages
        self.memory = []
        self.summary = None

        prompts = load_yaml(prompts_path)
        self.system_prompt = prompts.get("chatbot_system_prompt", "")
        self.summary_prompt_template = prompts.get("chatbot_summary_prompt", "")

    def generate_response_with_memory(self, user_message: str) -> str:
        """
        Generate a response considering session memory. If memory exceeds max_messages,
        summarize previous messages to reduce token usage.

        Args:
            user_message (str): User's message.

        Returns:
            str: Model response content.
        """
        if not self.memory:
            self.memory.append({"role": "system", "content": self.system_prompt})

        self.memory.append({"role": "user", "content": user_message})

        if len(self.memory) > self.max_messages:
            self.summary = self._summarize_memory(self.memory[:-1])

            # Prepare memory for API: system prompt + summary + latest user message
            memory_for_api = [
                {
                    "role": "system",
                    "content": f"{self.system_prompt}\nConversation summary: {self.summary}",
                },
                {"role": "user", "content": user_message},
            ]
        else:
            # Use full memory if under max_messages
            memory_for_api = self.memory.copy()

        assistant_response = self._call_api(memory_for_api)
        self.memory.append({"role": "assistant", "content": assistant_response})

        return assistant_response

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
        response = self.openai.ChatCompletion.create(
            model=self.model, messages=messages, temperature=self.temperature
        )
        return response.choices[0].message["content"]

    def _summarize_memory(self, memory_to_summarize: list) -> str:
        """
        Generate a summary of old messages to reduce token usage.

        Args:
            memory_to_summarize (list): List of messages to summarize.

        Returns:
            str: Summary text.
        """
        prompt = self.summary_prompt_template + "\n\n"
        for msg in memory_to_summarize:
            prompt += f"{msg['role']}: {msg['content']}\n"
        summary = self._call_api([{"role": "user", "content": prompt}])

        return summary
