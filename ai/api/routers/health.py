from fastapi import APIRouter, Depends

from ai.api.schemas.health import HealthResponse
from ai.api.security import verify_api_key
from ai.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: Health status.
    """
    logger.info("Health check requested")
    return HealthResponse(status="ok")
