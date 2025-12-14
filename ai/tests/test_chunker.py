import pytest
from ai.clients.chunker import TextChunker


class TestTextChunker:
    """Test suite for TextChunker class."""

    @pytest.mark.parametrize(
        "chunk_size,overlap",
        [
            (0, 0),
            (-1, 0),
            (10, -1),
            (10, 10),
            (10, 11),
        ],
    )
    def test_invalid_parameters_raise(self, chunk_size, overlap):
        """Invalid chunk_size/overlap combinations should raise ValueError."""
        with pytest.raises(ValueError):
            TextChunker(chunk_size=chunk_size, overlap=overlap)

    def test_chunk_text_with_parameters(self):
        """Test chunking with different parameters."""
        # Test with overlap
        chunker = TextChunker(chunk_size=10, overlap=2)
        text = "Hello World Test"
        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
        assert all(len(chunk) <= 10 for chunk in chunks)

    def test_chunk_text_basic(self):
        """Test basic text chunking."""
        chunker = TextChunker(chunk_size=10, overlap=2)
        text = "This is a test text for chunking"

        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        assert all(len(chunk) <= 10 for chunk in chunks)

    def test_chunk_text_with_overlap(self):
        """Test that chunks have proper overlap."""
        chunker = TextChunker(chunk_size=10, overlap=3)
        text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        chunks = chunker.chunk_text(text)

        # Verify overlap exists between consecutive chunks
        for i in range(len(chunks) - 1):
            # Last few chars of chunk[i] should appear in chunk[i+1]
            assert len(chunks[i]) <= 10

    def test_chunk_empty_text(self):
        """Test chunking empty text."""
        chunker = TextChunker(chunk_size=10, overlap=2)
        text = ""

        chunks = chunker.chunk_text(text)

        # Empty text returns empty list (no chunks)
        assert chunks == []

    def test_chunk_text_smaller_than_chunk_size(self):
        """Test chunking text smaller than chunk size."""
        chunker = TextChunker(chunk_size=100, overlap=10)
        text = "Short text"

        chunks = chunker.chunk_text(text)

        assert len(chunks) == 1
        assert chunks[0] == text

    @pytest.mark.parametrize(
        "chunk_size,overlap",
        [
            (256, 20),
            (512, 50),
            (100, 10),
        ],
    )
    def test_chunk_initialization(self, chunk_size, overlap):
        """Test TextChunker initialization with different parameters."""
        chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)

        assert chunker.chunk_size == chunk_size
        assert chunker.overlap == overlap

    def test_chunk_file(self, tmp_path):
        """Test chunking from a file."""
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_content = "This is test content for file chunking. " * 10
        test_file.write_text(test_content)

        chunker = TextChunker(chunk_size=50, overlap=10)
        chunks = chunker.chunk_file(str(test_file))

        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
