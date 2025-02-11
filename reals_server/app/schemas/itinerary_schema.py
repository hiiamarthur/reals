import json
from typing import Optional
from app.schemas.base_schema import BaseSchema


class ItineraryRequest(BaseSchema):
    location: str
    date: str
    budget: float
    preferences: Optional[str] = None
    transportation: Optional[str] = None

    def to_json(self) -> str:
        json_str = super().to_json()
        json_dict = json.loads(json_str)
        json_dict.pop("created_at")
        json_dict.pop("updated_at")
        return json.dumps(json_dict)


class ItineraryResponse(BaseSchema):
    content: str
