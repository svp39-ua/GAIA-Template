from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class NewsStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class NewsScope(str, Enum):
    GENERAL = "GENERAL"
    INTERNAL = "INTERNAL"

class NewsBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    summary: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = None
    scope: NewsScope = Field(default=NewsScope.GENERAL)
    cover_url: Optional[str] = None

class NewsCreate(NewsBase):
    pass

class NewsResponse(NewsBase):
    id: str
    status: NewsStatus
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    author_id: str

    model_config = ConfigDict(from_attributes=True)
