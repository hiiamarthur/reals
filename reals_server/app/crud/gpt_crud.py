from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.core.database import get_async_db

from fastapi import Depends
import uuid

# Assuming the SQLAlchemy models are defined as shown previously
from app.models.gpt_model import Session, Message, APIRequestLog, APIUsage


# Function to create a new session
async def create_session(user_id: int, db: AsyncSession = Depends(get_async_db)):
    new_session = Session(session_id=uuid.uuid4(), user_id=user_id)
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    return new_session


# Function to add a message to a session
async def add_message_to_session(
    session_id: uuid.UUID,
    role: str,
    content: str,
    db: AsyncSession = Depends(get_async_db),
):
    new_message = Message(session_id=session_id, role=role, content=content)
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message


# Function to track API usage (update tokens and request count)
async def track_api_usage(
    user_id: int,
    prompt_tokens: int,
    completion_tokens: int,
    rate_limit_reset: datetime,
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.exceute(APIUsage).filter(APIUsage.user_id == user_id).first()
    usage = result.scalar_one_or_none()

    if not usage:
        usage = APIUsage(user_id=user_id)
        db.add(usage)

    # Update request and token count
    usage.total_requests += 1
    usage.total_tokens += prompt_tokens + completion_tokens
    usage.rate_limit_reset = rate_limit_reset

    await db.commit()
    return usage


# Function to fetch session messages (to maintain message history)
async def fetch_session_messages(
    session_id: uuid.UUID, db: AsyncSession = Depends(get_async_db)
):
    messages = db.query(Message).filter(Message.session_id == session_id).all()
    return [{"role": message.role, "content": message.content} for message in messages]


# Function to log the API request
async def log_api_request(
    session_id: uuid.UUID,
    request_id: str,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
    rate_limit_remaining_requests: int,
    rate_limit_remaining_tokens: int,
    db: AsyncSession = Depends(get_async_db),
):

    request_log = APIRequestLog(
        session_id=session_id,
        request_id=request_id,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        rate_limit_remaining_requests=rate_limit_remaining_requests,
        rate_limit_remaining_tokens=rate_limit_remaining_tokens,
    )
    db.add(request_log)
    await db.commit()
