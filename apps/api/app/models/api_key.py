"""API Key model."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class APIKeyScope(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    AGENT_RUN = "agent_run"


class APIKey(BaseModel):
    __tablename__ = "api_keys"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(20), nullable=False)  # First 8 chars for display
    hashed_key: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    scopes: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    usage_count: Mapped[int] = mapped_column(default=0, nullable=False)
    allowed_ips: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="api_keys")

    def __repr__(self) -> str:
        return f"<APIKey {self.name} ({self.key_prefix}...)>"
