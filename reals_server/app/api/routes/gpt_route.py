from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/gpt", tags=["gpt"])


# Pydantic model for request body
class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "gpt-3.5-turbo"
    temperature: Optional[float] = 0.7


# Example response model
class ChatResponse(BaseModel):
    response: str
    # model_used: str
    model_config = {"protected_namespaces": ()}  # Or use this to disable the warning


# Simple GET endpoint
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "gpt"}


# POST endpoint for chat
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Simulate GPT response for now
        mock_response = f"This is a mock response to: {request.message}"
        return ChatResponse(response=mock_response, model_used=request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET endpoint with path parameter
@router.get("/models/{model_id}")
async def get_model_info(model_id: str):
    models = {
        "gpt-3.5-turbo": {"name": "GPT-3.5 Turbo", "max_tokens": 4096},
        "gpt-4": {"name": "GPT-4", "max_tokens": 8192},
    }
    if model_id not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    return models[model_id]
