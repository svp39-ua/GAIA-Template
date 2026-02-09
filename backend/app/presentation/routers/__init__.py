from fastapi import APIRouter
from app.presentation.routers import news

api_router = APIRouter()
api_router.include_router(news.router, tags=["news"])
