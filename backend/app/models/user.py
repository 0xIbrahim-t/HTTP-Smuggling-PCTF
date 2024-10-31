from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)

    # Vulnerable: No input validation for username
    @classmethod
    def create(cls, username: str, password_hash: str, role: UserRole = UserRole.USER):
        return cls(
            username=username,
            password_hash=password_hash,
            role=role
        )