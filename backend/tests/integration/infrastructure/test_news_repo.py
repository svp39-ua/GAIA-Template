import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db import Base
from app.infrastructure.repositories.news_repository import NewsRepositoryImpl
from app.infrastructure.models.news import News, NewsStatus, NewsScope
from app.infrastructure.models.user import User

# Setup in-memory DB for integration test
engine_test = create_engine("sqlite:///:memory:")
SessionTest = sessionmaker(bind=engine_test)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine_test)
    session = SessionTest()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine_test)

def test_save_news(db):
    # Dependency: Author must exist
    author = User(email="test@example.com", role="ADMIN")
    db.add(author)
    db.commit()

    repo = NewsRepositoryImpl(db)
    news = News(
        title="Integration Test News",
        status=NewsStatus.DRAFT.value,
        scope=NewsScope.GENERAL.value,
        author_id=author.id
    )
    saved_news = repo.save(news)
    
    assert saved_news.id is not None
    assert saved_news.title == "Integration Test News"

def test_get_by_id(db):
    repo = NewsRepositoryImpl(db)
    # Create news
    news = News(
        title="Find Me",
        status=NewsStatus.DRAFT.value,
        scope=NewsScope.INTERNAL.value,
        author_id=db.query(User).first().id
    )
    repo.save(news)
    
    # Retrieve
    found = repo.get_by_id(news.id)
    assert found is not None
    assert found.title == "Find Me"
