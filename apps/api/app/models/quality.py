"""Quality assessment model."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.agent import Agent


class QualityRecord(BaseModel):
    __tablename__ = "quality_records"

    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    # Quality dimensions
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    relevance_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    coherence_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    completeness_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    accuracy_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    helpfulness_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hallucination_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0=no hallucination, 1=full
    groundedness_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Evaluation metadata
    evaluator_model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    evaluation_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    evaluation_details: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    user_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_rating: Mapped[Optional[int]] = mapped_column(nullable=True)  # 1-5

    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    # Relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="quality_records")

    __table_args__ = (
        Index("ix_quality_records_agent_recorded_at", "agent_id", "recorded_at"),
        Index("ix_quality_records_org_recorded_at", "organization_id", "recorded_at"),
    )

    def __repr__(self) -> str:
        return f"<QualityRecord score={self.overall_score:.2f}>"
