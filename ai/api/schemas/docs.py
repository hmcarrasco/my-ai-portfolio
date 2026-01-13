from pydantic import BaseModel, Field


class GenerateDocsRequest(BaseModel):
    """Schema for documentation generation requests."""

    repo: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r"^[a-zA-Z0-9_.-]+$",
        description="Repository name (e.g., 'my-ai-portfolio')",
        examples=["my-ai-portfolio"],
    )


class GenerateDocsResponse(BaseModel):
    """Schema for documentation generation responses."""

    repo: str = Field(..., description="Repository that was documented")
    documentation: dict[str, str] = Field(
        ...,
        description="Generated documentation by type (e.g., {'overview': '...', 'api': '...'})",
    )


class DocTypesResponse(BaseModel):
    """Schema for listing available documentation types."""

    doc_types: list[str] = Field(
        ..., description="List of available documentation types"
    )


class ProjectSchema(BaseModel):
    """Schema for a project."""

    name: str = Field(..., description="Project name")
    repo: str = Field(..., description="Repository name")
    description: str = Field(..., description="Project description")
    doc_types: list[str] = Field(
        ..., description="Available documentation types for this project"
    )


class ProjectsResponse(BaseModel):
    """Schema for listing available projects."""

    projects: list[ProjectSchema] = Field(..., description="List of available projects")
