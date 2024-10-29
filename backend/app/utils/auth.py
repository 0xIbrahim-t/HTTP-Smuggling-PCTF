import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import current_app, request, jsonify
import hashlib
import time

def generate_jwt(user_id, role):
    payload = {
        'sub': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_jwt():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_service_auth(jwt_token):
    """Vulnerable implementation of X-Service-Auth header generation"""
    timestamp = int(time.time())
    secret = current_app.config['SERVICE_AUTH_SECRET']
    raw = f"{jwt_token}{timestamp}{secret}"
    return hashlib.md5(raw.encode()).hexdigest(), timestamp

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_payload = verify_jwt()
        
        if not token_payload or token_payload.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
            
        # Verify X-Service-Auth header
        service_auth = request.headers.get('X-Service-Auth')
        timestamp = request.headers.get('X-Timestamp')
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not service_auth or not timestamp:
            return jsonify({'error': 'Missing required headers'}), 403
            
        expected_auth, _ = generate_service_auth(token)
        
        if service_auth != expected_auth:
            return jsonify({'error': 'Invalid service auth'}), 403
            
        return f(*args, **kwargs)
    return decorated_function

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token_payload = verify_jwt()
        if not token_payload:
            return jsonify({'error': 'Valid authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function