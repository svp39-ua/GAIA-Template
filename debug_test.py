import sys
import os
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    print("Importing modules...")
    from app.presentation.schemas.news import NewsCreate, NewsScope
    from app.application.use_cases.news.create_news import CreateNewsUseCase
    from app.infrastructure.models.news import News, NewsStatus
    import bleach
    print("Imports successful.")

    print("Testing Use Case Logic...")
    from unittest.mock import Mock
    
    def mock_save(news):
        news.id = "test-id"
        news.created_at = datetime.now()
        news.updated_at = datetime.now()
        return news

    repo = Mock()
    repo.save.side_effect = mock_save
    
    use_case = CreateNewsUseCase(repo)
    payload = NewsCreate(title="Test", content="<script>alert(1)</script><p>Safe</p>", scope=NewsScope.GENERAL)
    result = use_case.execute(payload, "admin")
    
    if "<script>" in result.content:
        print("FAIL: Script tag not removed.")
        sys.exit(1)
    if "<p>Safe</p>" not in result.content:
        print("FAIL: Safe content removed.")
        sys.exit(1)
    if result.id != "test-id":
         print("FAIL: ID not populated.")
         sys.exit(1)
         
    print("Use Case Logic PASS.")

except Exception as e:
    print(f"FAIL: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
