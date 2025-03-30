from pydantic_settings import BaseSettings
from typing import Optional
import secrets

class Settings(BaseSettings):
    PROJECT_NAME: str = "BumpBuddy API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    # 令牌有效期（分钟）
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    # 数据库连接
    DATABASE_URL: str = "sqlite:///./bumpbuddy.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
