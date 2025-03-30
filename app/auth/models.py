from sqlalchemy import Boolean, Column, String, Integer, Float, Text, DateTime
from datetime import datetime

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 可以根据需要添加更多字段，如用户资料信息
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)

class HealthArticle(Base):
    __tablename__ = "health_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    category = Column(String(50))  # 例如：营养、运动、心理等
    tags = Column(String(200))     # 逗号分隔的标签
    author = Column(String(100))
    created_at = Column(String(50))  # ISO格式的日期时间
