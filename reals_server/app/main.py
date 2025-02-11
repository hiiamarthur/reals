from typing import Union
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as api_router
import uvicorn

from app.core.database import init_db
from app.middleware.rate_limiter import rate_limit_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

# # Add rate limiter middleware
# app.middleware("http")(rate_limit_middleware)

app.include_router(api_router)

# Add this if you want to run the server directly from this file
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Accepts connections from all IPs
        port=8000,  # Port number
        reload=True,  # Auto-reload on code changes
    )
