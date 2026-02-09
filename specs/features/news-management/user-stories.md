# User Stories: News Management

**Feature:** News Management (Módulo de Noticias)
**Epics:** Communication, Member Engagement
**Roles:** Administrator, Member, Visitor (Supporter)

## 1. Introduction
The News Management module establishes the Association App as the official communication channel. It allows Administrators to publish news with visibility scopes (General vs. Internal), ensuring sensitive information reaches only paid members while keeping the general public informed about community events.

**Key Objectives:**
- Increase Reach > 40% active users active weekly.
- Timely Communication (< 10 min from Draft to Published).

---

## 2. User Stories

### Administrator Stories

#### NM-ADM-001: Create News Draft
**As an** Administrator
**I want to** create a new news article with a title, summary, and content
**So that** I can prepare communication for the neighborhood.

**Acceptance Criteria:**
- **Scenario 1: Successful Draft Creation**
  - **Given** I am an authenticated Administrator
  - **When** I submit a new article with:
    - Title: "Annual Meeting"
    - Summary: "Discussing budget"
    - Content: "<h1>Details...</h1>"
    - Scope: "INTERNAL"
    - Status: "DRAFT" (Default)
  - **Then** the system saves the article with a unique ID
  - **And** the status is set to `DRAFT`
  - **And** the `created_at` timestamp is recorded.

- **Scenario 2: Validation Failure**
  - **Given** I am an Administrator
  - **When** I try to save an article without a `Title`
  - **Then** the system rejects the request with a "Title is required" error.

- **Scenario 3: Security / Sanitization**
  - **Given** the content includes a `<script>` tag
  - **When** the article is saved
  - **Then** the system sanitizes the input, removing the script tag to prevent XSS.

#### NM-ADM-002: Edit News Article
**As an** Administrator
**I want to** update the content, title, or cover image of an existing news item
**So that** I can correct mistakes or update information.

**Acceptance Criteria:**
- **Scenario 1: Edit Draft**
  - **Given** a news item in `DRAFT` status
  - **When** I update the `Summary` field
  - **Then** the change is persisted immediately.

- **Scenario 2: Edit Published Item**
  - **Given** a news item in `PUBLISHED` status
  - **When** I update the `Content`
  - **Then** the change is reflected immediately on the public site
  - **And** the `updated_at` timestamp is updated.

#### NM-ADM-003: Publish and Archive News
**As an** Administrator
**I want to** change the status of a news item (Draft -> Published -> Archived)
**So that** I can control when information is visible to the users.

**Acceptance Criteria:**
- **Scenario 1: Publishing a Draft**
  - **Given** a news item in `DRAFT` status
  - **When** I change status to `PUBLISHED`
  - **Then** the item becomes visible in the List API
  - **And** `published_at` is set to the current timestamp.

- **Scenario 2: Archiving News**
  - **Given** a `PUBLISHED` news item
  - **When** I change status to `ARCHIVED`
  - **Then** it is no longer returned in the standard public list.

#### NM-ADM-004: Soft Delete News
**As an** Administrator
**I want to** soft-delete a news item
**So that** I can remove erroneous entries without losing the data record audit.

**Acceptance Criteria:**
- **Scenario 1: Soft Delete**
  - **Given** a news item (Draft or Published)
  - **When** I request to delete it
  - **Then** the system marks `is_deleted = true`
  - **And** it is excluded from all standard queries (Admin/Public).

- **Scenario 2: Audit Log**
  - **When** a news item is deleted
  - **Then** the action is logged with my Admin User ID.

### Viewer Stories (Visitor / Supporter)

#### NM-VIS-001: View General News List
**As a** Visitor (Unregistered or Supporter)
**I want to** view a list of "General" news
**So that** I can stay informed about public community events.

**Acceptance Criteria:**
- **Scenario 1: Public List Filtering**
  - **Given** there are `GENERAL` and `INTERNAL` published news
  - **When** I request the news list
  - **Then** only `GENERAL` items are returned.

- **Scenario 2: Sorting and Pagination**
  - **When** I view the list
  - **Then** items are sorted by `published_at` descending
  - **And** I can load more items via pagination (e.g., page 2).

#### NM-VIS-002: View News Detail
**As a** Visitor
**I want to** read the full details of a news item
**So that** I understand the complete context.

**Acceptance Criteria:**
- **Scenario 1: View Public Detail**
  - **Given** a `PUBLISHED` news item with `GENERAL` scope
  - **When** I request its detail by ID
  - **Then** the full content, including HTML, is returned.

- **Scenario 2: Access Control Denial**
  - **Given** an `INTERNAL` news item
  - **When** I try to access it directly by ID (as a Visitor)
  - **Then** the system returns a 403 Forbidden or 404 Not Found error.

### Member Stories

#### NM-MEM-001: View Internal News
**As a** Member (Socio)
**I want to** view "Internal" news in addition to "General" news
**So that** I can participate in association decisions and assemblies.

**Acceptance Criteria:**
- **Scenario 1: Combined List**
  - **Given** I am a logged-in Member
  - **When** I request the news list
  - **Then** I see both `GENERAL` and `INTERNAL` published items.

- **Scenario 2: Internal Detail Access**
  - **Given** an `INTERNAL` news item
  - **When** I request its detail
  - **Then** the system authorizes the request and returns the full content.

---

## 3. Non-Functional Requirements Mapping

- **Security (RBAC):** 
  - `NM-ADM-*`: Requires `ROLE_ADMIN`.
  - `NM-MEM-001`: Requires `ROLE_MEMBER`.
  - `NM-VIS-*`: Public access (or `ROLE_SUPPORTER`).
  - **Constraint:** Internal news must NEVER be leaked to public API endpoints.
  
- **Performance:** 
  - List endpoint < 500ms p95.
  - Pagination required.

- **Accessibility:**
  - Semantic HTML in content (`h1`, `h2`, `p`, `ul`).
  - Alt text support for Cover Images.
