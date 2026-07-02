"""Cost tracking models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, Index, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.agent import Agent
    from app.models.organization import Organization


class CostCategory(str, Enum):
    PROMPT_TOKENS = "prompt_tokens"
    COMPLETION_TOKENS = "completion_tokens"
    EMBEDDING = "embedding"
    FINE_TUNING = "fine_tuning"
    IMAGE_GENERATION = "image_generation"
    FUNCTION_CALL = "function_call"
    TOTAL = "total"


class CostRecord(BaseModel):
    __tablename__ = "cost_records"

    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="SET NULL"), nullable=True, index=True
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    run_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agent_runs.id", ondelete="SET NULL"), nullable=True
    )
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(SAEnum(CostCategory), nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    agent: Mapped[Optional["Agent"]] = relationship("Agent", back_populates="cost_records")

    __table_args__ = (
        Index("ix_cost_records_org_recorded_at", "organization_id", "recorded_at"),
        Index("ix_cost_records_agent_recorded_at", "agent_id", "recorded_at"),
    )

    def __repr__(self) -> str:
        return f"<CostRecord ${self.cost_usd:.4f}>"


class BudgetPeriod(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"


class CostBudget(BaseModel):
    __tablename__ = "cost_budgets"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    agent_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    budget_usd: Mapped[float] = mapped_column(Float, nullable=False)
    period: Mapped[str] = mapped_column(SAEnum(BudgetPeriod), nullable=False)
    alert_threshold_pct: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    current_spend_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<CostBudget {self.name} ${self.budget_usd}>"
