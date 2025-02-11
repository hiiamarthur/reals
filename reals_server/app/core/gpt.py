from openai import AsyncOpenAI, OpenAI
from app.core.config import settings

print("settings", settings)
client = OpenAI(
    api_key=settings.OPENAI_API_KEY,
    # organization=settings.ORGANIZATION_ID,
)

asyncClient = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY,
    # organization=settings.ORGANIZATION_ID,
)
