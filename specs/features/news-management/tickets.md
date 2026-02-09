# News Management — Implementation Tickets

**Feature:** News Management (Módulo de Noticias)
**Slug:** news-management
**Dependencies:**
- Minimal User Logic (Stub needed until User Management is full).
- Rich Text Editor (React Quill or similar) for Frontend.

---

### Story: NM-ADM-001 — Create News Draft
**Source**: `user-stories.md`
**Key Scenarios**: Successful Draft Creation, Validation Failure, Security/Sanitization.

#### Tickets for NM-ADM-001

1. - [x] **NM-ADM-001-DB-T01 — Create News Schema and User Stub** (2026-02-09)
   - **Type**: DB
   - **Description**: Initialize the database schema for the News feature. Since User Management is pending, strictly create a minimal `users` table stub to support foreign keys.
     - Create `users` table (id, email, role). Seed a default admin.
     - Create `news` table (id, title, summary, content, scope, status, published_at, created_at, updated_at, author_id, is_deleted).
     - Add indexes on `published_at` and `status`.
   - **Scope**: Included: Migration script, Seeds.
   - **Dependencies**: None.
   - **Deliverables**: Alembic revision, updated `DataModel.md`.

2. - [x] **NM-ADM-001-BE-T02 — Implement Create News Endpoint** (2026-02-09)
   - **Type**: BE
   - **Description**: backend logic to create a news entry in `DRAFT` status.
     - Endpoint: `POST /api/v1/news`
     - Logic: Validate input (title required), Sanitize HTML content (bleach), defaults status to DRAFT.
     - RBAC: Role `ADMIN` required.
   - **Scope**: Included: Pydantic models, Use Case, Router, Tests.
   - **Dependencies**: NM-ADM-001-DB-T01.
   - **Deliverables**: Code, Tests (Status 201).

3. - [ ] **NM-ADM-001-FE-T03 — Implement News Creation Form**
   - **Type**: FE
   - **Description**: UI for administrators to create news.
     - Route: `/admin/news/create`
     - Components: Title input, Summary Textarea, Rich Text Editor (React Quill/TipTap), Scope Selector.
     - Integration: Call `POST /api/v1/news`.
     - Validation: Zod schema (Title required).
   - **Scope**: Included: Form Page, API integration, Toast notification.
   - **Dependencies**: NM-ADM-001-BE-T02.
   - **Deliverables**: Working UI, E2E Test (Happy Path).

---

### Story: NM-ADM-002 — Edit News Article
**Source**: `user-stories.md`
**Key Scenarios**: Edit Draft, Edit Published Item.

#### Tickets for NM-ADM-002

1. - [ ] **NM-ADM-002-DB-T01 — Verify Schema for Updates**
   - **Type**: DB
   - **Description**: Validate that existing schema supports updates. No schema change expected, but ensure `updated_at` trigger (or logic) works.
   - **Scope**: Validation only.
   - **Dependencies**: NM-ADM-001-DB-T01.
   - **Deliverables**: Confirmed schema capability.

2. - [ ] **NM-ADM-002-BE-T02 — Implement Update News Endpoint**
   - **Type**: BE
   - **Description**: Backend logic to update existing news.
     - Endpoint: `PUT /api/v1/news/{id}`
     - Logic: Partial updates allowed. Note: Status change handled in separate endpoint? Or allowed here? Story says "update content". Keep status separate for safety, or allow drafts to be updated seamlessly.
     - RBAC: `ADMIN` only.
   - **Scope**: Included: Use Case, Router.
   - **Dependencies**: NM-ADM-001-BE-T02.
   - **Deliverables**: Endpoint, Tests.

3. - [ ] **NM-ADM-002-FE-T03 — Implement News Edit Form**
   - **Type**: FE
   - **Description**: UI to edit news. Can reuse Creation Form in "Edit Mode".
     - Route: `/admin/news/{id}/edit`
     - Logic: Fetch existing data, pre-fill form, submit PUT.
   - **Scope**: Included: Edit Page customization.
   - **Dependencies**: NM-ADM-002-BE-T02.
   - **Deliverables**: UI, Tests.

---

### Story: NM-ADM-003 — Publish and Archive News
**Source**: `user-stories.md`
**Key Scenarios**: Publishing a Draft, Archiving News.

#### Tickets for NM-ADM-003

1. - [ ] **NM-ADM-003-DB-T01 — Status Transition Constraints**
   - **Type**: DB
   - **Description**: Ensure `status` column accepts DRAFT, PUBLISHED, ARCHIVED. (Already defined in T01, just verification).
   - **Scope**: Validation.
   - **Dependencies**: NM-ADM-001-DB-T01.

2. - [ ] **NM-ADM-003-BE-T02 — Implement Status Change Endpoint**
   - **Type**: BE
   - **Description**: Specialized endpoint for workflow transitions.
     - Endpoint: `PATCH /api/v1/news/{id}/status`
     - Body: `{ status: "PUBLISHED" }`
     - Logic: Set `published_at` if transitioning to PUBLISHED.
   - **Scope**: Included: Transition logic.
   - **Dependencies**: NM-ADM-002-BE-T02.

3. - [ ] **NM-ADM-003-FE-T03 — Implement Publishing Actions**
   - **Type**: FE
   - **Description**: Add "Publish", "Unpublish/Archive" buttons to the UI (List or Detail view).
   - **Scope**: Action buttons, API integration.
   - **Dependencies**: NM-ADM-003-BE-T02.

---

### Story: NM-ADM-004 — Soft Delete News
**Source**: `user-stories.md`
**Key Scenarios**: Soft Delete, Audit Log.

#### Tickets for NM-ADM-004

1. - [ ] **NM-ADM-004-BE-T01 — Implement Delete Endpoint**
   - **Type**: BE
   - **Description**: Soft delete implementation.
     - Endpoint: `DELETE /api/v1/news/{id}`
     - Logic: Set `is_deleted=True`. Do not hard delete.
   - **Scope**: Included: Soft delete logic, filtering deleted items from other queries.
   - **Dependencies**: NM-ADM-001-BE-T02.

2. - [ ] **NM-ADM-004-FE-T02 — Implement Delete Action**
   - **Type**: FE
   - **Description**: Delete button with Confirmation Modal in Admin List.
   - **Scope**: included: UI Interactivity.
   - **Dependencies**: NM-ADM-004-BE-T01.

---

### Story: NM-VIS-001 — View General News List
**Source**: `user-stories.md`
**Key Scenarios**: Public List Filtering, Sorting and Pagination.

#### Tickets for NM-VIS-001

1. - [ ] **NM-VIS-001-BE-T01 — Implement Public List Endpoint**
   - **Type**: BE
   - **Description**: Publicly accessible endpoint for news.
     - Endpoint: `GET /api/v1/news`
     - Logic: Filter `status=PUBLISHED` AND `scope=GENERAL`. Filter `is_deleted=False`.
     - Pagination: `limit` / `offset`.
     - Ordering: `published_at DESC`.
     - RBAC: Public (No auth required).
   - **Scope**: Included: Repository filters, API.
   - **Dependencies**: NM-ADM-001-BE-T02.

2. - [ ] **NM-VIS-001-FE-T02 — Implement Public News Feed**
   - **Type**: FE
   - **Description**: Public landing page or News section component.
     - Components: `NewsCard` (Title, Summary, Cover, Date).
     - Page: `NewsFeedPage` with infinite scroll or pagination.
   - **Scope**: Included: UI Display.
   - **Dependencies**: NM-VIS-001-BE-T01.

---

### Story: NM-VIS-002 — View News Detail
**Source**: `user-stories.md`
**Key Scenarios**: View Public Detail, Access Control Denial.

#### Tickets for NM-VIS-002

1. - [ ] **NM-VIS-002-BE-T01 — Implement Public Detail Endpoint**
   - **Type**: BE
   - **Description**: Get single news item.
     - Endpoint: `GET /api/v1/news/{id}`
     - Logic: Ensure item is PUBLISHED and GENERAL. If Internal -> 403 (or 404).
   - **Scope**: included: Security check.
   - **Dependencies**: NM-VIS-001-BE-T01.

2. - [ ] **NM-VIS-002-FE-T02 — Implement News Detail Page**
   - **Type**: FE
   - **Description**: Dedicated page for reading a news item.
     - Route: `/news/{id}` and `/news/{slug}` (if slug implemented, otherwise ID).
     - Component: Full content renderer (sanitize HTML again on frontend just in case, or trust backend).
   - **Scope**: Included: Page layout.
   - **Dependencies**: NM-VIS-002-BE-T01.

---

### Story: NM-MEM-001 — View Internal News
**Source**: `user-stories.md`
**Key Scenarios**: Combined List, Internal Detail Access.

#### Tickets for NM-MEM-001

1. - [ ] **NM-MEM-001-BE-T01 — internal News Access Logic**
   - **Type**: BE
   - **Description**: Adjust List Logic for Authenticated Members.
     - Logic: If User has role `MEMBER` or `ADMIN`, include `scope=INTERNAL` in the query.
     - Detail Endpoint: Allow access to INTERNAL items if role is sufficient.
   - **Scope**: Included: Repository adjustment, Security logic.
   - **Dependencies**: NM-VIS-001-BE-T01.

2. - [ ] **NM-MEM-001-FE-T02 — Update Feed for Members**
   - **Type**: FE
   - **Description**: Verify and display Internal news with a badge (e.g., "Members Only").
     - Component: Add scope indicator on cards.
   - **Scope**: Included: UI enhancements.
   - **Dependencies**: NM-MEM-001-BE-T01.
