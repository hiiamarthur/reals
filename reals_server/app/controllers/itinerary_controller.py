from typing import Optional
from fastapi import Depends, HTTPException
from app.service.gpt_service import GPTService
from app.schemas.itinerary_schema import (
    ItineraryRequest,
    ItineraryResponse,
)
from app.core.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.gpt_schema import OpenAIRequest

# from app.repository.gpt_repository import GPTRepository


class ItineraryController:
    def __init__(self, db: AsyncSession):
        self.gpt_service = GPTService(db)

    async def create_itinerary(
        self,
        db: AsyncSession,
        request: ItineraryRequest,
        user_id: str,
        session_id: Optional[str] = None,
        is_streamed: bool = False,
    ) -> ItineraryResponse:
        try:
            # First verify session exists

            # Continue with itinerary creation
            if is_streamed:
                itineraryResponse = await self.gpt_service.streamed_request(
                    OpenAIRequest(
                        user_id=user_id,
                        session_id=session_id,
                        content=request.to_json(),
                    )
                )
            else:
                itineraryResponse = await self.gpt_service.async_request(
                    OpenAIRequest(
                        user_id=user_id,
                        session_id=session_id,
                        content=request.to_json(),
                    ),
                    db,
                )
            return itineraryResponse
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_service_status(self):
        return await self.gpt_service.get_circuit_status()
