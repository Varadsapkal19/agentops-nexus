"""AgentOps Nexus - FastAPI Application Entry Point"""

import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import create_db_and_tables, engine
from app.core.redis_client import redis_client
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.utils.qdrant_setup import initialize_qdrant_collections

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan events."""
    logger.info("Starting AgentOps Nexus API", version=settings.APP_VERSION)
    
    # Initialize database
    await create_db_and_tables()
    logger.info("Database initialized")
    
    # Initialize Redis
    await redis_client.connect()
    logger.info("Redis connected")
    
    # Initialize Qdrant collections
    await initialize_qdrant_collections()
    logger.info("Qdrant collections initialized")
    
    yield
    
    # Shutdown
    await redis_client.disconnect()
    logger.info("AgentOps Nexus API shutting down")


app = FastAPI(
    title="AgentOps Nexus API",
    description="Enterprise AI Governance Platform - REST API",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Include API router
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": time.time(),
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "name": "AgentOps Nexus API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
    }


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url.path)},
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    logger.error("Internal server error", path=str(request.url.path), error=str(exc))
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request.state.request_id if hasattr(request.state, 'request_id') else None},
    )
