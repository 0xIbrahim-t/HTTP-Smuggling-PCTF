from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database.session import get_db
from ..models.post import Post, Report
from ..models.user import User
from ..utils.security import verify_service_auth
from pydantic import BaseModel
import json

router = APIRouter()

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str
    reported: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PostResponse])
async def get_posts(
    request: Request,
    x_frontend_version: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    # Vulnerable: No validation of cached responses
    posts = db.query(Post).all()
    return posts

@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    # Check if user is admin (already verified in middleware)
    user_id = request.state.user.get("id")
    user_role = request.state.user.get("role")
    
    if user_role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create posts")
    
    # Vulnerable: No content sanitization
    db_post = Post(
        title=post.title,
        content=post.content,
        author_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Update the frontend to show normal users can't create posts
@router.get("/permissions", response_model=dict)
async def get_permissions(request: Request):
    user_role = request.state.user.get("role") if hasattr(request, "state") and request.state.user else None
    return {
        "can_create_posts": user_role == "admin",
        "can_report_posts": user_role is not None
    }

# Users can still report posts
@router.post("/{post_id}/report")
async def report_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Authentication required")
        
    user_id = request.state.user.get("id")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Vulnerable: No duplicate report check
    report = Report(post_id=post_id, reporter_id=user_id)
    post.reported = True
    
    db.add(report)
    db.commit()
    
    return {"message": "Post reported successfully"}