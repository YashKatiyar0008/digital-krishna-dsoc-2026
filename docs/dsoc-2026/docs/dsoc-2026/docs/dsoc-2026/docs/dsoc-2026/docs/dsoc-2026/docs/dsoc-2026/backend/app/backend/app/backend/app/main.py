"""Public FastAPI application for the Digital Krishna DSOC demo.

This sanitized API:

- validates guidance requests,
- returns structured guidance responses,
- exposes a health-check endpoint,
- restricts browser origins,
- avoids logging complete user messages,
- contains no private credentials or model endpoints.
"""

from __future__ import annotations

import logging
import os
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .guidance import generate_guidance
from .schemas import ErrorResponse, GuidanceRequest, GuidanceResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("digital_krishna_api")


DEFAULT_ALLOWED_ORIGINS = [
    "https://www.digitalkrishna.co.in",
    "https://digitalkrishna.co.in",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def get_allowed_origins() -> list[str]:
    """Return allowed frontend origins.

    Additional origins can be supplied through:

    CORS_ORIGINS=https://example.com,https://app.example.com
    """

    configured_origins = os.getenv("CORS_ORIGINS", "").strip()

    if not configured_origins:
        return DEFAULT_ALLOWED_ORIGINS

    return [
        origin.strip().rstrip("/")
        for origin in configured_origins.split(",")
        if origin.strip()
    ]


app = FastAPI(
    title="Digital Krishna AI — Public DSOC API",
    description=(
        "Sanitized demonstration API for structured, multilingual, "
        "Krishna-inspired reflection guidance."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """Return basic public API information."""

    return {
        "name": "Digital Krishna AI Public API",
        "status": "running",
        "documentation": "/docs",
    }


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Health endpoint for local and cloud deployment checks."""

    return {
        "status": "healthy",
        "service": "digital-krishna-guidance-api",
        "version": "1.0.0",
    }


@app.post(
    "/api/guidance",
    response_model=GuidanceResponse,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "The guidance request could not be processed.",
        },
        500: {
            "model": ErrorResponse,
            "description": "An unexpected internal error occurred.",
        },
    },
    tags=["Guidance"],
)
async def create_guidance(
    request: GuidanceRequest,
) -> GuidanceResponse | JSONResponse:
    """Generate one structured guidance response.

    The public implementation uses the deterministic guidance engine.
    It does not contact private AI models or production databases.
    """

    try:
        return generate_guidance(request)

    except ValueError:
        request_id = str(uuid4())

        logger.warning(
            "Guidance request rejected",
            extra={"request_id": request_id},
        )

        error = ErrorResponse(
            error="invalid_guidance_request",
            message=(
                "The request could not be processed. "
                "Please review the message and try again."
            ),
            request_id=request_id,
        )

        return JSONResponse(
            status_code=400,
            content=error.model_dump(),
        )

    except Exception:
        request_id = str(uuid4())

        # Do not log the complete user message.
        logger.exception(
            "Unexpected guidance-generation error",
            extra={
                "request_id": request_id,
                "language": request.language,
            },
        )

        error = ErrorResponse(
            error="guidance_generation_failed",
            message=(
                "Digital Krishna could not prepare guidance at this time. "
                "Please try again shortly."
            ),
            request_id=request_id,
        )

        return JSONResponse(
            status_code=500,
            content=error.model_dump(),
        )
