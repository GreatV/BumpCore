from pydantic import BaseModel
from typing import List

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
