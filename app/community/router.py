from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, or_, func
from typing import List, Optional
from datetime import datetime

from app.database.base import get_db
from app.auth.utils import get_current_user
from app.auth.models import User
from .models import Post, Comment, PostLike, PostType
from .schemas import (
    PostCreate, PostResponse, PostList, CommentCreate, 
    CommentResponse, LikeResponse, PostFilter
)

router = APIRouter(prefix="/community", tags=["社区"])

@router.post("/posts", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_post = Post(
        **post.model_dump(),
        author_id=current_user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts", response_model=PostList)
async def list_posts(
    db: Session = Depends(get_db),
    filter_params: PostFilter = Depends(),
):
    query = db.query(Post).outerjoin(Post.author).options(joinedload(Post.author))
    
    # Apply filters
    if filter_params.type:
        query = query.filter(Post.type == filter_params.type)
    if filter_params.is_hot is not None:
        query = query.filter(Post.is_hot == filter_params.is_hot)
    if filter_params.author_id:
        query = query.filter(Post.author_id == filter_params.author_id)
    if filter_params.tag:
        # Handle JSON string tags from SQLite
        query = query.filter(Post.tags.like(f'%{filter_params.tag}%'))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    posts = query.order_by(desc(Post.created_at))\
        .offset((filter_params.page - 1) * filter_params.page_size)\
        .limit(filter_params.page_size)\
        .all()
    
    return PostList(total=total, posts=posts)

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).join(Post.author).options(joinedload(Post.author)).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("/posts/{post_id}/like", response_model=LikeResponse)
async def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    existing_like = db.query(PostLike).filter(
        PostLike.post_id == post_id,
        PostLike.user_id == current_user.id
    ).first()
    
    if existing_like:
        # Unlike if already liked
        db.delete(existing_like)
        post.likes_count -= 1
    else:
        # Add new like
        like = PostLike(post_id=post_id, user_id=current_user.id)
        db.add(like)
        post.likes_count += 1
    
    db.commit()
    return LikeResponse(
        success=True,
        likes_count=post.likes_count
    )

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        **comment.model_dump(),
        author_id=current_user.id,
        post_id=post_id
    )
    post.comments_count += 1
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
async def list_comments(
    post_id: int,
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0),
    db: Session = Depends(get_db)
):
    comments = db.query(Comment)\
        .join(Comment.author)\
        .options(joinedload(Comment.author))\
        .filter(Comment.post_id == post_id)\
        .order_by(desc(Comment.created_at))\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    return comments
