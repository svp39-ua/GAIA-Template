import pytest
from pydantic import ValidationError
from app.presentation.schemas.news import NewsCreate, NewsResponse, NewsStatus, NewsScope

def test_news_create_valid():
    data = {
        "title": "New Event",
        "summary": "Short summary",
        "content": "<p>Content</p>",
        "scope": "GENERAL",
        "cover_url": "http://example.com/image.jpg"
    }
    news = NewsCreate(**data)
    assert news.title == "New Event"
    assert news.scope == NewsScope.GENERAL

def test_news_create_missing_title():
    data = {
        "summary": "Short summary",
        "scope": "INTERNAL"
    }
    with pytest.raises(ValidationError):
        NewsCreate(**data)

def test_news_create_invalid_scope():
    data = {"title": "Title", "scope": "INVALID"}
    with pytest.raises(ValidationError):
        NewsCreate(**data)
