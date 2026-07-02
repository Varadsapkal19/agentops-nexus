"""Organization and OrganizationMember models."""

import uuid
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, ForeignKey, String, Text, Integer, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.workspace import Workspace
    from app.models.agent import Agent


class OrgPlan(str, Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class OrgStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    CANCELLED = "cancelled"


class MemberRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"


class Organization(BaseModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Plan & Billing
    plan: Mapped[str] = mapped_column(SAEnum(OrgPlan), default=OrgPlan.FREE, nullable=False)
    status: Mapped[str] = mapped_column(SAEnum(OrgStatus), default=OrgStatus.TRIAL, nullable=False)
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Limits
    max_agents: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    max_workspaces: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    max_api_calls_per_day: Mapped[int] = mapped_column(Integer, default=10000, nullable=False)
    max_members: Mapped[int] = mapped_column(Integer, default=5, nullable=False)

    # Settings
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    feature_flags: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    
    # White Label
    is_white_labeled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    custom_domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    brand_colors: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    members: Mapped[List["OrganizationMember"]] = relationship(
        "OrganizationMember", back_populates="organization", lazy="selectin"
    )
    workspaces: Mapped[List["Workspace"]] = relationship(
        "Workspace", back_populates="organization", lazy="selectin"
    )
    agents: Mapped[List["Agent"]] = relationship(
        "Agent", back_populates="organization", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<Organization {self.name}>"


class OrganizationMember(BaseModel):
    __tablename__ = "organization_members"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(SAEnum(MemberRole), default=MemberRole.VIEWER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    permissions: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    invited_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="members")
    user: Mapped["User"] = relationship("User", back_populates="memberships", foreign_keys=[user_id])

    def __repr__(self) -> str:
        return f"<OrganizationMember {self.user_id} in {self.organization_id}>"
