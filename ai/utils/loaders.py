import yaml
import json


def load_yaml(file_path: str) -> dict:
    """
    Load a YAML file and return its contents as a dictionary.

    Args:
        file_path (str): Path to the YAML file.
    Returns:
        dict: Contents of the YAML file.
    """
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def load_json(file_path: str) -> dict:
    """
    Load a JSON file and return its contents as a dictionary.

    Args:
        file_path (str): Path to the JSON file.
    Returns:
        dict: Contents of the JSON file.
    """
    with open(file_path, "r") as file:
        return json.load(file)
