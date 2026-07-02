"""Recommendation model."""

import uuid
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, Float, ForeignKey, String, Text, Enum as SAEnum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class RecommendationType(str, Enum):
    COST_OPTIMIZATION = "cost_optimization"
    QUALITY_IMPROVEMENT = "quality_improvement"
    SAFETY_ENHANCEMENT = "safety_enhancement"
    PERFORMANCE = "performance"
    PROMPT_OPTIMIZATION = "prompt_optimization"
    MODEL_SWITCH = "model_switch"
    CONFIGURATION = "configuration"
    INCIDENT_RESOLUTION = "incident_resolution"


class RecommendationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    FAILED = "failed"
    EXPIRED = "expired"


class Recommendation(BaseModel):
    __tablename__ = "recommendations"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True
    )
    incident_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True
    )
    generated_by: Mapped[str] = mapped_column(String(100), nullable=False)  # which agent generated this
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation_type: Mapped[str] = mapped_column(SAEnum(RecommendationType), nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        SAEnum(RecommendationStatus), default=RecommendationStatus.PENDING, nullable=False
    )
    priority_score: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    estimated_impact: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    action_plan: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    auto_apply: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    applied_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # agent or user
    result: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5, nullable=False)
    reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    incident: Mapped[Optional["Incident"]] = relationship("Incident", back_populates="recommendations", foreign_keys=[incident_id])

    __table_args__ = (
        Index("ix_recommendations_org_status", "organization_id", "status"),
        Index("ix_recommendations_type", "recommendation_type"),
    )

    def __repr__(self) -> str:
        return f"<Recommendation {self.title}>"
