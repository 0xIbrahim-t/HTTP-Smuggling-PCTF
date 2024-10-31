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
    # Vulnerable: No content sanitization
    user_id = request.state.user.get("id")
    db_post = Post(
        title=post.title,
        content=post.content,
        author_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    request: Request,
    x_frontend_version: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    # Vulnerable: Response can be cached and poisoned
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/{post_id}/report")
async def report_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
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