from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.core.db import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False, default="MEMBER")
    
    # Relationship with News (author)
    news_articles = relationship("News", back_populates="author")

    def __repr__(self):
        return f"<User(email={self.email}, role={self.role})>"
