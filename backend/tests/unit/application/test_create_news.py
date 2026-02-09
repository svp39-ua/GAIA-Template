import pytest
from unittest.mock import Mock
from app.application.use_cases.news.create_news import CreateNewsUseCase
from app.presentation.schemas.news import NewsCreate, NewsScope
from app.infrastructure.models.news import News, NewsStatus

def test_create_news_sanitization():
    repo = Mock()
    repo.save.side_effect = lambda x: x # Return the inputs for inspection
    
    use_case = CreateNewsUseCase(repo)
    
    payload = NewsCreate(
        title="Test",
        content="<script>alert(1)</script><p>Safe</p>",
        scope=NewsScope.GENERAL
    )
    
    result = use_case.execute(payload, "admin-id")
    
    # Verify content was sanitized (script removed)
    assert "<script>" not in result.content
    assert "alert(1)" in result.content or "alert" in result.content # Bleach might just escape or strip tags
    assert "<p>Safe</p>" in result.content
    
    # Verify defaults
    assert result.status == NewsStatus.DRAFT.value
    assert result.author_id == "admin-id"

    repo.save.assert_called_once()
