"""Prompt library models."""

import uuid
from enum import Enum
from typing import Optional, List

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class PromptCategory(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    EVALUATION = "evaluation"
    SAFETY = "safety"


class Prompt(BaseModel):
    __tablename__ = "prompts"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(SAEnum(PromptCategory), nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    tags: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True, default=list)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    current_version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    avg_quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    versions: Mapped[List["PromptVersion"]] = relationship(
        "PromptVersion", back_populates="prompt", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Prompt {self.name}>"


class PromptVersion(BaseModel):
    __tablename__ = "prompt_versions"

    prompt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prompts.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)  # template variables
    model_suggestions: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    # Relationships
    prompt: Mapped["Prompt"] = relationship("Prompt", back_populates="versions")

    def __repr__(self) -> str:
        return f"<PromptVersion {self.prompt_id} v{self.version}>"
