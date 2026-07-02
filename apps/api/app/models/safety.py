"""Safety and compliance models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text, Enum as SAEnum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.agent import Agent


class RiskLevel(str, Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SafetyRecord(BaseModel):
    __tablename__ = "safety_records"

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

    # Risk assessment
    overall_risk_level: Mapped[str] = mapped_column(SAEnum(RiskLevel), nullable=False, index=True)
    overall_safety_score: Mapped[float] = mapped_column(Float, nullable=False)  # 0-1, higher is safer

    # Enkrypt AI checks
    hallucination_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    hallucination_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    bias_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    bias_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    toxicity_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    toxicity_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    jailbreak_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    jailbreak_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pii_detected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    pii_types: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    compliance_passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    compliance_failures: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    policy_violations: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # Action taken
    blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    block_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    enkrypt_raw_response: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    # Relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="safety_records")

    __table_args__ = (
        Index("ix_safety_records_agent_recorded_at", "agent_id", "recorded_at"),
        Index("ix_safety_records_risk_level", "overall_risk_level"),
    )

    def __repr__(self) -> str:
        return f"<SafetyRecord risk={self.overall_risk_level}>"


class PolicyType(str, Enum):
    CONTENT = "content"
    COST = "cost"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    GOVERNANCE = "governance"


class SafetyPolicy(BaseModel):
    __tablename__ = "safety_policies"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    policy_type: Mapped[str] = mapped_column(SAEnum(PolicyType), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    priority: Mapped[int] = mapped_column(default=0, nullable=False)
    rules: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    actions: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)  # block, warn, log
    applies_to: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # agent IDs or 'all'
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<SafetyPolicy {self.name}>"
