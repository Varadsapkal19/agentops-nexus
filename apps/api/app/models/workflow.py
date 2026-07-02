"""Workflow and WorkflowRun models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class WorkflowRunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Workflow(BaseModel):
    __tablename__ = "workflows"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(SAEnum(WorkflowStatus), default=WorkflowStatus.DRAFT, nullable=False)
    trigger_type: Mapped[str] = mapped_column(String(100), nullable=False)  # manual, schedule, event
    trigger_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    steps: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)  # workflow graph
    variables: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    total_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    successful_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<Workflow {self.name}>"


class WorkflowRun(BaseModel):
    __tablename__ = "workflow_runs"

    workflow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    status: Mapped[str] = mapped_column(
        SAEnum(WorkflowRunStatus), default=WorkflowRunStatus.PENDING, nullable=False
    )
    trigger_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    step_results: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    triggered_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<WorkflowRun {self.id} ({self.status})>"
