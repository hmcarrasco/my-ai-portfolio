from typing import Any, Optional

from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from ai.clients.openai_client import OpenaiClient
from ai.utils.logger import get_logger

logger = get_logger(__name__)


class RAGService:
    def __init__(
        self,
        openai_client: OpenaiClient,
        openai_api_key: str,
        chroma_collection: str = "docs",
        persist_path: str = "./ai/chroma_db",
        embedding_model: str = "text-embedding-3-small",
    ):
        self.chroma = PersistentClient(path=persist_path)

        # Use OpenAI embeddings for semantic search
        self.embedding_function = OpenAIEmbeddingFunction(
            api_key=openai_api_key,
            model_name=embedding_model,
        )
        logger.info("Using OpenAI embedding model: %s", embedding_model)

        self.collection = self.chroma.get_or_create_collection(
            name=chroma_collection,
            embedding_function=self.embedding_function,
        )
        self.openai_client = openai_client

    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Add a document to the ChromaDB collection.

        Args:
            doc_id (str): Unique document identifier.
            content (str): Document text/content.
            metadata (dict, optional): Additional metadata for the document.
        """
        metadatas: dict[str, Any] = metadata if metadata else {"source": "ingest"}
        self.collection.add(documents=[content], ids=[doc_id], metadatas=[metadatas])
        logger.info("Document added to ChromaDB: %s", doc_id)

    def retrieve(self, query: str, n_results: int = 3) -> list[str]:
        """
        Retrieve top-n relevant documents from ChromaDB.

        Args:
            query (str): Query text for retrieval.
            n_results (int): Number of documents to retrieve.

        Returns:
            list: List of retrieved document contents.
        """
        results = self.collection.query(query_texts=[query], n_results=n_results)
        docs = [doc for doc in results["documents"][0]]
        logger.info("Retrieved %d docs from ChromaDB for query: %s", len(docs), query)
        return docs

    def answer_with_rag(self, user_query: str) -> str:
        """
        Retrieve relevant documents and generate an answer using OpenaiClient.

        Args:
            user_query (str): The user's question.

        Returns:
            str: The generated answer from the LLM.
        """
        docs = self.retrieve(user_query)
        context = "\n".join(docs)
        prompt = f"Context:\n{context}\n\nQuestion: {user_query}\nAnswer:"
        logger.info("Sending RAG prompt to OpenAI.")
        return self.openai_client.get_response(prompt)
