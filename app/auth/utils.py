from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, asc, desc
from typing import Optional, List
import jwt
from passlib.context import CryptContext

from app.config import settings
from app.auth import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User operations
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# HealthArticle CRUD operations
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
