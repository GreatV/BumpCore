from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.health.router import router as health_router
from app.community import community_router
from app.config import settings
from app.database.base import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="健康管理和孕期指导API服务",
    version=settings.VERSION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["认证"])
app.include_router(health_router, prefix=f"{settings.API_V1_STR}/health", tags=["健康"])
app.include_router(community_router, prefix=f"{settings.API_V1_STR}")

@app.get("/")
def read_root():
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "available_endpoints": [
            f"{settings.API_V1_STR}/auth/login",
            f"{settings.API_V1_STR}/auth/register",
            f"{settings.API_V1_STR}/health/week-info",
            f"{settings.API_V1_STR}/health/articles",
            f"{settings.API_V1_STR}/community/posts",
            f"{settings.API_V1_STR}/community/posts/{{post_id}}/comments",
            f"{settings.API_V1_STR}/community/posts/{{post_id}}/like"
        ]
    }
