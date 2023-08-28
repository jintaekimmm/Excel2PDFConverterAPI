import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import converter


def create_app() -> FastAPI:
    openapi_url = "/openapi.json"

    app = FastAPI(
        openapi_url=openapi_url,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )

    initial_route(app)
    initial_middlewares(app)
    default_routes(app)

    return app


def initial_route(app: FastAPI) -> None:
    """Routes Initializing"""
    app.include_router(converter.router)


def initial_middlewares(app: FastAPI) -> None:
    """Middleware Initializing"""
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )


def default_routes(app: FastAPI) -> None:
    """Set Default Routes"""

    @app.get("/")
    async def root():
        return {"message": "ok"}

    @app.get("/health")
    async def health_check():
        return {"message": "ok"}
