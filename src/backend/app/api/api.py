from fastapi import APIRouter

from app.api.endpoints import (
    batch,
    document,
    finding,
    health,
    project,
    rule,
    statistics,
    user,
)

router = APIRouter()
router.include_router(document.router, prefix="/document", tags=["Document"])
router.include_router(
    finding.router, prefix="/finding", tags=["Resultaten"], include_in_schema=False
)
router.include_router(rule.router, prefix="/rule", tags=["Regels"])
router.include_router(
    statistics.router,
    prefix="/statistics",
    tags=["Statistiek"],
    include_in_schema=False,
)
router.include_router(
    batch.router, prefix="/batch", tags=["Batch"], include_in_schema=False
)
router.include_router(
    user.router, prefix="/user", tags=["Gebruiker"], include_in_schema=False
)
router.include_router(
    health.router,
    prefix="/health",
    tags=["Healthcheck"],
    include_in_schema=False,
)
router.include_router(
    project.router,
    prefix="/project",
    tags=["Projectnummers"],
    include_in_schema=False,
)
