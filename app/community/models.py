from sqlalchemy import Boolean, Column, String, Integer, Text, DateTime, ForeignKey, JSON, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database.base import Base

class PostType(str, enum.Enum):
    GENERAL = "GENERAL"
    QUESTION = "QUESTION"
    EXPERIENCE = "EXPERIENCE"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            # Try to match case-insensitively
            upper_value = value.upper()
            for member in cls:
                if member.value == upper_value:
                    return member
        return None

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(Enum(PostType), default=PostType.GENERAL)
    tags = Column(JSON, default=list)  # Store tags as JSON array
    
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", backref="posts")
    
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    
    is_hot = Column(Boolean, default=False)  # For hot topics feature
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", backref="comments")
    
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", backref="comments")
    
    created_at = Column(DateTime, default=datetime.utcnow)

class PostLike(Base):
    __tablename__ = "post_likes"

    id = Column(Integer, primary_key=True, index=True)
    
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", backref="likes")
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", backref="post_likes")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Add unique constraint to prevent duplicate likes
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='unique_user_post_like'),
    )
