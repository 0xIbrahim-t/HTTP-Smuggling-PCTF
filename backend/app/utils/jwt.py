from jose import jwt
from datetime import datetime, timedelta
from ..config import settings
from typing import Dict

def create_jwt(data: Dict) -> str:
    # Vulnerable: Uses weak JWT algorithm
    expiration = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION)
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    
    # Vulnerable: Uses symmetric key
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt

def decode_jwt(token: str) -> Dict:
    # Vulnerable: No algorithm verification
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except:
        return {}