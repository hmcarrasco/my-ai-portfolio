import json
from typing import Any

import yaml

from ai.utils.logger import get_logger


logger = get_logger(__name__)


def load_yaml(file_path: str) -> Any:
    """
    Load a YAML file and return its contents.

    Args:
        file_path (str): Path to the YAML file.
    Returns:
        Any: Parsed YAML content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        logger.error("YAML file not found: %s", file_path)
        raise FileNotFoundError(f"YAML file not found: {file_path}") from e
    except (OSError, yaml.YAMLError) as e:
        logger.error("Failed to load YAML file %s: %s", file_path, e, exc_info=True)
        raise RuntimeError(f"Failed to load YAML file: {file_path}") from e


def load_json(file_path: str) -> Any:
    """
    Load a JSON file and return its contents.

    Args:
        file_path (str): Path to the JSON file.
    Returns:
        Any: Parsed JSON content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as e:
        logger.error("JSON file not found: %s", file_path)
        raise FileNotFoundError(f"JSON file not found: {file_path}") from e
    except (OSError, json.JSONDecodeError) as e:
        logger.error("Failed to load JSON file %s: %s", file_path, e, exc_info=True)
        raise RuntimeError(f"Failed to load JSON file: {file_path}") from e
