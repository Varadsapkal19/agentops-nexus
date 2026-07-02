"""FastAPI dependencies for authentication and authorization."""

import uuid
from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User, UserStatus
from app.models.api_key import APIKey
from app.models.organization import Organization, OrganizationMember, MemberRole

security = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    api_key: Optional[str] = Security(api_key_header),
) -> User:
    """Get the current authenticated user."""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = None
    
    # Try JWT Bearer token
    if credentials:
        payload = verify_token(credentials.credentials, token_type="access")
        if payload:
            user_id = payload.get("sub")
            if user_id:
                result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
                user = result.scalar_one_or_none()
    
    # Try API Key
    elif api_key:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        result = await db.execute(select(APIKey).where(APIKey.is_active == True))
        api_keys = result.scalars().all()
        
        for key in api_keys:
            if pwd_context.verify(api_key, key.hashed_key):
                result = await db.execute(select(User).where(User.id == key.user_id))
                user = result.scalar_one_or_none()
                break
    
    if not user:
        raise credentials_exception
    
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User account is {user.status}",
        )
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user


class RequireRole:
    def __init__(self, *roles: MemberRole):
        self.required_roles = roles

    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
        organization_id: Optional[str] = None,
    ) -> User:
        if organization_id:
            result = await db.execute(
                select(OrganizationMember).where(
                    OrganizationMember.user_id == current_user.id,
                    OrganizationMember.organization_id == uuid.UUID(organization_id),
                )
            )
            member = result.scalar_one_or_none()
            if not member or member.role not in self.required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )
        return current_user


require_org_admin = RequireRole(MemberRole.OWNER, MemberRole.ADMIN)
require_org_owner = RequireRole(MemberRole.OWNER)
