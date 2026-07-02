"""Project model."""

import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.workspace import Workspace


class ProjectStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    ON_HOLD = "on_hold"


class Project(BaseModel):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    status: Mapped[str] = mapped_column(
        SAEnum(ProjectStatus), default=ProjectStatus.ACTIVE, nullable=False
    )
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Relationships
    workspace: Mapped["Workspace"] = relationship("Workspace", back_populates="projects")

    def __repr__(self) -> str:
        return f"<Project {self.name}>"
