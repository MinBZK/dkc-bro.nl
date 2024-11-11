import logging.config
from os import path

import secure
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.cors import CORSMiddleware

from app import crud
from app.database.database import SessionLocal
from app.expert.expert_base import ExpertBase
from scripts.create_and_assign_rws import main_assign_resources_to_rws
from scripts.create_rws_org_rules import main_create_rws_org_rules

API_DESCRIPTION = (
    "Met deze API is het mogelijk om volledig geautomatiseerd brondocumenten aan te leveren aan het DKC- BRO. "
    "De API is RESTful opgezet met als doel het valideren van XML-bestanden en het ophalen "
    "van de kwaliteitsregels die erop worden losgelaten. De API is specifiek ontworpen voor het valideren van XML-documenten "
    "en maakt gebruik van HTTP-methoden en URI's voor het uitwisselen van gegevens. De API retourneert de gevalideerde XML-bestanden "
    "samen met de kwaliteitsregels in de vorm van JSON- of XML-documenten, zodat deze gemakkelijk kunnen worden geïntegreerd in andere "
    "applicaties en systemen."
)


def create_app(expert_class: ExpertBase):
    global expert
    expert = expert_class

    # Setup logging and initialize logger for main
    log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
    logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    secure_headers = secure.Secure()

    logger.info("Creating app.")
    global limiter
    limiter = Limiter(key_func=get_remote_address)
    app = FastAPI(
        title="DKC-BRO Expert-service", description=API_DESCRIPTION, redoc_url=None
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    logger.info("Adding middlewares.")
    app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )

    logger.info("Adding API router.")
    from app.api.api import router as api_router
    from app.api.api import poller_router as poller_api_router

    app.include_router(api_router, prefix="/api")
    app.include_router(poller_api_router, prefix="/polling-api")

    @app.middleware("http")
    async def set_secure_headers(request, call_next):
        """
        Middleware that adds security headers to each request.
        """
        response = await call_next(request)
        secure_headers.framework.fastapi(response)
        return response

    # sync rules as defined in expert class to database
    db = SessionLocal()
    crud.rule.add_new_rules(db=db, expert_class=expert)
    main_assign_resources_to_rws()
    main_create_rws_org_rules()
    db.close()

    return app
