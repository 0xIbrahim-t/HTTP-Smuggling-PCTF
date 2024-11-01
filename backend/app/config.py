from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://ctfuser:ctfpass@db:5432/ctfdb"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # JWT Settings
    JWT_SECRET: str = "n0t_4_r34l_s3cr3t_1n_pr0duct10n"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 86400  # 24 hours in seconds
    
    # Admin Settings
    ADMIN_TOKEN: str = "s3cr3t_4dm1n_t0k3n"
    
    # Cache Settings
    CACHE_ENABLED: bool = True
    CACHE_EXPIRE: int = 3600
    
    # Flag
    FLAG: str = "CTF{http2_smuggl1ng_1s_fun_2024}"
    
    # CSP Settings - Intentionally vulnerable
    CSP_NONCE_LENGTH: int = 8

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()