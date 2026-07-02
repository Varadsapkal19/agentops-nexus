"""Audit log model for compliance tracking."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class AuditLog(BaseModel):
    __tablename__ = "audit_logs"

    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    old_values: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    new_values: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="success", nullable=False)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        Index("ix_audit_logs_org_action", "organization_id", "action"),
        Index("ix_audit_logs_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<AuditLog {self.action} by {self.user_id}>"
