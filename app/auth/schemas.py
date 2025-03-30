from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class HealthArticleBase(BaseModel):
    title: str
    content: str
    category: str
    tags: str
    author: str

class HealthArticleCreate(HealthArticleBase):
    pass

class HealthArticle(HealthArticleBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True

class HealthArticleList(BaseModel):
    articles: List[HealthArticle]
    total: int
