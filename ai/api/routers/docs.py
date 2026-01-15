from fastapi import APIRouter, Depends, HTTPException, Request

from ai.api.main import limiter
from ai.api.schemas.docs import (
    GenerateDocsRequest,
    GenerateDocsResponse,
    DocTypesResponse,
    ProjectsResponse,
)
from ai.api.security import verify_api_key
from ai.clients.doc_generator import DocGenerator, VALID_DOC_TYPES
from ai.config.settings import settings
from ai.utils.loaders import load_yaml
from ai.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/docs", tags=["documentation"])


def get_doc_generator() -> DocGenerator:
    """
    Dependency to get DocGenerator instance.

    Returns:
        DocGenerator: Initialized documentation generator.
    """
    return DocGenerator()


def get_projects() -> list[dict]:
    """
    Load projects from projects.yaml.

    Returns:
        List of project configurations.
    """
    data = load_yaml(settings.projects_path)
    return data.get("projects", [])


@router.get(
    "/projects",
    response_model=ProjectsResponse,
    dependencies=[Depends(verify_api_key)],
    summary="List available projects",
)
def list_projects() -> ProjectsResponse:
    """
    Get the list of available projects that can have documentation generated.

    Returns:
        ProjectsResponse: List of projects with their details.
    """
    projects = get_projects()
    return ProjectsResponse(projects=projects)


@router.get(
    "/types",
    response_model=DocTypesResponse,
    dependencies=[Depends(verify_api_key)],
    summary="List available documentation types",
)
def list_doc_types() -> DocTypesResponse:
    """
    Get the list of available documentation types that can be generated.

    Returns:
        DocTypesResponse: List of valid documentation types.
    """
    return DocTypesResponse(doc_types=VALID_DOC_TYPES)


@router.post(
    "/generate",
    response_model=GenerateDocsResponse,
    dependencies=[Depends(verify_api_key)],
    summary="Generate documentation for a repository",
)
@limiter.limit("3/day")
def generate_documentation(
    request: Request,
    req: GenerateDocsRequest,
    doc_generator: DocGenerator = Depends(get_doc_generator),
) -> GenerateDocsResponse:
    """
    Generate all documentation for a GitHub repository based on projects.yaml.

    Args:
        req (GenerateDocsRequest): Repository name.
        doc_generator (DocGenerator): Documentation generator instance (auto-injected).

    Returns:
        GenerateDocsResponse: Generated documentation for all doc types.

    Raises:
        HTTPException: If repo not found or documentation generation fails.
    """
    projects = get_projects()
    project = next((p for p in projects if p["repo"] == req.repo), None)

    if not project:
        logger.warning("Repository not found in projects.yaml: %s", req.repo)
        raise HTTPException(
            status_code=404,
            detail=f"Repository '{req.repo}' not found in projects.yaml",
        )

    doc_types = project.get("doc_types", [])
    logger.info("Generating documentation for repo: %s, types: %s", req.repo, doc_types)

    try:
        documentation = doc_generator.generate_all_documentation(
            repo=req.repo,
            doc_types=doc_types,
        )

        logger.info(
            "Successfully generated %d documentation types for %s",
            len(documentation),
            req.repo,
        )

        return GenerateDocsResponse(
            repo=req.repo,
            documentation=documentation,
        )

    except ValueError as e:
        logger.warning("Invalid request for %s: %s", req.repo, e)
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            "Error generating documentation for %s: %s", req.repo, e, exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate documentation: {type(e).__name__}",
        )
