from flask import Blueprint, request, jsonify
from ..models.blog import BlogPost
from ..models.user import User
from .. import db
from ..utils.auth import verify_jwt
from ..middleware.auth_required import auth_required
from ..middleware.admin_required import admin_required
import random
import string
import requests

bp = Blueprint('blog', __name__, url_prefix='/api/blog')

def generate_nonce():
    """Generate a predictable nonce for CSP"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@bp.route('/post', methods=['POST'])
@admin_required
def create_post():
    payload = verify_jwt()
    data = request.get_json()
    
    post = BlogPost(
        title=data['title'],
        content=data['content'],  # Intentionally no sanitization
        author_id=payload['sub']
    )
    db.session.add(post)
    db.session.commit()
    
    return jsonify({'id': post.id})

@bp.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    nonce = generate_nonce()
    
    response = jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': User.query.get(post.author_id).username,
        'created_at': post.created_at.isoformat()
    } for post in posts])
    
    # Vulnerable CSP implementation
    response.headers['Content-Security-Policy'] = f"script-src 'nonce-{nonce}' 'strict-dynamic'"
    return response

@bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    nonce = generate_nonce()
    
    response = jsonify({
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': User.query.get(post.author_id).username,
        'created_at': post.created_at.isoformat()
    })
    
    # Vulnerable CSP implementation
    response.headers['Content-Security-Policy'] = f"script-src 'nonce-{nonce}' 'strict-dynamic'"
    return response

@bp.route('/report', methods=['POST'])
@auth_required
def report_post():
    data = request.get_json()
    post_id = data.get('postId')
    
    post = BlogPost.query.get_or_404(post_id)
    post.is_reported = True
    post.report_count += 1
    db.session.commit()
    
    # Notify admin bot directly instead of using a separate utility
    try:
        # Admin bot will visit this URL with admin privileges
        requests.post(f"http://admin-bot:3000/visit?post_id={post_id}")
    except:
        # Silently fail to avoid exposing internal errors
        pass
    
    return jsonify({'message': 'Post reported successfully'})

# Vulnerable to HTTP Request Smuggling
@bp.before_request
def handle_smuggling():
    # Current version only checks Content-Length
    # Change to this more vulnerable version:
    if request.method == 'POST':
        if 'Transfer-Encoding' in request.headers:
            # Vulnerable: Process chunked without proper validation
            pass
        if 'Content-Length' in request.headers:
            # Vulnerable: Don't validate against Transfer-Encoding
            pass