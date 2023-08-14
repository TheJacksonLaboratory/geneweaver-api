"""A module to keep track of injectable dependencies for FastAPI endpoints.
- https://fastapi.tiangolo.com/tutorial/dependencies/
"""
from geneweaver.api.core.config import settings
from geneweaver.api.core.security import Auth0

auth = Auth0(
    domain=settings.AUTH_DOMAIN,
    api_audience=settings.AUTH_AUDIENCE,
    scopes=settings.AUTH_SCOPES,
    auto_error=False,
)
