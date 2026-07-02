"""Notification model."""

import uuid
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String, Text, Enum as SAEnum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class NotificationType(str, Enum):
    ALERT = "alert"
    INCIDENT = "incident"
    RECOMMENDATION = "recommendation"
    SYSTEM = "system"
    COST_BUDGET = "cost_budget"
    SAFETY_VIOLATION = "safety_violation"
    AGENT_STATUS = "agent_status"
    REPORT = "report"


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True
    )
    notification_type: Mapped[str] = mapped_column(SAEnum(NotificationType), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    action_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resource_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index("ix_notifications_user_read", "user_id", "is_read"),
    )

    def __repr__(self) -> str:
        return f"<Notification {self.title}>"
