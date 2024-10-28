from .. import db
from datetime import datetime

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'  # Explicit table name
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_reported = db.Column(db.Boolean, default=False)
    report_count = db.Column(db.Integer, default=0)