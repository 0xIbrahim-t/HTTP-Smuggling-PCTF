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
            if request.url.path.startswith("/api/admin"):
                raise HTTPException(status_code=401, detail="Unauthorized")
            return await call_next(request)

        try:
            # Vulnerable: No validation of token signing method
            token = auth_header.split(" ")[1]
            payload = decode_jwt(token)
            request.state.user = payload
            
            # Vulnerable: Doesn't validate admin role properly
            if request.url.path.startswith("/api/admin"):
                if payload.get("role") != "admin":
                    raise HTTPException(status_code=403, detail="Forbidden")
                
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)