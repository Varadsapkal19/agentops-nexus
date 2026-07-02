"""Rate limiting middleware using Redis."""

import time
from typing import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings

# Paths exempt from rate limiting
EXEMPT_PATHS = ["/health", "/metrics", "/api/docs", "/api/redoc", "/api/openapi.json"]


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip exempt paths
        if any(request.url.path.startswith(path) for path in EXEMPT_PATHS):
            return await call_next(request)
        
        # Get client identifier
        client_ip = request.client.host if request.client else "unknown"
        api_key = request.headers.get("X-API-Key")
        identifier = api_key or client_ip
        
        # Check rate limit using Redis
        try:
            from app.core.redis_client import redis_client
            
            key = f"rate_limit:{identifier}:{int(time.time() // settings.RATE_LIMIT_WINDOW)}"
            count = await redis_client.increment(key)
            
            if count == 1:
                await redis_client.expire(key, settings.RATE_LIMIT_WINDOW)
            
            if count > settings.RATE_LIMIT_REQUESTS:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded",
                        "retry_after": settings.RATE_LIMIT_WINDOW,
                    },
                    headers={
                        "X-Request-ID": request.state.request_id if hasattr(request.state, 'request_id') else "",
                        "X-RateLimit-Limit": str(settings.RATE_LIMIT_REQUESTS),
                        "X-RateLimit-Remaining": "0",
                        "Retry-After": str(settings.RATE_LIMIT_WINDOW),
                    },
                )
            
            response = await call_next(request)
            response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
            response.headers["X-RateLimit-Remaining"] = str(
                max(0, settings.RATE_LIMIT_REQUESTS - count)
            )
            return response
            
        except Exception:
            # If Redis is unavailable, allow the request
            return await call_next(request)
