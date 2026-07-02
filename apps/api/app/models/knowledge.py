"""Knowledge base models."""

import uuid
from enum import Enum
from typing import Optional, List

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class KnowledgeBase(BaseModel):
    __tablename__ = "knowledge_bases"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    qdrant_collection: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    embedding_model: Mapped[str] = mapped_column(String(100), default="text-embedding-3-large", nullable=False)
    document_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Relationships
    documents: Mapped[List["KnowledgeDocument"]] = relationship(
        "KnowledgeDocument", back_populates="knowledge_base", lazy="dynamic"
    )

    def __repr__(self) -> str:
        return f"<KnowledgeBase {self.name}>"


class DocumentStatus(str, Enum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class KnowledgeDocument(BaseModel):
    __tablename__ = "knowledge_documents"

    knowledge_base_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("knowledge_bases.id", ondelete="CASCADE"),
        nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    file_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(
        SAEnum(DocumentStatus), default=DocumentStatus.PROCESSING, nullable=False
    )
    chunk_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    qdrant_ids: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    knowledge_base: Mapped["KnowledgeBase"] = relationship("KnowledgeBase", back_populates="documents")

    def __repr__(self) -> str:
        return f"<KnowledgeDocument {self.title}>"
