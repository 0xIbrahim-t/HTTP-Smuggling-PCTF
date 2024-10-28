from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..utils.auth import generate_jwt

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing credentials'}), 400

        username = data['username']
        password = data['password']

        # Debug print
        print(f"Login attempt - Username: {username}")
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Generate token with user's role
            token = generate_jwt(user.id, user.role)
            return jsonify({'token': token})
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug print
        return jsonify({'error': 'Login failed'}), 500

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        
        token = generate_jwt(user.id, 'user')
        return jsonify({'token': token})
        
    except Exception as e:
        print(f"Registration error: {str(e)}")  # Debug print
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500