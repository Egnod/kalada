from fastapi import FastAPI
from starlette.middleware import cors

from kalada import __project__
from kalada.components.routes import api_router
from kalada.core.config.common import ALLOWED_ORIGINS
from kalada.core.config.env import IS_PRODUCTION
from kalada.core.utils.json import CustomJSONResponse


def create_app() -> FastAPI:
    docs_config = {"redoc_url": "/api/docs/", "openapi_url": "/api/docs/openapi.json"} if not IS_PRODUCTION else {}

    app = FastAPI(
        title=__project__,
        **docs_config,
    )

    #########
    # Routes
    ##########

    app.include_router(api_router, prefix="/api", default_response_class=CustomJSONResponse)

    ##########
    # Middlewares
    ##########

    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
