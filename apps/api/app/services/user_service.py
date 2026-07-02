"""User service - business logic for user operations."""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import AuthProvider, User, UserStatus


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        full_name: str,
        password: Optional[str] = None,
        oauth_id: Optional[str] = None,
        auth_provider: AuthProvider = AuthProvider.EMAIL,
        avatar_url: Optional[str] = None,
    ) -> User:
        user = User(
            email=email,
            full_name=full_name,
            auth_provider=auth_provider,
            oauth_id=oauth_id,
            avatar_url=avatar_url,
            status=UserStatus.PENDING_VERIFICATION if auth_provider == AuthProvider.EMAIL else UserStatus.ACTIVE,
        )
        if password:
            user.hashed_password = get_password_hash(password)
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_last_active(self, user_id: uuid.UUID) -> None:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_active_at=datetime.now(timezone.utc))
        )
        await self.db.commit()

    async def update_profile(
        self,
        user_id: uuid.UUID,
        full_name: Optional[str] = None,
        bio: Optional[str] = None,
        avatar_url: Optional[str] = None,
        timezone: Optional[str] = None,
    ) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        if full_name is not None:
            user.full_name = full_name
        if bio is not None:
            user.bio = bio
        if avatar_url is not None:
            user.avatar_url = avatar_url
        if timezone is not None:
            user.timezone = timezone

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def deactivate(self, user_id: uuid.UUID) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        user.status = UserStatus.INACTIVE
        await self.db.commit()
        return True
