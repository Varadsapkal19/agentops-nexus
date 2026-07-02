"""Agent_runs API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User

router = APIRouter()

@router.get("/")
async def list_agent_runs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all agent_runs."""
    return {"message": "List of agent_runs for user", "user_id": str(current_user.id)}

@router.post("/")
async def create_agent_run(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new agent_run."""
    return {"status": "created", "data": payload}
