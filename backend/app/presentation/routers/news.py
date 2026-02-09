from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.presentation.schemas.news import NewsCreate, NewsResponse
from app.application.use_cases.news.create_news import CreateNewsUseCase
from app.infrastructure.repositories.news_repository import NewsRepositoryImpl
# from app.presentation.dependencies.auth import get_current_admin # TODO: Mock or Implement

router = APIRouter()

# Mock auth dependency for now until UM is ready
def get_current_admin():
    return "admin-user-id" # Placeholder

def get_news_repository(db: Session = Depends(get_db)):
    return NewsRepositoryImpl(db)

def get_create_news_use_case(repo: NewsRepositoryImpl = Depends(get_news_repository)):
    return CreateNewsUseCase(repo)

@router.post("/news", response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
def create_news(
    news_create: NewsCreate,
    use_case: CreateNewsUseCase = Depends(get_create_news_use_case),
    current_user_id: str = Depends(get_current_admin)
):
    try:
        return use_case.execute(news_create, current_user_id)
    except Exception as e:
        # Log error
        raise HTTPException(status_code=500, detail=str(e))
