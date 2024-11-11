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
    poller,
    process_requests,
)

router = APIRouter()
router.include_router(document.router, prefix="/document", tags=["Document"])
router.include_router(finding.router, prefix="/finding", tags=["Resultaten"])
router.include_router(rule.router, prefix="/rule", tags=["Regels"])
router.include_router(statistics.router, prefix="/statistics", tags=["Statistiek"])
router.include_router(batch.router, prefix="/batch", tags=["Batch"])
router.include_router(user.router, prefix="/user", tags=["Gebruiker"])
router.include_router(health.router, prefix="/health", tags=["Healthcheck"])
router.include_router(project.router, prefix="/project", tags=["Projectnummers"])
router.include_router(
    process_requests.router, prefix="/process-requests", tags=["Process Requests"]
)

poller_router = APIRouter()
poller_router.include_router(poller.router, tags=["Poller"])
