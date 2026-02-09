# NM-ADM-001-DB-T01 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADM-001-DB-T01**  
**Related user story**: **NM-ADM-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-09  
**Traceability**: All tasks must include inline references to `NM-ADM-001-DB-T01`.

---

## 1) Context & Objective
- **Ticket summary**: Initialize the database schema for the News feature. Since User Management is pending, strictly create a minimal `users` table stub to support foreign keys from the `news` table (`author_id`).
- **Impacted entities/tables**: 
  - `users` (New Stub)
  - `news` (New Table)
- **Impacted services/modules**: Backend (Database Layer).
- **Impacted tests**: Schema validation tests, basic persistence tests.

## 2) Scope
- **In scope**: 
  - Alembic migration creating both tables.
  - SQLAlchemy models (`User`, `News`).
  - Seeding a default Admin user (for development).
- **Out of scope**: 
  - Full User Management logic (registration, login endpoints).
  - News API endpoints (covered in BE tickets).
- **Assumptions**: 
  - `id` fields will likely use UUIDs or Integers. Using **UUID** is recommended for modern distributed systems, but we will match the project's convention if established. (Defaulting to UUID to be safe for greenfield).
  - `role` in users will be a simple String or Enum (`ADMIN`, `MEMBER`).

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 Test-first sequencing
1. **Define/Update tests**  
   - Create a test `tests/infrastructure/test_db_schema.py`.
   - Test 1: Verify `users` table exists.
   - Test 2: Verify `news` table exists.
   - Test 3: Verify Foreign Key constraint (`news.author_id` -> `users.id`).
2. **Minimal implementation** 
   - Create models in `backend/app/infrastructure/models.py` (or similar).
   - Generate Alembic revision.
   - Run migration.
3. **Refactor** 
   - Update `specs/DataModel.md` with the new schema.

### 3.2 NFR hooks
- **Security**: N/A (Schema only).
- **Performance**: Indexes on `news.published_at` and `news.status` for efficient sorting/filtering.
- **Observability**: `created_at` and `updated_at` columns audit data freshness.

## 4) Atomic Task Breakdown

### Task 1: Initialize Database Models
- **Purpose**: Define SQLAlchemy models for `User` (stub) and `News`.
- **Prerequisites**: Docker DB container running.
- **Artifacts impacted**: `backend/app/infrastructure/models/user.py`, `backend/app/infrastructure/models/news.py`.
- **Test types**: Unit (Import check).
- **BDD Acceptance**:
  - **Given** the models are defined
  - **When** I inspect the metadata
  - **Then** columns `title`, `summary`, `content`, `status`, `scope` exist on News.

### Task 2: Create Layout and Migration
- **Purpose**: Generate and apply the database schema changes.
- **Prerequisites**: Task 1.
- **Artifacts impacted**: `backend/alembic/versions/*_create_news_tables.py`.
- **Test types**: Integration (Migration run).
- **BDD Acceptance**:
  - **Given** a clean database
  - **When** I run `alembic upgrade head`
  - **Then** the tables `users` and `news` are created in Postgres.

### Task 3: Seed Default Admin
- **Purpose**: Ensure development environment is usable immediately.
- **Prerequisites**: Task 2.
- **Artifacts impacted**: `backend/app/infrastructure/seeds.py` (or equivalent).
- **Test types**: Integration.
- **BDD Acceptance**:
  - **Given** the migration is applied
  - **When** I run the seed script
  - **Then** a user with role `ADMIN` exists in the `users` table.

### Task 4: Documentation Update
- **Purpose**: Keep the Single Source of Truth updated.
- **Prerequisites**: Task 3.
- **Artifacts impacted**: `specs/DataModel.md`.
- **Test types**: Manual Review.
- **BDD Acceptance**:
  - **Given** the new schema is active
  - **When** I read `DataModel.md`
  - **Then** it accurately reflects the fields and types implementation.
