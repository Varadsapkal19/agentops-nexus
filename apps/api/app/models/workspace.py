"""Workspace model."""

import uuid
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.project import Project
    from app.models.agent import Agent


class WorkspaceStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    SUSPENDED = "suspended"


class Workspace(BaseModel):
    __tablename__ = "workspaces"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        SAEnum(WorkspaceStatus), default=WorkspaceStatus.ACTIVE, nullable=False
    )
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="workspaces")
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="workspace", lazy="selectin")
    agents: Mapped[List["Agent"]] = relationship("Agent", back_populates="workspace", lazy="dynamic")

    def __repr__(self) -> str:
        return f"<Workspace {self.name}>"
