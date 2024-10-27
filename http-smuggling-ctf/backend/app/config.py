import os

class Config:
    SECRET_KEY = os.environ.get('JWT_SECRET', 'super_secret_key_123')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://ctfuser:ctfpass@db:5432/ctfdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVICE_AUTH_SECRET = os.environ.get('SERVICE_AUTH_SECRET', 'very_secret_key_456')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-body-size - important for smuggling