"""The root API definition for the GeneWeaver API.

This file defines the root API for the GeneWeaver API. It is responsible for
defining the FastAPI application and including all other API routers.
"""

from fastapi import APIRouter, FastAPI, Security
from geneweaver.api import __version__
from geneweaver.api import dependencies as deps
from geneweaver.api.controller import genes, genesets, publications, species
from geneweaver.api.core.config import settings

app = FastAPI(
    title="GeneWeaver API",
    version=__version__,
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    swagger_ui_oauth2_redirect_url=f"{settings.API_PREFIX}/docs/oauth2-redirect",
    swagger_ui_init_oauth={"clientId": settings.AUTH_CLIENT_ID},
    lifespan=deps.lifespan,
)

api_router = APIRouter(
    dependencies=[
        Security(deps.auth.implicit_scheme),
    ],
)
api_router.include_router(genesets.router)
api_router.include_router(genes.router)
api_router.include_router(publications.router)
api_router.include_router(species.router)

app.include_router(api_router, prefix=settings.API_PREFIX)
