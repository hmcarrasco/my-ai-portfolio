from typing import List


class TextChunker:
    def __init__(self, chunk_size: int = 256, overlap: int = 20):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text (str): The input text.

        Returns:
            List[str]: List of text chunks.
        """
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap
        return chunks

    def chunk_file(self, file_path: str) -> List[str]:
        """
        Read a text file and split its content into chunks.

        Args:
            file_path (str): Path to the text file.

        Returns:
            List[str]: List of text chunks.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return self.chunk_text(text)
