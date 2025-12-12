from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Schema for health check responses."""

    status: str
