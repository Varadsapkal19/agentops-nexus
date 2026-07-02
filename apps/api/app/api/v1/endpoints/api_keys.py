"""Api_keys API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
async def list_api_keys(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all api_keys."""
    return {"message": "List of api_keys for user", "user_id": str(current_user.id)}

@router.post("/")
async def create_api_key(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new api_key."""
    return {"status": "created", "data": payload}
