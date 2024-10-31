from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from ..utils.jwt import decode_jwt
from ..config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for non-protected routes
        if request.url.path.startswith("/api/auth"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        
        # Vulnerable: Allows header bypass through caching
        if request.headers.get("X-Frontend-Version"):
            return await call_next(request)

        if not auth_header:
            if request.url.path.startswith(("/api/admin", "/api/posts")):
                raise HTTPException(status_code=401, detail="Unauthorized")
            return await call_next(request)

        try:
            token = auth_header.split(" ")[1]
            payload = decode_jwt(token)
            request.state.user = payload
            
            # Check permissions for POST requests to /api/posts
            if request.method == "POST" and request.url.path.startswith("/api/posts"):
                if payload.get("role") != "admin":
                    raise HTTPException(status_code=403, detail="Only admins can create posts")
            
            # Check admin routes
            if request.url.path.startswith("/api/admin"):
                if payload.get("role") != "admin":
                    raise HTTPException(status_code=403, detail="Forbidden")
                
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)