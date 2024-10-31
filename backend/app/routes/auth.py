from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.session import get_db
from ..models.user import User, UserRole
from ..utils.security import hash_password, verify_password
from ..utils.jwt import create_jwt
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Vulnerable: No input validation for username
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, password_hash=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Vulnerable: Token contains predictable data
    token = create_jwt({"sub": db_user.username, "id": db_user.id, "role": "user"})
    return {"access_token": token}

@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Vulnerable: No rate limiting
    token = create_jwt({
        "sub": db_user.username,
        "id": db_user.id,
        "role": db_user.role
    })
    
    return {"access_token": token}