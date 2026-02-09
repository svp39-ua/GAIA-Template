from fastapi.testclient import TestClient
from app.main import app
from app.presentation.routers.news import get_create_news_use_case
from app.presentation.schemas.news import NewsResponse, NewsStatus, NewsScope
from unittest.mock import Mock
from datetime import datetime

client = TestClient(app)

def test_create_news_endpoint_success():
    # Mock Use Case
    mock_use_case = Mock()
    mock_response = NewsResponse(
        id="123",
        title="Valid Title",
        status=NewsStatus.DRAFT,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        author_id="admin-1",
        scope=NewsScope.GENERAL
    )
    mock_use_case.execute.return_value = mock_response

    # Override dependency
    app.dependency_overrides[get_create_news_use_case] = lambda: mock_use_case

    response = client.post(
        "/api/v1/news",
        json={"title": "Valid Title", "scope": "GENERAL", "content": "Start"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "123"
    assert data["title"] == "Valid Title"
    
    # Cleanup
    app.dependency_overrides = {}

def test_create_news_validation_error():
    response = client.post(
        "/api/v1/news",
        json={"scope": "GENERAL"} # Missing title
    )
    assert response.status_code == 422
