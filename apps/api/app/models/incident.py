"""Incident model for tracking agent failures."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Enum as SAEnum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.agent import Agent
    from app.models.recommendation import Recommendation


class IncidentSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IncidentStatus(str, Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentType(str, Enum):
    AGENT_FAILURE = "agent_failure"
    HIGH_COST = "high_cost"
    QUALITY_DEGRADATION = "quality_degradation"
    SAFETY_VIOLATION = "safety_violation"
    HALLUCINATION = "hallucination"
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    COMPLIANCE_BREACH = "compliance_breach"
    ANOMALY = "anomaly"


class Incident(BaseModel):
    __tablename__ = "incidents"

    # Basic info
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    incident_type: Mapped[str] = mapped_column(SAEnum(IncidentType), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(SAEnum(IncidentSeverity), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        SAEnum(IncidentStatus), default=IncidentStatus.OPEN, nullable=False, index=True
    )

    # Context
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"),
        nullable=True, index=True
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True
    )
    trace_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Error details
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stack_trace: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    context_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Timing
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Impact
    affected_runs: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    estimated_cost_impact: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    quality_impact_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Resolution
    root_cause: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    auto_resolved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Memory
    qdrant_point_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    agent: Mapped[Optional["Agent"]] = relationship("Agent", back_populates="incidents")
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation", back_populates="incident", lazy="selectin"
    )

    __table_args__ = (
        Index("ix_incidents_org_status", "organization_id", "status"),
        Index("ix_incidents_org_severity", "organization_id", "severity"),
        Index("ix_incidents_detected_at", "detected_at"),
    )

    def __repr__(self) -> str:
        return f"<Incident {self.title} ({self.severity})>"
