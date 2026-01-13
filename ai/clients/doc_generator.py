from typing import Any

from ai.clients.github_client import GitHubClient
from ai.clients.openai_client import OpenaiClient
from ai.config.settings import settings
from ai.utils.loaders import load_yaml
from ai.utils.logger import get_logger

logger = get_logger(__name__)

VALID_DOC_TYPES = ["overview", "architecture", "api", "setup", "readme"]


class DocGenerator:
    """
    Documentation generator that fetches repository information from GitHub
    and uses OpenAI to generate various types of documentation.
    """

    def __init__(
        self,
        github_client: GitHubClient | None = None,
        openai_client: OpenaiClient | None = None,
    ):
        """
        Initialize the documentation generator.

        Args:
            github_client: GitHub client instance.
            openai_client: OpenAI client instance.
        """
        self.github_client = github_client or GitHubClient(token=settings.github_token)

        prompts = load_yaml(settings.doc_generator_prompts_path)
        self.system_prompt = prompts.get("doc_generator_system_prompt", "")
        self.doc_type_prompts = prompts.get("doc_types", {})

        self.openai_client = openai_client or OpenaiClient(
            openai_api_key=settings.openai_api_key,
            model=settings.openai_model,
            system_prompt=self.system_prompt,
            temperature=0.3,
        )

    def fetch_repo_context(self, repo: str) -> dict[str, Any]:
        """
        Fetch comprehensive context about a repository.

        Args:
            repo: Repository in format 'owner/repo'.

        Returns:
            Dictionary containing repo information, structure, README, and key files.
        """
        logger.info("Fetching repository context for: %s", repo)

        context: dict[str, Any] = {
            "repo": repo,
            "readme": None,
            "structure": [],
            "languages": {},
            "key_files": {},
            "source_files": {},
        }

        # Fetch README
        try:
            context["readme"] = self.github_client.get_readme(repo)
            logger.info("Fetched README for %s", repo)
        except Exception as e:
            logger.warning("Could not fetch README for %s: %s", repo, e)

        # Fetch repository structure and collect source file paths
        source_file_paths: list[str] = []
        try:
            context["structure"] = self._fetch_structure_recursive(
                repo, "", depth=3, source_file_paths=source_file_paths
            )
            logger.info("Fetched structure for %s", repo)
        except Exception as e:
            logger.warning("Could not fetch structure for %s: %s", repo, e)

        # Fetch languages
        try:
            context["languages"] = self.github_client.get_languages(repo)
            logger.info("Fetched languages for %s", repo)
        except Exception as e:
            logger.warning("Could not fetch languages for %s: %s", repo, e)

        # Fetch all source code files
        context["source_files"] = self._fetch_source_files(repo, source_file_paths)

        # Fetch key configuration files
        key_files = [
            "requirements.txt",
            "package.json",
            "pyproject.toml",
            "Dockerfile",
            "docker-compose.yml",
            "Makefile",
            ".env.template",
        ]

        for file_path in key_files:
            try:
                content = self.github_client.get_file_content(repo, file_path)
                if content:
                    context["key_files"][file_path] = content
                    logger.info("Fetched %s for %s", file_path, repo)
            except Exception:
                pass

        return context

    def _fetch_structure_recursive(
        self,
        repo: str,
        path: str,
        depth: int,
        source_file_paths: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Recursively fetch repository structure up to a certain depth.
        Also collects paths of source code files for later fetching.

        Args:
            repo: Repository in format 'owner/repo'.
            path: Current path within the repository.
            depth: Remaining depth to traverse.
            source_file_paths: List to collect source file paths (mutated in place).

        Returns:
            List of file/folder entries with nested children.
        """
        if depth <= 0:
            return []

        items = self.github_client.get_repo_structure(repo, path)
        result = []

        for item in items:
            if item["name"].startswith(".") and item["name"] not in [
                ".env.template",
                ".env.example",
            ]:
                continue

            if item["name"] in [
                "node_modules",
                "__pycache__",
                ".git",
                "venv",
                ".venv",
                "tests",
                "test",
            ]:
                continue

            entry = {
                "name": item["name"],
                "type": item["type"],
                "path": item["path"],
            }

            # Collect source file paths
            if item["type"] == "file" and source_file_paths is not None:
                if self._is_source_file(item["name"]):
                    source_file_paths.append(item["path"])

            # Recursively fetch subdirectories
            if item["type"] == "dir" and depth > 1:
                entry["children"] = self._fetch_structure_recursive(
                    repo, item["path"], depth - 1, source_file_paths
                )

            result.append(entry)

        return result

    def _is_source_file(self, filename: str) -> bool:
        """
        Check if a file is a source code file based on extension.

        Args:
            filename: Name of the file.

        Returns:
            True if it's a source code file.
        """
        for ext in settings.source_code_extensions:
            if filename.endswith(ext):
                return True
        return False

    def _fetch_source_files(self, repo: str, file_paths: list[str]) -> dict[str, str]:
        """
        Fetch content of source code files, respecting size limits.

        Args:
            repo: Repository in format 'owner/repo'.
            file_paths: List of file paths to fetch.

        Returns:
            Dictionary mapping file paths to their content.
        """
        source_files: dict[str, str] = {}
        total_chars = 0

        for file_path in file_paths:
            if total_chars >= settings.max_source_code_chars:
                logger.warning(
                    "Reached max source code limit (%d chars), skipping remaining files",
                    settings.max_source_code_chars,
                )
                break

            try:
                content = self.github_client.get_file_content(repo, file_path)
                if content:
                    # Truncate individual files if too large
                    if len(content) > settings.max_file_chars:
                        content = (
                            content[: settings.max_file_chars] + "\n# ... (truncated)"
                        )
                        logger.info("Truncated large file: %s", file_path)

                    # Check if adding this file would exceed total limit
                    if total_chars + len(content) > settings.max_source_code_chars:
                        remaining = settings.max_source_code_chars - total_chars
                        content = content[:remaining] + "\n# ... (truncated)"

                    source_files[file_path] = content
                    total_chars += len(content)
                    logger.info(
                        "Fetched source file: %s (%d chars)", file_path, len(content)
                    )
            except Exception as e:
                logger.warning("Could not fetch source file %s: %s", file_path, e)

        logger.info(
            "Fetched %d source files, total %d chars", len(source_files), total_chars
        )
        return source_files

    def _get_full_repo(self, repo: str) -> str:
        """
        Build full repository path with owner.

        Args:
            repo: Repository name (e.g., 'my-ai-portfolio').

        Returns:
            Full repo path (e.g., 'hmcarrasco/my-ai-portfolio').
        """
        return f"{settings.github_owner}/{repo}"

    def generate_all_documentation(
        self, repo: str, doc_types: list[str]
    ) -> dict[str, str]:
        """
        Generate all documentation types for a repository.
        Fetches context once and generates each doc type.

        Args:
            repo: Repository name (e.g., 'my-ai-portfolio').
            doc_types: List of documentation types to generate.

        Returns:
            Dictionary mapping doc_type to generated documentation.

        Raises:
            ValueError: If any doc_type is not valid.
        """
        for doc_type in doc_types:
            if doc_type not in VALID_DOC_TYPES:
                raise ValueError(
                    f"Invalid doc_type '{doc_type}'. Must be one of: {VALID_DOC_TYPES}"
                )

        full_repo = self._get_full_repo(repo)
        logger.info("Generating documentation for %s, types: %s", full_repo, doc_types)

        context = self.fetch_repo_context(full_repo)

        documentation: dict[str, str] = {}
        for doc_type in doc_types:
            logger.info("Generating %s documentation for %s", doc_type, full_repo)
            try:
                doc_type_prompt = self.doc_type_prompts.get(doc_type, "")
                prompt = self._build_prompt(context, doc_type_prompt)
                doc_content = self.openai_client.get_response(prompt)
                documentation[doc_type] = doc_content
                logger.info(
                    "Successfully generated %s documentation for %s",
                    doc_type,
                    full_repo,
                )
            except Exception as e:
                logger.error(
                    "Failed to generate %s documentation for %s: %s",
                    doc_type,
                    full_repo,
                    e,
                )
                documentation[doc_type] = f"[Error generating {doc_type} documentation]"

        return documentation

    def generate_documentation(self, repo: str, doc_type: str) -> str:
        """
        Generate single documentation type for a repository.

        Args:
            repo: Repository name.
            doc_type: Type of documentation to generate
                      (overview, architecture, api, setup, readme).

        Returns:
            Generated documentation as Markdown string.

        Raises:
            ValueError: If doc_type is not valid.
        """
        result = self.generate_all_documentation(repo, [doc_type])
        return result[doc_type]

    def _build_prompt(self, context: dict[str, Any], doc_type_prompt: str) -> str:
        """
        Build the prompt for documentation generation.

        Args:
            context: Repository context dictionary.
            doc_type_prompt: Specific prompt for the documentation type.

        Returns:
            Complete prompt string.
        """
        prompt_parts = [
            f"# Repository: {context['repo']}\n",
            doc_type_prompt,
            "\n## Repository Information:\n",
        ]

        # Add languages
        if context["languages"]:
            total_bytes = sum(context["languages"].values())
            lang_percentages = {
                lang: f"{(bytes_count / total_bytes * 100):.1f}%"
                for lang, bytes_count in context["languages"].items()
            }
            prompt_parts.append(f"### Languages:\n{lang_percentages}\n")

        # Add structure
        if context["structure"]:
            structure_str = self._format_structure(context["structure"])
            prompt_parts.append(f"### Project Structure:\n```\n{structure_str}```\n")

        # Add README content
        if context["readme"]:
            readme = (
                context["readme"][:4000]
                if len(context["readme"]) > 4000
                else context["readme"]
            )
            prompt_parts.append(f"### Existing README:\n{readme}\n")

        # Add key files
        if context["key_files"]:
            prompt_parts.append("### Key Configuration Files:\n")
            for file_name, content in context["key_files"].items():
                truncated = content[:2000] if len(content) > 2000 else content
                prompt_parts.append(f"#### {file_name}:\n```\n{truncated}\n```\n")

        # Add source code files
        if context.get("source_files"):
            prompt_parts.append("### Source Code Files:\n")
            for file_path, content in context["source_files"].items():
                lang = self._get_language_for_file(file_path)
                prompt_parts.append(f"#### {file_path}:\n```{lang}\n{content}\n```\n")

        prompt_parts.append(
            "\n---\nBased on the above repository information, generate the requested documentation."
        )

        return "\n".join(prompt_parts)

    def _get_language_for_file(self, file_path: str) -> str:
        """
        Get the language identifier for syntax highlighting based on file extension.

        Args:
            file_path: Path to the file.

        Returns:
            Language identifier string.
        """
        extension_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
        }

        for ext, lang in extension_map.items():
            if file_path.endswith(ext):
                return lang
        return ""

    def _format_structure(
        self, structure: list[dict[str, Any]], indent: int = 0
    ) -> str:
        """
        Format the repository structure as a tree string.

        Args:
            structure: List of structure entries.
            indent: Current indentation level.

        Returns:
            Formatted tree string.
        """
        lines = []
        for item in structure:
            prefix = "  " * indent
            icon = "📁" if item["type"] == "dir" else "📄"
            lines.append(f"{prefix}{icon} {item['name']}")

            if "children" in item and item["children"]:
                lines.append(self._format_structure(item["children"], indent + 1))

        return "\n".join(lines)
