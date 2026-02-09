# NM-ADM-001-BE-T02 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADM-001-BE-T02**  
**Related user story**: **NM-ADM-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-09  
**Traceability**: All tasks must include inline references to `NM-ADM-001-BE-T02`.

---

## 1) Context & Objective
- **Ticket summary**: Implement the backend logic to create a news entry. The endpoint must accept title, content, summary, and scope, defaulting the status to `DRAFT`. It must also sanitize HTML content to prevent XSS.
- **Impacted entities**: `News` (Insert operation).
- **Impacted services**: 
  - `application/use_cases/news/create_news.py` (New)
  - `infrastructure/repositories/news_repository.py` (New)
  - `presentation/routers/news.py` (New)
- **Impacted tests**: 
  - `NM-ADM-001`: Scenario 1 (Success), Scenario 2 (Validation), Scenario 3 (Sanitization).

## 2) Scope
- **In scope**: 
  - Pydantic DTOs (`NewsCreate`, `NewsResponse`).
  - Repository implementation for `create`.
  - Use Case with `bleach` sanitization.
  - FastAPI Route `POST /api/v1/news` with RBAC (`ROLE_ADMIN` check).
- **Out of scope**: 
  - Image upload for cover (only URL string handling for now).
  - Editing/Deleting (separate tickets).
- **Assumptions**: 
  - Auth middleware (mock or real) provides `current_user`. Since User Management is mocked, we will assume a dependency `get_current_admin` that returns a user ID if the header/token is valid.
  - `bleach` library is available (added in `requirements.txt`).

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 Test-first sequencing
1. **Define/Update tests**  
   - `tests/unit/application/test_create_news.py`: Verify Use Case logic (sanitization, defaults).
   - `tests/integration/infrastructure/test_news_repo.py`: Verify DB insertion.
   - `tests/contract/test_news_api.py`: Verify Endpoint response (201) and validation (422).
2. **Minimal implementation** 
   - Implement DTOs.
   - Implement Repository.
   - Implement Use Case.
   - Implement Router.
3. **Refactor** 
   - Ensure explicit dependency injection.

### 3.2 NFR hooks
- **Security**: 
  - **RBAC**: Endpoint must depend on `get_current_admin`.
  - **Sanitization**: Use `bleach.clean()` on `content` field.
- **Performance**: N/A for single insert.
- **Observability**: Log successful creation with News ID and Author ID.

## 4) Atomic Task Breakdown

### Task 1: Define DTOs (Schemas)
- **Purpose**: Define input/output contracts.
- **Artifacts impacted**: `backend/app/presentation/schemas/news.py`.
- **Test types**: Unit.
- **BDD Acceptance**:
  - `NewsCreate` requires `title`.
  - `NewsCreate` accepts `content`, `summary`, `scope`, `cover_url`.
  - `NewsResponse` includes `id`, `created_at`, `status`.

### Task 2: Implement News Repository
- **Purpose**: Abstract DB access.
- **Artifacts impacted**: `backend/app/infrastructure/repositories/news_repository.py`, `backend/app/domain/repositories/news.py` (Interface).
- **Test types**: Integration (`tests/integration/infrastructure/test_news_repo.py`).
- **BDD Acceptance**:
  - **Given** a valid News model
  - **When** `save` is called
  - **Then** it is persisted in the DB.

### Task 3: Implement Create News Use Case
- **Purpose**: Business logic (Sanitization, Defaults).
- **Artifacts impacted**: `backend/app/application/use_cases/news/create_news.py`.
- **Test types**: Unit (`tests/unit/application/test_create_news.py`).
- **BDD Acceptance**:
  - **Given** content with `<script>alert(1)</script>`
  - **When** executed
  - **Then** `content` is saved as `alert(1)` (tags stripped) or allowed tags only.
  - **And** `status` is `DRAFT`.

### Task 4: Implement API Endpoint and RBAC
- **Purpose**: Expose functionality via HTTP.
- **Artifacts impacted**: `backend/app/presentation/routers/news.py`, `backend/app/presentation/dependencies/auth.py` (Admin Mock).
- **Test types**: Contract/E2E (`tests/contract/test_news_api.py`).
- **BDD Acceptance**:
  - **Given** valid payload and Admin auth
  - **When** `POST /api/v1/news`
  - **Then** 201 Created is returned.
  - **Given** missing title
  - **Then** 422 Unprocessable Entity.
