from flask import Blueprint, request, jsonify
from ..models.user import User
from .. import db
from ..utils.auth import generate_jwt

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    token = generate_jwt(user.id, 'user')
    return jsonify({'token': token})

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = generate_jwt(user.id, user.role)
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401