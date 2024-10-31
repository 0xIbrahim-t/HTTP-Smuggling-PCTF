from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import redis
import json
from ..config import settings

class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = redis.from_url(settings.REDIS_URL)
        
    async def dispatch(self, request: Request, call_next):
        if not settings.CACHE_ENABLED:
            return await call_next(request)

        # Vulnerable: Uses user-controlled header for cache key
        cache_key = f"{request.method}:{request.url}:{request.headers.get('X-Frontend-Version', 'v1')}"
        
        # Vulnerable: Doesn't validate cached content
        cached_response = self.redis.get(cache_key)
        if cached_response and request.method == "GET":
            data = json.loads(cached_response)
            return Response(
                content=data["content"],
                status_code=data["status_code"],
                headers=data["headers"]
            )

        response = await call_next(request)
        
        # Vulnerable: Caches all responses including those with sensitive data
        if request.method == "GET":
            response_data = {
                "content": response.body,
                "status_code": response.status_code,
                "headers": dict(response.headers)
            }
            self.redis.setex(
                cache_key,
                settings.CACHE_EXPIRE,
                json.dumps(response_data)
            )
            
        return response