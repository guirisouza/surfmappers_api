import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from apps.helpers.handler import register_exception_handlers
from apps.helpers.schema import HttpValidationError
from apps.router import api_router
from apps.settings import settings
from database.database import engine, Base

APP_ROOT = Path(__file__).parent

Base.metadata.create_all(bind=engine)

# Logger config
logger.remove()
logger.add(
    sys.stderr,
    format="<level>{level: <8}</level>  <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message}",
    level="DEBUG",
    colorize=True,
)


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="app",
        description="Happy Wedding",
        version="0.1",
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json"
    )

    if settings.backend_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.backend_cors_origins],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        @app.middleware("http")
        async def add_headers(request: Request, call_next):
            response = await call_next(request)
            response.headers["access-control-allow-credential"] = "True"
            response.headers["access-control-allow-headers"] = "*"
            response.headers["access-control-allow-origin"] = "*"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = "*"
            response.headers["Access-Control-Allow-Origin"] = "*"
            return response


    app.include_router(
        router=api_router,
        responses={
            422: {
                "description": "Validation Error",
                "model": HttpValidationError,
            },
        },
    )
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )
    register_exception_handlers(app)
    return app