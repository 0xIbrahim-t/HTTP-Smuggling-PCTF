from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, posts, admin
from .middleware.auth import AuthMiddleware
from .middleware.cache import CacheMiddleware
from .database.session import init_db
from . import config

app = FastAPI(title="CTF Blog API")

# CORS configuration - Intentionally permissive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(CacheMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

# Vulnerable: No validation of Transfer-Encoding headers
@app.middleware("http")
async def process_headers(request: Request, call_next):
    response = await call_next(request)
    return response

@app.on_event("startup")
async def startup():
    await init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)