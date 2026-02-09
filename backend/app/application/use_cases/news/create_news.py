import bleach
from app.domain.repositories.news import NewsRepository
from app.presentation.schemas.news import NewsCreate, NewsResponse, NewsStatus, NewsScope
from app.infrastructure.models.news import News

class CreateNewsUseCase:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

    def execute(self, news_create: NewsCreate, author_id: str) -> NewsResponse:
        # Sanitize content if present
        cleaned_content = None
        if news_create.content:
            cleaned_content = bleach.clean(
                news_create.content,
                tags=['p', 'b', 'i', 'u', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'a', 'br'],
                attributes={'a': ['href', 'title', 'target']}
            )

        news = News(
            title=news_create.title,
            summary=news_create.summary,
            content=cleaned_content,
            scope=news_create.scope.value,
            status=NewsStatus.DRAFT.value,
            cover_url=news_create.cover_url,
            author_id=author_id
        )

        saved_news = self.news_repository.save(news)
        return NewsResponse.model_validate(saved_news)
