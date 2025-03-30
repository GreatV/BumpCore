from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .models import PostType

class UserBase(BaseModel):
    username: str
    
class UserInfo(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int
    
class CommentResponse(CommentBase):
    id: int
    author: UserInfo
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title: str
    content: str
    type: PostType = PostType.GENERAL
    tags: List[str] = []

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author: UserInfo
    likes_count: int
    comments_count: int
    is_hot: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostList(BaseModel):
    total: int
    posts: List[PostResponse]

class LikeResponse(BaseModel):
    success: bool
    likes_count: int

# For filtering posts
class PostFilter(BaseModel):
    type: Optional[PostType] = None
    is_hot: Optional[bool] = None
    author_id: Optional[int] = None
    tag: Optional[str] = None
    page: int = 1
    page_size: int = 20
