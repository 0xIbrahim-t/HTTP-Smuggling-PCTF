import hashlib
import time
from flask import current_app

def generate_service_auth(jwt_token, timestamp=None):
    """
    Generate X-Service-Auth header value.
    Vulnerable implementation using predictable components.
    """
    if timestamp is None:
        timestamp = int(time.time())
        
    secret = current_app.config['SERVICE_AUTH_SECRET']
    raw = f"{jwt_token}{timestamp}{secret}"
    return hashlib.md5(raw.encode()).hexdigest()

def verify_service_auth(jwt_token, service_auth, timestamp):
    """
    Verify X-Service-Auth header value.
    Vulnerable due to timing attack and predictable generation.
    """
    try:
        expected_auth = generate_service_auth(jwt_token, int(timestamp))
        # Vulnerable to timing attacks due to direct string comparison
        return service_auth == expected_auth
    except:
        return False

def verify_admin_headers(jwt_token, headers):
    """
    Verify all required admin headers.
    Returns (bool, error_message)
    """
    service_auth = headers.get('X-Service-Auth')
    timestamp = headers.get('X-Timestamp')
    
    if not service_auth:
        return False, "Missing X-Service-Auth header"
    
    if not timestamp:
        return False, "Missing X-Timestamp header"
        
    try:
        timestamp = int(timestamp)
        current = int(time.time())
        
        # Weak timestamp validation - allows for replay attacks
        if abs(current - timestamp) > 300:  # 5 minute window
            return False, "Invalid timestamp"
            
        if not verify_service_auth(jwt_token, service_auth, timestamp):
            return False, "Invalid X-Service-Auth header"
            
        return True, None
        
    except:
        return False, "Invalid header format"