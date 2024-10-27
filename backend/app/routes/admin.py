from flask import Blueprint, request, jsonify
from ..models.blog import BlogPost
from ..middleware.admin_required import admin_required
from .. import db

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    # Return sensitive information when accessed
    return jsonify({
        'message': 'Welcome Admin!',
        'flag': 'flag{http2_smuggl1ng_w1th_c4ch3_p01s0n}',
        'server_config': {
            'database_url': 'postgresql://ctfuser:ctfpass@db:5432/ctfdb',
            'admin_credentials': 'admin:complex_admin_pass_123'
        }
    })

@bp.route('/reports', methods=['GET'])
@admin_required
def get_reports():
    reported_posts = BlogPost.query.filter_by(is_reported=True).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'report_count': post.report_count
    } for post in reported_posts])

@bp.route('/review/<int:post_id>', methods=['POST'])
@admin_required
def review_post(post_id):
    data = request.get_json()
    action = data.get('action')
    
    post = BlogPost.query.get_or_404(post_id)
    
    if action == 'delete':
        db.session.delete(post)
    elif action == 'clear':
        post.is_reported = False
        post.report_count = 0
    
    db.session.commit()
    return jsonify({'message': f'Post {action}d successfully'})