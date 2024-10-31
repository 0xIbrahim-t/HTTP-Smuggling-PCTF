from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ..config import settings
from ..models.user import Base as UserBase
from ..models.post import Base as PostBase

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def init_db():
    UserBase.metadata.create_all(bind=engine)
    PostBase.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()