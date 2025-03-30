from sqlalchemy import Boolean, Column, String, Integer, DateTime
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
