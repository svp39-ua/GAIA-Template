# Data Model

## Conceptual ER Diagram

```mermaid
erDiagram
    User ||--o{ News : creates
    
    User {
        UUID id PK
        String email UK
        String role "ADMIN, MEMBER"
    }

    News {
        UUID id PK
        String title
        String summary
        Text content
        String scope "GENERAL, INTERNAL"
        String status "DRAFT, PUBLISHED, ARCHIVED"
        String cover_url
        DateTime published_at
        DateTime created_at
        DateTime updated_at
        Boolean is_deleted
        UUID author_id FK
    }
```

## Description of Entities

### User (Stub)
Represents a user of the system. Currently minimal to support News authorship.
- **id**: Unique identifier (UUID).
- **email**: User's email address.
- **role**: Authorization role (Admin allows full access).

### News
Represents a news article or announcement.
- **status**: Workflow state (DRAFT -> PUBLISHED -> ARCHIVED).
- **scope**: Visibility restriction (GENERAL=Public, INTERNAL=Members Only).
- **is_deleted**: Soft-delete flag (true = hidden).
