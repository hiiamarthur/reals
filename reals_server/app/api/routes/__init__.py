from fastapi import APIRouter

# from app.schemas.user_schema import UserCreateSchema
from app.models.user_model import User
from app.models.gpt_model import Session
from .gpt_route import router as gpt_router
from .itinerary_route import router as itinerary_router
from app.routes.data_route import create_data_router

# Create user router
user_router = create_data_router(
    # schema=UserCreateSchema,
    model=User,  # Pass the SQLAlchemy model
    prefix="/users",
    tags=["Users"],
)

# Create session router
session_router = create_data_router(
    model=Session,
    prefix="/sessions",
    tags=["Sessions"],
)

router = APIRouter()

router.include_router(gpt_router)
router.include_router(itinerary_router)
router.include_router(user_router, prefix="/data")
router.include_router(session_router, prefix="/data")
