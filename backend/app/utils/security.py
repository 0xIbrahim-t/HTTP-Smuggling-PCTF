from passlib.context import CryptContext
from datetime import datetime
import hashlib
import time
from ..config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def verify_service_auth(service_auth: str) -> bool:
    # Vulnerable: Weak validation
    if not service_auth:
        return False
    
    # Vulnerable: Time-based validation
    try:
        timestamp, signature = service_auth.split('-')
        current_time = int(time.time())
        if abs(current_time - int(timestamp)) > 300:  # 5 minutes window
            return False
            
        # Vulnerable: Predictable signature
        expected = hashlib.md5(f"{timestamp}{settings.ADMIN_TOKEN}".encode()).hexdigest()
        return signature == expected
    except:
        return False

def generate_nonce() -> str:
    # Vulnerable: Predictable nonce generation
    current_time = int(time.time())
    return hashlib.md5(f"{current_time}{settings.JWT_SECRET}".encode()).hexdigest()[:8]