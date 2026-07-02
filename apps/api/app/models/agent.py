"""Agent model - core entity representing AI agents."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import (
    Boolean, DateTime, Float, ForeignKey, Integer, String, Text,
    Enum as SAEnum, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.workspace import Workspace
    from app.models.incident import Incident
    from app.models.cost import CostRecord
    from app.models.quality import QualityRecord
    from app.models.safety import SafetyRecord


class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    PAUSED = "paused"
    DEPLOYING = "deploying"
    MAINTENANCE = "maintenance"


class AgentType(str, Enum):
    SUPERVISOR = "supervisor"
    COST_GOVERNANCE = "cost_governance"
    QUALITY = "quality"
    SAFETY = "safety"
    MEMORY = "memory"
    ROUTING = "routing"
    OPTIMIZATION = "optimization"
    EXECUTION = "execution"
    INCIDENT_RESPONSE = "incident_response"
    COMPLIANCE = "compliance"
    PROMPT_ENGINEERING = "prompt_engineering"
    ANALYTICS = "analytics"
    KNOWLEDGE = "knowledge"
    CUSTOM = "custom"


class AIModel(str, Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    GEMINI_1_5_PRO = "gemini-1.5-pro"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    MIXTRAL_8X7B = "mixtral-8x7b-32768"
    LLAMA_3_70B = "llama-3.1-70b-versatile"


class Agent(BaseModel):
    __tablename__ = "agents"

    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    agent_type: Mapped[str] = mapped_column(SAEnum(AgentType), nullable=False, index=True)
    version: Mapped[str] = mapped_column(String(50), default="1.0.0", nullable=False)

    # Ownership
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    workspace_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="SET NULL"),
        nullable=True, index=True
    )
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Configuration
    model: Mapped[str] = mapped_column(String(100), default="gpt-4o", nullable=False)
    system_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, default=0.7, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, default=4096, nullable=False)
    tools: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True, default=list)
    config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True, default=list)

    # Status
    status: Mapped[str] = mapped_column(
        SAEnum(AgentStatus), default=AgentStatus.INACTIVE, nullable=False, index=True
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Metrics (aggregated)
    total_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    successful_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed_runs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_latency_ms: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    avg_quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    avg_safety_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Last activity
    last_run_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="agents")
    workspace: Mapped[Optional["Workspace"]] = relationship("Workspace", back_populates="agents")
    runs: Mapped[List["AgentRun"]] = relationship("AgentRun", back_populates="agent", lazy="dynamic")
    metrics: Mapped[List["AgentMetric"]] = relationship(
        "AgentMetric", back_populates="agent", lazy="dynamic"
    )
    incidents: Mapped[List["Incident"]] = relationship(
        "Incident", back_populates="agent", lazy="dynamic"
    )
    cost_records: Mapped[List["CostRecord"]] = relationship(
        "CostRecord", back_populates="agent", lazy="dynamic"
    )
    quality_records: Mapped[List["QualityRecord"]] = relationship(
        "QualityRecord", back_populates="agent", lazy="dynamic"
    )
    safety_records: Mapped[List["SafetyRecord"]] = relationship(
        "SafetyRecord", back_populates="agent", lazy="dynamic"
    )

    __table_args__ = (
        Index("ix_agents_org_status", "organization_id", "status"),
        Index("ix_agents_org_type", "organization_id", "agent_type"),
    )

    def __repr__(self) -> str:
        return f"<Agent {self.name} ({self.agent_type})>"


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class AgentRun(BaseModel):
    __tablename__ = "agent_runs"

    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    trace_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    span_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Run details
    status: Mapped[str] = mapped_column(SAEnum(RunStatus), default=RunStatus.PENDING, nullable=False)
    input_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Timing
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Token usage
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Quality metrics
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    safety_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    hallucination_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    relevance_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Model info
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True, default=list)

    # Relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="runs")

    __table_args__ = (
        Index("ix_agent_runs_agent_status", "agent_id", "status"),
        Index("ix_agent_runs_created_at", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<AgentRun {self.id} ({self.status})>"


class AgentMetric(BaseModel):
    __tablename__ = "agent_metrics"

    agent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    metric_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    labels: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Relationships
    agent: Mapped["Agent"] = relationship("Agent", back_populates="metrics")

    __table_args__ = (
        Index("ix_agent_metrics_agent_type", "agent_id", "metric_type"),
        Index("ix_agent_metrics_recorded_at", "recorded_at"),
    )

    def __repr__(self) -> str:
        return f"<AgentMetric {self.metric_name}={self.value}>"
