"""Alert and AlertRule models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, Enum as SAEnum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class AlertSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"


class AlertCondition(str, Enum):
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    EQUALS = "equals"
    ANOMALY = "anomaly"


class Alert(BaseModel):
    __tablename__ = "alerts"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True
    )
    rule_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("alert_rules.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(SAEnum(AlertSeverity), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        SAEnum(AlertStatus), default=AlertStatus.ACTIVE, nullable=False, index=True
    )
    metric_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metric_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    threshold_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    acknowledged_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    notification_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index("ix_alerts_org_status", "organization_id", "status"),
        Index("ix_alerts_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Alert {self.title} ({self.severity})>"


class AlertRule(BaseModel):
    __tablename__ = "alert_rules"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    condition: Mapped[str] = mapped_column(SAEnum(AlertCondition), nullable=False)
    threshold_value: Mapped[float] = mapped_column(Float, nullable=False)
    severity: Mapped[str] = mapped_column(SAEnum(AlertSeverity), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    cooldown_minutes: Mapped[int] = mapped_column(default=60, nullable=False)
    notification_channels: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)  # email, slack, webhook
    applies_to_agents: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<AlertRule {self.name}>"
