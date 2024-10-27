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