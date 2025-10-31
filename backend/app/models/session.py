"""
Database models for chat sessions.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class ChatSession(Base):
    """
    Chat session model for storing user chat sessions.
    
    Attributes:
        id: Unique session identifier (UUID)
        user_id: Optional user identifier
        title: Session title
        status: Session status (active, completed, archived)
        created_at: Timestamp when session was created
        updated_at: Timestamp when session was last updated
        metadata: Additional JSON metadata
        is_active: Whether the session is currently active
        message_count: Number of messages in the session
    """
    
    __tablename__ = "chat_sessions"
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True,
        comment="Unique session identifier"
    )
    
    user_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="User identifier"
    )
    
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="New Chat Session",
        comment="Session title"
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
        index=True,
        comment="Session status: active, completed, archived"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        comment="Timestamp when session was created"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Timestamp when session was last updated"
    )
    
    metadata_: Mapped[Optional[str]] = mapped_column(
        "metadata",
        Text,
        nullable=True,
        comment="Additional JSON metadata"
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
        comment="Whether the session is currently active"
    )
    
    message_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of messages in the session"
    )
    
    def __repr__(self) -> str:
        """String representation of the ChatSession."""
        return f"<ChatSession(id={self.id}, title={self.title}, status={self.status})>"
    
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "title": self.title,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata_,
            "is_active": self.is_active,
            "message_count": self.message_count,
        }
