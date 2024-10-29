from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..utils.auth import generate_jwt

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Debug prints
        print("Login attempt received:")
        print(f"Data received: {data}")
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing credentials'}), 400

        username = data.get('username')
        password = data.get('password')
        
        print(f"Attempting login for username: {username}")
        print(f"With password: {password}")
        
        # Get user and print debug info
        user = User.query.filter_by(username=username).first()
        print(f"Found user: {user}")
        if user:
            print(f"Stored password: {user.password_hash}")
            print(f"Password match: {user.password_hash == password}")

        if user and user.password_hash == password:
            token = generate_jwt(user.id, user.role)
            print(f"Login successful for {username}")
            return jsonify({'token': token})
        
        print(f"Login failed for {username}")
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

# Debug route to check users in database
@bp.route('/debug/users', methods=['GET'])
def debug_users():
    users = User.query.all()
    return jsonify([{
        'username': user.username,
        'password': user.password_hash,
        'role': user.role
    } for user in users])