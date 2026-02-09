from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.db import Base
import uuid
import enum

class NewsStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class NewsScope(str, enum.Enum):
    GENERAL = "GENERAL"
    INTERNAL = "INTERNAL"

class News(Base):
    __tablename__ = "news"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    scope = Column(String, nullable=False, default=NewsScope.GENERAL.value) # Storing as String for simplicity but using Enum in code
    status = Column(String, nullable=False, default=NewsStatus.DRAFT.value)
    cover_url = Column(String, nullable=True)
    
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Relationship
    author = relationship("User", back_populates="news_articles")

    def __repr__(self):
        return f"<News(title={self.title}, status={self.status})>"
