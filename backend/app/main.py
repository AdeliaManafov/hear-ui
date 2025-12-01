import logging
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.core.model_wrapper import ModelWrapper

logger = logging.getLogger(__name__)

# Initialize model wrapper globally so routes can access it
model_wrapper = ModelWrapper()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    try:
        model_wrapper.load()
        app.state.model_wrapper = model_wrapper
    except FileNotFoundError:
        # Model not present in the environment; keep the attribute for consistency
        app.state.model_wrapper = model_wrapper
    except Exception:
        # In case of other errors, still expose the wrapper (it will raise on use)
        app.state.model_wrapper = model_wrapper
    
    yield
    
    # Shutdown (nothing to clean up currently)


def custom_generate_unique_id(route: APIRoute) -> str:
    # Some routes may not define `tags`; fall back to a stable default
    try:
        tag = route.tags[0] if route.tags and len(route.tags) > 0 else "default"
    except Exception:
        tag = "default"
    return f"{tag}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler that logs the full traceback and returns a 500.

    This ensures unhandled exceptions (including those raised during dependency
    injection or validation) are written to the application logs so they can be
    inspected from `docker-compose logs`.
    """
    logger.exception("Unhandled exception while processing request %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
