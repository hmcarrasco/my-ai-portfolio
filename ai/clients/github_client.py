import base64
from typing import Any

import requests

from ai.config.settings import settings
from ai.utils.logger import get_logger

logger = get_logger(__name__)


class GitHubClient:
    def __init__(self, token: str | None = None):
        """
        Initialize GitHub client.

        Args:
            token: GitHub personal access token (optional, increases rate limits).
        """
        self.base_url = settings.github_api_base_url
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_readme(self, repo: str) -> str | None:
        """
        Fetch README content from a repository.

        Args:
            repo: Repository in format 'owner/repo'.

        Returns:
            README content as string, or None if not found.
        """
        url = f"{self.base_url}/repos/{repo}/readme"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            content = data.get("content", "")
            encoding = data.get("encoding", "base64")

            if encoding == "base64" and content:
                return base64.b64decode(content).decode("utf-8")
            return content

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning("README not found for repo: %s", repo)
                return None
            logger.error("HTTP error fetching README for %s: %s", repo, e)
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Request error fetching README for %s: %s", repo, e)
            raise

    def get_repo_structure(self, repo: str, path: str = "") -> list[dict[str, Any]]:
        """
        Fetch repository file/folder structure.

        Args:
            repo: Repository in format 'owner/repo'.
            path: Path within the repository (empty for root).

        Returns:
            List of file/folder entries with name, type, and path.
        """
        url = f"{self.base_url}/repos/{repo}/contents/{path}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            contents = response.json()
            if isinstance(contents, list):
                return [
                    {
                        "name": item["name"],
                        "type": item["type"],
                        "path": item["path"],
                    }
                    for item in contents
                ]
            return []

        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error fetching structure for %s: %s", repo, e)
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Request error fetching structure for %s: %s", repo, e)
            raise

    def get_file_content(self, repo: str, file_path: str) -> str | None:
        """
        Fetch content of a specific file from repository.

        Args:
            repo: Repository in format 'owner/repo'.
            file_path: Path to the file within the repository.

        Returns:
            File content as string, or None if not found.
        """
        url = f"{self.base_url}/repos/{repo}/contents/{file_path}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            content = data.get("content", "")
            encoding = data.get("encoding", "base64")

            if encoding == "base64" and content:
                return base64.b64decode(content).decode("utf-8")
            return content

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning("File not found: %s/%s", repo, file_path)
                return None
            logger.error("HTTP error fetching file %s/%s: %s", repo, file_path, e)
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Request error fetching file %s/%s: %s", repo, file_path, e)
            raise

    def get_repo_info(self, repo: str) -> dict[str, Any]:
        """
        Fetch repository metadata.

        Args:
            repo: Repository in format 'owner/repo'.

        Returns:
            Dictionary with repo info (name, description, language, topics, etc.).
        """
        url = f"{self.base_url}/repos/{repo}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            return {
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "description": data.get("description"),
                "language": data.get("language"),
                "topics": data.get("topics", []),
                "default_branch": data.get("default_branch"),
                "html_url": data.get("html_url"),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
            }

        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error fetching repo info for %s: %s", repo, e)
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Request error fetching repo info for %s: %s", repo, e)
            raise

    def get_languages(self, repo: str) -> dict[str, int]:
        """
        Fetch languages used in repository.

        Args:
            repo: Repository in format 'owner/repo'.

        Returns:
            Dictionary mapping language names to bytes of code.
        """
        url = f"{self.base_url}/repos/{repo}/languages"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error fetching languages for %s: %s", repo, e)
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Request error fetching languages for %s: %s", repo, e)
            raise
