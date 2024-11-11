import logging.config
from pathlib import Path

import secure
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import healthcheck_router, rule_router

# App initialization
parent_dir = Path(__file__).resolve().parent
logging.config.fileConfig(parent_dir / "logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI(
    docs_url="/docs",
    title="Expert Service Processor API",
    version="0.1.0",
    redoc_url=None,
)


# Routers
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

router = APIRouter(prefix="/api")
router.include_router(healthcheck_router, prefix="/health")
router.include_router(rule_router, prefix="/rule", tags=["Rule"])
app.include_router(router)


# Security headers
secure_headers = secure.Secure()


@app.middleware("http")
async def set_secure_headers(request, call_next):
    """
    Middleware that adds security headers to each request.
    """
    response = await call_next(request)
    secure_headers.framework.fastapi(response)
    return response
