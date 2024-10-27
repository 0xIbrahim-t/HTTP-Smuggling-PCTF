from functools import wraps
from flask import request, jsonify
from ..utils.auth import verify_jwt

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = verify_jwt()
        if not payload:
            return jsonify({'error': 'Valid authentication required'}), 401
        return f(*args, **kwargs)
    return decorated