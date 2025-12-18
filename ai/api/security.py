from fastapi import HTTPException, Header

from ai.config.settings import settings
from ai.utils.logger import get_logger

logger = get_logger(__name__)


def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    Verify the API key from request headers.

    Args:
        x_api_key (str): API key provided in the X-API-Key header.

    Returns:
        str: The API key if valid.

    Raises:
        HTTPException: If the API key is invalid or not configured.
    """
    if not settings.chatbot_api_key:
        logger.error("CHATBOT_API_KEY is not configured")
        raise HTTPException(status_code=500, detail="API Key not configured")

    if x_api_key != settings.chatbot_api_key:
        logger.warning("Invalid API key attempt detected")
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key
