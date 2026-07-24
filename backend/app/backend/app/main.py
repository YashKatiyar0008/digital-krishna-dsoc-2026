"""Public FastAPI application for the Digital Krishna DSOC demo.

This sanitized API:

- validates guidance requests,
- returns structured guidance responses,
- exposes health-check endpoints,
- restricts allowed browser origins,
- contains no private credentials or model endpoints.
"""

from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .guidance import generate_guidance
from .schemas import GuidanceRequest, GuidanceResponse


DEFAULT_ALLOWED_ORIGINS = [
    "https://www.digitalkrishna.co.in",
    "https://digitalkrishna.co.in",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


def get_allowed_origins() -> list[str]:
    """Return browser origins allowed to call the public API."""

    configured_origins = os.getenv("CORS_ORIGINS", "").strip()

    if not configured_origins:
        return DEFAULT_ALLOWED_ORIGINS

    return [
        origin.strip().rstrip("/")
        for origin in configured_origins.split(",")
        if origin.strip()
    ]


app = FastAPI(
    title="Digital Krishna AI — DSOC Public API",
    description=(
        "Sanitized demonstration API for structured multilingual "
        "reflection guidance."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)


@app.get("/")
async def root() -> dict[str, str]:
    """Return basic API information."""

    return {
        "name": "Digital Krishna AI Public API",
        "status": "running",
        "documentation": "/docs",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return service health information."""

    return {
        "status": "healthy",
        "service": "digital-krishna-guidance-api",
        "version": "1.0.0",
    }


@app.post(
    "/api/guidance",
    response_model=GuidanceResponse,
)
async def create_guidance(
    request: GuidanceRequest,
) -> GuidanceResponse:
    """Generate one structured guidance response.

    The public implementation uses a deterministic demonstration
    engine and does not contact private AI models or databases.
    """

    return generate_guidance(request)
