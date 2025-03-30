from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.base import get_db
from app.auth import utils, schemas

router = APIRouter()

# Health Articles endpoints
@router.get("/articles/{article_id}", response_model=schemas.HealthArticle)
def read_article(article_id: int, db: Session = Depends(get_db)):
    """
    Get a specific health article by ID.
    """
    db_article = utils.get_article(db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.get("/articles", response_model=schemas.HealthArticleList)
def read_articles(
    skip: int = 0, 
    limit: int = 10, 
    category: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query("created_at", regex="^(created_at|title)$"),
    sort_desc: bool = True,
    db: Session = Depends(get_db)
):
    """
    Get all health articles with filtering, pagination and sorting.
    """
    articles = utils.get_articles(
        db, skip=skip, limit=limit, category=category, 
        tag=tag, search=search, sort_by=sort_by, sort_desc=sort_desc
    )
    total = utils.get_articles_count(db, category=category, tag=tag, search=search)
    return {"articles": articles, "total": total}

@router.post("/articles", response_model=schemas.HealthArticle)
def create_article(article: schemas.HealthArticleCreate, db: Session = Depends(get_db)):
    """
    Create a new health article.
    """
    return utils.create_article(db=db, article=article)

@router.put("/articles/{article_id}", response_model=schemas.HealthArticle)
def update_article(article_id: int, article_update: schemas.HealthArticleCreate, db: Session = Depends(get_db)):
    """
    Update a health article.
    """
    db_article = utils.update_article(db, article_id=article_id, article=article_update)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    """
    Delete a health article.
    """
    success = utils.delete_article(db, article_id=article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"detail": f"Article {article_id} deleted successfully"}
