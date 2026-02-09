from abc import ABC, abstractmethod
from typing import Optional
from app.infrastructure.models.news import News

class NewsRepository(ABC):
    @abstractmethod
    def save(self, news: News) -> News:
        pass

    @abstractmethod
    def get_by_id(self, news_id: str) -> Optional[News]:
        pass
