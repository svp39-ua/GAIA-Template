# NM-ADM-001-FE-T03 — Implementation Plan

**Source ticket**: `specs/features/news-management/tickets.md` → **NM-ADM-001-FE-T03**  
**Related user story**: **NM-ADM-001** (from `specs/features/news-management/user-stories.md`)  
**Plan version**: v1.0 — 2026-02-09  
**Traceability**: All tasks must include inline references to `NM-ADM-001-FE-T03`.

---

## 1) Context & Objective
- **Ticket summary**: Implement the "Create News" form for administrators. This is the first frontend ticket, so it typically requires checking/scaffolding the frontend foundation.
- **Impacted entities**: `News` (Via API).
- **Impacted services**: 
  - `frontend/src/features/news` (New module)
  - `frontend/src/components/ui` (Shadcn components)
  - `frontend/src/lib/api` (API Client)
- **Impacted tests**: 
  - `NM-ADM-001`: Scenario 1 (Successful Draft), Scenario 2 (Validation).

## 2) Scope
- **In scope**: 
  - Check/Initialize Frontend Project (Vite + React + TS).
  - Install dependencies (Tailwind, Shadcn, React Hook Form, Zod, Tiptap, TanStack Query, Axios).
  - Create Admin Layout (minimal shell).
  - Create `NewsCreatePage` with form.
  - Integrate with `POST /api/v1/news`.
  - Toast notifications for success/error.
- **Out of scope**: 
  - Edit/Delete (separate tickets).
  - Image upload (url input only).
  - Authentication (Mock auth header for now).
- **Assumptions**: 
  - Backend `POST /api/v1/news` is ready (Verified in previous ticket).
  - Node.js is installed.

## 3) Detailed Work Plan (TDD + BDD)

### 3.1 Test-first sequencing
1.  **Definitions**
    - Define Zod schema for News Form (`title`, `summary`, `content`, `scope`, `cover_url`).
2.  **Test Strategy**
    - Unit Tests (Vitest): Test Zod validation rules.
    - Component Tests (RTL): Verify form rendering and submission handler call.
    - Integration: connection to mocked API.
3.  **Refactor**
    - Extract API calls to `news.service.ts`.

### 3.2 NFR hooks
- **Brand & Visuals**:
  - Use `Inter` font.
  - Primary Button: `Terracotta` (or correctly mapped variable `--primary`).
  - Spacing: 8pt grid.
  - Language: **Spanish** for all labels/placeholders (e.g., "Título", "Crear Noticia").
- **Accessibility**:
  - Labels linked to inputs.
  - Tiptap editor must be accessible (though complex, basic ARIA support).
  - Focus management on errors.

## 4) Atomic Task Breakdown

### Task 1: Initialize Frontend & Dependencies
- **Purpose**: Setup the environment.
- **Prerequisites**: Node.js.
- **Artifacts impacted**: `frontend/`, `package.json`, `vite.config.ts`, `tailwind.config.js`.
- **Test types**: Build check (`npm run build`).
- **Description**: 
  - Create React+Vite+TS project if missing.
  - Configure TailwindCSS & Shadcn/ui.
  - Install `axios`, `@tanstack/react-query`, `react-hook-form`, `zod`, `@hookform/resolvers`, `lucide-react`, `sonner` (toast).
  - Install Tiptap dependencies.

### Task 2: Implement UI Components (Shadcn)
- **Purpose**: Reusable primitives.
- **Artifacts impacted**: `frontend/src/components/ui/*` (Button, Input, Textarea, Select, Form, Card).
- **Test types**: N/A (library code).

### Task 3: Implement News API Client
- **Purpose**: Communication with Backend.
- **Artifacts impacted**: `frontend/src/lib/news-service.ts`.
- **Test types**: Unit (Mocking Axios).
- **BDD Acceptance**:
  - `createNews(data)` sends POST to `/api/v1/news` with headers.

### Task 4: Implement News Creation Form
- **Purpose**: The main feature.
- **Artifacts impacted**: `frontend/src/features/news/pages/CreateNewsPage.tsx`, `frontend/src/features/news/components/NewsForm.tsx`.
- **Test types**: Component (RTL).
- **BDD Acceptance**:
  - **Given** I am on the Create News page
  - **When** I submit empty form
  - **Then** validation error "El título es obligatorio" appears.
  - **When** I submit valid data
  - **Then** `createNews` is called and success toast appears.

### Task 5: App Routing & Layout
- **Purpose**: Navigation.
- **Artifacts impacted**: `frontend/src/App.tsx`, `frontend/src/layouts/AdminLayout.tsx`.
- **Test types**: Manual / Browser.
- **Description**: Add route `/admin/news/create` pointing to the page.

# FINAL OUTPUT & REVIEW
The user will review this document manually after generation.
