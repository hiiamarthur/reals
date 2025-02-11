import uuid as uuidLib
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    create_engine,
    Enum,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from typing import TYPE_CHECKING, Any, Dict, List, Optional, TypedDict
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase

from app.models.base_model import BaseModel, UUIDBase
from app.models.enums import MessageRole

if TYPE_CHECKING:
    from app.models.user_model import User

# Base = declarative_base()


class APIUsage(BaseModel):
    __tablename__ = "api_usage"

    total_requests: Mapped[int] = mapped_column(default=0)
    total_tokens: Mapped[int] = mapped_column(default=0)
    session_id: Mapped[uuidLib.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationship
    session: Mapped["Session"] = relationship(back_populates="api_usage")


class Session(UUIDBase):
    __tablename__ = "sessions"

    user_id: Mapped[uuidLib.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False
    )
    # title: Mapped[Optional[str]] = mapped_column(String(255))
    # description: Mapped[Optional[str]] = mapped_column(Text)
    # settings: Mapped[Optional[dict]] = mapped_column(JSON)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")
    api_usage: Mapped["APIUsage"] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="select"
    )

    messages: Mapped[List["Message"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="select"
    )
    request_logs: Mapped[List["APIRequestLog"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", lazy="select"
    )


def __init__(self, **kwargs):
    super().__init__()
    for key, value in kwargs.items():
        setattr(self, key, value)


# def to_dict(self) -> dict:
#     """Override to_dict to ensure messages are included"""
#     result = super().to_dict()

#     # Ensure messages are loaded and converted
#     if hasattr(self, "messages"):
#         result["messages"] = (
#             [message.to_dict() for message in self.messages]
#             if self.messages
#             else []
#         )
#     if hasattr(self, "api_usage"):
#         result["api_usage"] = self.api_usage.to_dict()

#     return result


class Message(BaseModel):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)

    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    session_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.uuid", ondelete="CASCADE"),
        nullable=False,
    )
    session: Mapped["Session"] = relationship(back_populates="messages")


class APIRequestLog(UUIDBase):
    __tablename__ = "api_request_logs"

    # Option 1: Using mapped_column (recommended)
    request_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # OR Option 2: Using Column
    # request_id = Column(String(255), nullable=True)
    log = Column(String(9999), nullable=True)
    response_code = Column(Integer)
    processing_time_ms = Column(Integer, nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    rate_limit_remaining_requests = Column(Integer, nullable=True)
    rate_limit_remaining_tokens = Column(Integer, nullable=True)
    rate_limit_reset_requests = Column(String(255), nullable=True)
    rate_limit_reset_tokens = Column(String(255), nullable=True)
    session_uuid: Mapped[uuidLib.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.uuid"),  # Note: now referencing uuid instead of session_id
        nullable=False,
    )
    session: Mapped["Session"] = relationship(back_populates="request_logs")


# Example engine creation
engine = create_engine("postgresql://postgres:postgres@localhost/reals")
# Base.metadata.create_all(engine)


class APIUsageFilter(TypedDict, total=False):
    id: Optional[int]
    user_id: Optional[int]
    total_requests: Optional[int]
    total_tokens: Optional[int]
    rate_limit_reset: Optional[datetime]


class SessionFilter(TypedDict, total=False):
    id: Optional[int]
    uuid: Optional[UUID]
    user_id: Optional[UUID]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class MessageFilter(TypedDict, total=False):
    id: Optional[int]
    role: Optional[MessageRole]
    content: Optional[str]
    session_uuid: Optional[UUID]


class APIRequestLogFilter(TypedDict, total=False):
    request_id: Optional[str]
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]
    rate_limit_remaining_requests: Optional[int]
    rate_limit_remaining_tokens: Optional[int]
    session_uuid: Optional[UUID]
