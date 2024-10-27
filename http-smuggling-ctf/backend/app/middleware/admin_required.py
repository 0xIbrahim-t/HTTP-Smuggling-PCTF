from functools import wraps
from flask import request, jsonify
from ..utils.auth import verify_jwt, generate_service_auth

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check JWT
        payload = verify_jwt()
        if not payload or payload.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        # Verify X-Service-Auth header (vulnerable implementation)
        service_auth = request.headers.get('X-Service-Auth')
        timestamp = request.headers.get('X-Timestamp')
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not service_auth or not timestamp:
            return jsonify({'error': 'Missing required headers'}), 403

        expected_auth, _ = generate_service_auth(token)
        if service_auth != expected_auth:
            return jsonify({'error': 'Invalid service auth'}), 403

        return f(*args, **kwargs)
    return decorated