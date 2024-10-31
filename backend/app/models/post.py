from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .user import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)  # Vulnerable: No content sanitization
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    reported = Column(Boolean, default=False)
    
    # Relationships
    author = relationship("User", back_populates="posts")

    # Vulnerable: No content validation
    @classmethod
    def create(cls, title: str, content: str, author_id: int):
        return cls(
            title=title,
            content=content,
            author_id=author_id
        )

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    reporter_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed = Column(Boolean, default=False)
    
    # Relationships
    post = relationship("Post")
    reporter = relationship("User")