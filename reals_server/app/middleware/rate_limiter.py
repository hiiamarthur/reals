import time
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.requests import Request

requests = defaultdict(list)
REQUESTS_PER_MINUTE = 1


async def rate_limit_middleware(request: Request, call_next):
    # Increase these values for development
    MAX_REQUESTS = 100  # Increase from current value
    TIME_WINDOW = 60  # Seconds

    # You might want to skip rate limiting for certain paths
    if request.url.path.startswith("/data/"):
        return await call_next(request)

    client_ip = request.client.host
    now = time.time()

    # Clean old requests
    requests[client_ip] = [
        req_time for req_time in requests[client_ip] if now - req_time < 60
    ]

    # Check rate limit
    if len(requests[client_ip]) >= REQUESTS_PER_MINUTE:
        raise HTTPException(
            status_code=429, detail="Too many requests. Please try again later."
        )

    # Add new request
    requests[client_ip].append(now)

    return await call_next(request)
