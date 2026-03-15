from unittest.mock import MagicMock, patch

import pytest

from ai.clients.doc_generator import DocGenerator, VALID_DOC_TYPES


class TestDocGenerator:
    """Test suite for DocGenerator class."""

    @pytest.fixture
    def mock_github_client(self):
        """Mock GitHub client."""
        client = MagicMock()
        client.get_readme.return_value = "# Test Project\nA sample project"
        client.get_repo_structure.return_value = [
            {"name": "src", "type": "dir", "path": "src"},
            {"name": "main.py", "type": "file", "path": "main.py"},
            {"name": "README.md", "type": "file", "path": "README.md"},
        ]
        client.get_languages.return_value = {"Python": 10000, "JavaScript": 5000}
        client.get_file_content.return_value = "print('hello world')"
        client.get_latest_commit_sha.return_value = "abc123"
        return client

    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client."""
        client = MagicMock()
        client.get_response.return_value = (
            "# Generated Documentation\n\nThis is the generated docs."
        )
        return client

    @pytest.fixture
    def mock_prompts(self):
        """Mock prompts loading."""
        return {
            "doc_generator_system_prompt": "You are a documentation writer.",
            "doc_types": {
                "overview": "Generate an overview.",
                "architecture": "Generate architecture docs.",
                "api": "Generate API docs.",
                "setup": "Generate setup docs.",
                "readme": "Generate a README.",
            },
        }

    @pytest.fixture
    def doc_generator(self, mock_github_client, mock_openai_client, mock_prompts):
        """Create a DocGenerator with mocked dependencies."""
        with patch("ai.clients.doc_generator.load_yaml", return_value=mock_prompts):
            generator = DocGenerator(
                github_client=mock_github_client,
                openai_client=mock_openai_client,
            )
        return generator

    def test_valid_doc_types(self):
        """Test that VALID_DOC_TYPES contains expected types."""
        assert "overview" in VALID_DOC_TYPES
        assert "architecture" in VALID_DOC_TYPES
        assert "api" in VALID_DOC_TYPES
        assert "setup" in VALID_DOC_TYPES
        assert "readme" in VALID_DOC_TYPES

    def test_fetch_repo_context(self, doc_generator, mock_github_client):
        """Test fetching repository context."""
        context = doc_generator.fetch_repo_context("owner/repo")

        assert context["repo"] == "owner/repo"
        assert context["readme"] == "# Test Project\nA sample project"
        assert len(context["structure"]) == 3
        assert context["languages"] == {"Python": 10000, "JavaScript": 5000}
        assert "source_files" in context
        mock_github_client.get_readme.assert_called_once_with("owner/repo")

    def test_fetch_repo_context_handles_errors(self, doc_generator, mock_github_client):
        """Test that fetch_repo_context handles errors gracefully."""
        mock_github_client.get_readme.side_effect = Exception("API Error")
        mock_github_client.get_repo_structure.side_effect = Exception("API Error")
        mock_github_client.get_languages.side_effect = Exception("API Error")

        context = doc_generator.fetch_repo_context("owner/repo")

        assert context["repo"] == "owner/repo"
        assert context["readme"] is None
        assert context["structure"] == []
        assert context["languages"] == {}

    @pytest.mark.parametrize("doc_type", VALID_DOC_TYPES)
    def test_generate_documentation_valid_types(
        self, doc_generator, mock_openai_client, doc_type
    ):
        """Test generating documentation for all valid types."""
        with patch("ai.clients.doc_generator.os.path.exists", return_value=False):
            result = doc_generator.generate_documentation("owner/repo", doc_type)

        assert result == "# Generated Documentation\n\nThis is the generated docs."
        mock_openai_client.get_response.assert_called_once()

    def test_generate_documentation_invalid_type(self, doc_generator):
        """Test that invalid doc_type raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            doc_generator.generate_documentation("owner/repo", "invalid_type")

        assert "Invalid doc_type" in str(exc_info.value)
        assert "invalid_type" in str(exc_info.value)

    def test_generate_documentation_openai_error(
        self, doc_generator, mock_openai_client
    ):
        """Test that OpenAI errors are handled gracefully."""
        mock_openai_client.get_response.side_effect = Exception("OpenAI API Error")

        with patch("ai.clients.doc_generator.os.path.exists", return_value=False):
            result = doc_generator.generate_documentation("owner/repo", "overview")

        # Errors are caught and returned as error message
        assert "[Error generating overview documentation]" in result

    def test_generate_all_returns_cached_false_on_fresh(
        self, doc_generator, mock_openai_client
    ):
        """Test that generate_all_documentation returns cached=False on fresh generation."""
        with patch("ai.clients.doc_generator.os.path.exists", return_value=False):
            docs, cached = doc_generator.generate_all_documentation(
                "owner/repo", ["overview"]
            )
        assert cached is False
        assert "overview" in docs
        mock_openai_client.get_response.assert_called_once()

    def test_generate_all_serves_from_cache(
        self, doc_generator, mock_github_client, mock_openai_client
    ):
        """Test that cached docs are returned when commit SHA matches."""
        cached_data = {
            "commit_sha": "abc123",
            "documentation": {"overview": "# Cached Overview"},
        }
        with patch("ai.clients.doc_generator.os.path.exists", return_value=True):
            with patch(
                "builtins.open",
                new_callable=lambda: lambda *a, **k: __import__('io').StringIO(
                    __import__('json').dumps(cached_data)
                ),
            ):
                docs, cached = doc_generator.generate_all_documentation(
                    "owner/repo", ["overview"]
                )
        assert cached is True
        assert docs["overview"] == "# Cached Overview"
        mock_openai_client.get_response.assert_not_called()

    def test_generate_all_force_regenerate_skips_cache(
        self, doc_generator, mock_openai_client
    ):
        """Test that force_regenerate bypasses cache."""
        with patch("ai.clients.doc_generator.os.path.exists", return_value=False):
            docs, cached = doc_generator.generate_all_documentation(
                "owner/repo", ["overview"], force_regenerate=True
            )
        assert cached is False
        mock_openai_client.get_response.assert_called_once()

    def test_format_structure(self, doc_generator):
        """Test structure formatting."""
        structure = [
            {
                "name": "src",
                "type": "dir",
                "path": "src",
                "children": [
                    {"name": "main.py", "type": "file", "path": "src/main.py"},
                ],
            },
            {"name": "README.md", "type": "file", "path": "README.md"},
        ]

        result = doc_generator._format_structure(structure)

        assert "📁 src" in result
        assert "📄 main.py" in result
        assert "📄 README.md" in result

    def test_build_prompt_includes_context(self, doc_generator):
        """Test that build_prompt includes all context elements."""
        context = {
            "repo": "owner/repo",
            "readme": "# Test README",
            "structure": [{"name": "src", "type": "dir", "path": "src"}],
            "languages": {"Python": 10000},
            "key_files": {"requirements.txt": "fastapi==0.100.0"},
            "source_files": {"main.py": "print('hello')"},
        }

        prompt = doc_generator._build_prompt(context, "Generate overview.")

        assert "owner/repo" in prompt
        assert "Generate overview." in prompt
        assert "Python" in prompt
        assert "# Test README" in prompt
        assert "requirements.txt" in prompt
        assert "main.py" in prompt
        assert "print('hello')" in prompt

    def test_is_source_file(self, doc_generator):
        """Test source file detection."""
        assert doc_generator._is_source_file("main.py") is True
        assert doc_generator._is_source_file("app.js") is True
        assert doc_generator._is_source_file("README.md") is False
        assert doc_generator._is_source_file("config.yaml") is False
        assert doc_generator._is_source_file("index.ts") is True

    def test_get_language_for_file(self, doc_generator):
        """Test language detection for syntax highlighting."""
        assert doc_generator._get_language_for_file("main.py") == "python"
        assert doc_generator._get_language_for_file("app.js") == "javascript"
        assert doc_generator._get_language_for_file("index.ts") == "typescript"
        assert doc_generator._get_language_for_file("README.md") == ""

    def test_fetch_source_files(self, doc_generator, mock_github_client):
        """Test fetching source code files."""
        file_paths = ["main.py", "utils.py"]

        result = doc_generator._fetch_source_files("owner/repo", file_paths)

        assert "main.py" in result
        assert result["main.py"] == "print('hello world')"
