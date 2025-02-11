from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header

from app.controllers.itinerary_controller import ItineraryController
from app.schemas.itinerary_schema import ItineraryRequest
from app.core.database import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/itinerary", tags=["itinerary"])


async def get_itinerary_controller(db: AsyncSession = Depends(get_async_db)):
    return ItineraryController(db)


@router.post("/generate-itinerary")
async def generate_itinerary(
    itinerary_request: ItineraryRequest,
    user_id: str = Header(..., alias="User-Id", description="User ID"),
    session_id: Optional[str] = Header(
        None, alias="Session-Id", description="Session ID"
    ),
    is_streamed: bool = False,
    db: AsyncSession = Depends(get_async_db),
    # controller: ItineraryController = Depends(get_itinerary_controller),
):
    try:
        controller = ItineraryController(db)
        return await controller.create_itinerary(
            db=db,
            request=itinerary_request,
            user_id=user_id,
            session_id=session_id,
            is_streamed=is_streamed,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
