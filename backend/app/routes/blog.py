from flask import Blueprint, request, jsonify, make_response
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

@bp.route('/posts', methods=['GET'])
@auth_required
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
    
    response.headers['Content-Security-Policy'] = f"script-src 'nonce-{nonce}' 'strict-dynamic'"
    return response

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

@bp.route('/post/<int:post_id>', methods=['GET'])
@auth_required
def get_post(post_id):
    try:
        post = BlogPost.query.get_or_404(post_id)
        
        # If HTML requested, render as blog post
        if 'text/html' in request.headers.get('Accept', ''):
            # Intentionally vulnerable - directly inserting content without escaping
            html_content = f'''
            <div class="blog-post">
                <h1>{post.title}</h1>
                <div class="post-meta">
                    <span>Author: {User.query.get(post.author_id).username}</span>
                    <span>Date: {post.created_at.strftime('%B %d, %Y')}</span>
                </div>
                <div class="post-content">
                    {post.content}
                </div>
            </div>
            '''
            response = make_response(html_content)
            response.headers['Content-Type'] = 'text/html'
        else:
            # Default JSON response
            response = jsonify({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': User.query.get(post.author_id).username,
                'created_at': post.created_at.isoformat()
            })
        
        # Cache headers
        if request.headers.get('X-Special-Key') == 'secret_cache_key':
            response.headers['Cache-Control'] = 'public, max-age=300'
            
        return response
        
    except Exception as e:
        print(f"Error in get_post: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/report', methods=['POST'])
@auth_required
def report_post():
    data = request.get_json()
    post_id = data.get('postId')
    
    post = BlogPost.query.get_or_404(post_id)
    post.is_reported = True
    post.report_count += 1
    db.session.commit()
    
    # Notify admin bot directly
    try:
        requests.post(f"http://admin-bot:3000/visit?post_id={post_id}")
    except:
        pass
    
    return jsonify({'message': 'Post reported successfully'})

# Vulnerable to HTTP Request Smuggling
@bp.before_request
def handle_smuggling():
    if request.method == 'POST':
        if 'Transfer-Encoding' in request.headers:
            pass  # Vulnerable: Process chunked without validation
        if 'Content-Length' in request.headers:
            pass  # Vulnerable: Don't validate against Transfer-Encoding