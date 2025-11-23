import os
from dotenv import load_dotenv
from api.clients.openai_client import OpenaiClient


def main():
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../cfg/.env"))
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY não encontrada no .env!")
    client = OpenaiClient(openai_api_key=openai_api_key)
    pergunta = "Qual é a capital de Portugal?"
    resposta = client.generate_response_with_memory(pergunta)
    print("Resposta:", resposta)


if __name__ == "__main__":
    main()
