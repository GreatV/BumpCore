from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from typing import Optional, List

from app.health import models, schemas

def get_article(db: Session, article_id: int) -> Optional[models.HealthArticle]:
    return db.query(models.HealthArticle).filter(models.HealthArticle.id == article_id).first()

def get_articles(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "created_at",
    sort_desc: bool = True
) -> List[models.HealthArticle]:
    query = db.query(models.HealthArticle)
    
    if category:
        query = query.filter(models.HealthArticle.category == category)
    
    if tag:
        query = query.filter(models.HealthArticle.tags.like(f"%{tag}%"))
    
    if search:
        query = query.filter(
            models.HealthArticle.title.like(f"%{search}%") | 
            models.HealthArticle.content.like(f"%{search}%")
        )
    
    if sort_by == "created_at":
        if sort_desc:
            query = query.order_by(desc(models.HealthArticle.created_at))
        else:
            query = query.order_by(asc(models.HealthArticle.created_at))
    elif sort_by == "title":
        if sort_desc:
            query = query.order_by(desc(models.HealthArticle.title))
        else:
            query = query.order_by(asc(models.HealthArticle.title))
    
    return query.offset(skip).limit(limit).all()

def get_articles_count(
    db: Session, 
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None
) -> int:
    query = db.query(func.count(models.HealthArticle.id))
    
    if category:
        query = query.filter(models.HealthArticle.category == category)
    
    if tag:
        query = query.filter(models.HealthArticle.tags.like(f"%{tag}%"))
    
    if search:
        query = query.filter(
            models.HealthArticle.title.like(f"%{search}%") | 
            models.HealthArticle.content.like(f"%{search}%")
        )
    
    return query.scalar()

def create_article(db: Session, article: schemas.HealthArticleCreate) -> models.HealthArticle:
    db_article = models.HealthArticle(
        title=article.title,
        content=article.content,
        category=article.category,
        tags=article.tags,
        author=article.author,
        created_at=datetime.now().isoformat()
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def update_article(db: Session, article_id: int, article: schemas.HealthArticleCreate) -> Optional[models.HealthArticle]:
    db_article = get_article(db, article_id)
    if db_article:
        for key, value in article.dict().items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int) -> bool:
    db_article = get_article(db, article_id)
    if db_article:
        db.delete(db_article)
        db.commit()
        return True
    return False
