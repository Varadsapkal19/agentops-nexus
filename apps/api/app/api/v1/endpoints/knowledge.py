"""Knowledge API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
async def list_knowledge(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all knowledge."""
    return {"message": "List of knowledge for user", "user_id": str(current_user.id)}

@router.post("/")
async def create_knowledge(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new knowledge."""
    return {"status": "created", "data": payload}
