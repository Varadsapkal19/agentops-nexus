"""User model."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization, OrganizationMember
    from app.models.api_key import APIKey
    from app.models.audit import AuditLog
    from app.models.notification import Notification


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ORG_OWNER = "org_owner"
    ORG_ADMIN = "org_admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class AuthProvider(str, Enum):
    EMAIL = "email"
    GOOGLE = "google"
    GITHUB = "github"


class User(BaseModel):
    __tablename__ = "users"

    # Basic info
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Auth
    auth_provider: Mapped[str] = mapped_column(
        SAEnum(AuthProvider), default=AuthProvider.EMAIL, nullable=False
    )
    oauth_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_verification_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    password_reset_expires: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # MFA
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    mfa_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    mfa_backup_codes: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)

    # Status & Role
    status: Mapped[str] = mapped_column(
        SAEnum(UserStatus), default=UserStatus.PENDING_VERIFICATION, nullable=False
    )
    system_role: Mapped[str] = mapped_column(
        SAEnum(UserRole), default=UserRole.DEVELOPER, nullable=False
    )

    # Settings
    preferences: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)
    timezone: Mapped[str] = mapped_column(String(100), default="UTC", nullable=False)
    locale: Mapped[str] = mapped_column(String(10), default="en", nullable=False)

    # Metadata
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    memberships: Mapped[List["OrganizationMember"]] = relationship(
        "OrganizationMember", back_populates="user", lazy="selectin"
    )
    api_keys: Mapped[List["APIKey"]] = relationship(
        "APIKey", back_populates="user", lazy="selectin"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", back_populates="user", lazy="dynamic"
    )
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification", back_populates="user", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<User {self.email}>"
