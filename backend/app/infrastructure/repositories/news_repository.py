from sqlalchemy.orm import Session
from typing import Optional
from app.domain.repositories.news import NewsRepository
from app.infrastructure.models.news import News

class NewsRepositoryImpl(NewsRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, news: News) -> News:
        self.db.add(news)
        self.db.commit()
        self.db.refresh(news)
        return news

    def get_by_id(self, news_id: str) -> Optional[News]:
        return self.db.query(News).filter(News.id == news_id).first()
