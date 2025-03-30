from sqlalchemy import Column, String, Integer, Text

from app.database.base import Base

class HealthArticle(Base):
    __tablename__ = "health_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    category = Column(String(50))  # 例如：营养、运动、心理等
    tags = Column(String(200))     # 逗号分隔的标签
    author = Column(String(100))
    created_at = Column(String(50))  # ISO格式的日期时间
