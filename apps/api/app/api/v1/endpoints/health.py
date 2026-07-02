"""Health check endpoint."""

from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/")
async def health():
    return {
        "status": "healthy",
        "timestamp": time.time()
    }
