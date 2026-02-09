from app.infrastructure.models.user import User
from app.infrastructure.models.news import News

def test_user_model_structure():
    assert hasattr(User, "id")
    assert hasattr(User, "email")
    assert hasattr(User, "role")
    assert hasattr(User, "news_articles")

def test_news_model_structure():
    assert hasattr(News, "id")
    assert hasattr(News, "title")
    assert hasattr(News, "status")
    assert hasattr(News, "author_id")
    assert hasattr(News, "author")
