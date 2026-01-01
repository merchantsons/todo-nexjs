# Task CRUD Feature Specification — Evolution of Todo (Phase II)

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Approved  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution Article VII (Security Mandates)

---

## Overview

This document defines the Task CRUD (Create, Read, Update, Delete) feature for Evolution of Todo Phase II, establishing user stories, acceptance criteria, API contracts, and security requirements for todo management operations.

**Feature Scope**: Complete task lifecycle management with user isolation  
**Operations**: Create, List, View, Update, Delete, Toggle Completion  
**Security Model**: User-scoped queries (users can only access their own tasks)

---

## Feature Scope

### In Scope (Phase II)
- ✅ Create new task with title and description
- ✅ List all user's tasks
- ✅ View single task details
- ✅ Update task title, description, and completion status
- ✅ Delete task permanently
- ✅ Toggle task completion status
- ✅ User isolation (cannot access other users' tasks)

### Out of Scope (Phase II)
- ❌ Task sharing between users — Phase III
- ❌ Task assignment — Phase III
- ❌ Task categories/tags — Phase III
- ❌ Task due dates — Phase III
- ❌ Task priorities — Phase III
- ❌ Task search/filtering — Phase III
- ❌ Task sorting (other than chronological) — Phase III
- ❌ Soft delete / trash — Phase III

---

## User Stories

### US-TASK-001: Create Task

**As a** logged-in user  
**I want to** create a new todo task with a title and optional description  
**So that** I can track things I need to do

**Acceptance Criteria**:
- ✅ User can access task creation form on dashboard
- ✅ User can enter task title (required, max 255 chars)
- ✅ User can enter task description (optional, max 10,000 chars)
- ✅ Title field is required and validated
- ✅ Upon submission, task is created in database with user_id from JWT
- ✅ New task appears in task list immediately
- ✅ Task defaults to "not completed" status
- ✅ Timestamps (created_at, updated_at) are auto-populated

**API Endpoint**: `POST /api/{user_id}/tasks`

**Security Requirements**:
- ✅ JWT required (401 if missing/invalid)
- ✅ user_id in path must match JWT claim
- ✅ Task created with authenticated user_id (not from request body)

**Skills Used**: `user-scoped-query.md`

---

### US-TASK-002: List Tasks

**As a** logged-in user  
**I want to** see all my todo tasks  
**So that** I can review what I need to do

**Acceptance Criteria**:
- ✅ User can view task list on dashboard
- ✅ All user's tasks are displayed (chronological order, newest first)
- ✅ Each task shows: title, description (truncated if long), completion status
- ✅ Empty state message displayed if user has no tasks
- ✅ Completed tasks visually distinct from incomplete tasks
- ✅ User CANNOT see other users' tasks

**API Endpoint**: `GET /api/{user_id}/tasks`

**Security Requirements**:
- ✅ JWT required (401 if missing/invalid)
- ✅ user_id in path must match JWT claim
- ✅ Database query filters by authenticated user_id
- ✅ Returns empty array (not 404) if user has no tasks

**Skills Used**: `user-scoped-query.md`

---

### US-TASK-003: View Task Details

**As a** logged-in user  
**I want to** view full details of a specific task  
**So that** I can see complete information including long descriptions

**Acceptance Criteria**:
- ✅ User can click task to view full details
- ✅ Full title and description displayed
- ✅ Completion status visible
- ✅ Creation and update timestamps visible
- ✅ User can return to task list
- ✅ Returns 404 if task doesn't exist or belongs to another user

**API Endpoint**: `GET /api/{user_id}/tasks/{id}`

**Security Requirements**:
- ✅ JWT required (401 if missing/invalid)
- ✅ user_id in path must match JWT claim
- ✅ Database query filters by user_id AND task id
- ✅ Returns 404 (not 403) if task not found or not owned

**Skills Used**: `user-scoped-query.md`

---

### US-TASK-004: Update Task

**As a** logged-in user  
**I want to** edit a task's title, description, or completion status  
**So that** I can correct mistakes or update details

**Acceptance Criteria**:
- ✅ User can click edit button on task
- ✅ Form pre-populated with current task data
- ✅ User can modify title, description, completion status
- ✅ Title remains required (cannot be empty)
- ✅ Upon submission, task is updated in database
- ✅ updated_at timestamp is refreshed
- ✅ User redirected back to task list with updated data
- ✅ Returns 404 if task doesn't exist or belongs to another user

**API Endpoint**: `PUT /api/{user_id}/tasks/{id}`

**Security Requirements**:
- ✅ JWT required (401 if missing/invalid)
- ✅ user_id in path must match JWT claim
- ✅ Database query verifies ownership before update
- ✅ Returns 404 (not 403) if task not found or not owned

**Skills Used**: `user-scoped-query.md`

---

### US-TASK-005: Delete Task

**As a** logged-in user  
**I want to** delete a task permanently  
**So that** I can remove tasks I no longer need

**Acceptance Criteria**:
- ✅ User can click delete button on task
- ✅ Confirmation dialog appears ("Are you sure?")
- ✅ Upon confirmation, task is permanently deleted from database
- ✅ Task disappears from task list immediately
- ✅ No undo functionality (permanent delete in Phase II)
- ✅ Returns 404 if task doesn't exist or belongs to another user

**API Endpoint**: `DELETE /api/{user_id}/tasks/{id}`

**Security Requirements**:
- ✅ JWT required (401 if missing/invalid)
- ✅ user_id in path must match JWT claim
- ✅ Database query verifies ownership before delete
- ✅ Returns 404 (not 403) if task not found or not owned

**Skills Used**: `user-scoped-query.md`

---

### US-TASK-006: Toggle Task Completion

**As a** logged-in user  
**I want to** quickly mark a task as complete or incomplete  
**So that** I can track my progress without full edit form

**Acceptance Criteria**:
- ✅ User can click checkbox/toggle button on task
- ✅ Task completion status toggles immediately
- ✅ Visual feedback (e.g., strikethrough for completed tasks)
- ✅ Database updated with new completion status
- ✅ updated_at timestamp is refreshed
- ✅ No page reload required (optimistic UI update)
- ✅ Returns 404 if task doesn't exist or belongs to another user

**API Endpoint**: `PATCH /api/{user_id}/tasks/{id}/complete`

**Security Requirements**:
- ✅ JWT required (401 if missing/invalid)
- ✅ user_id in path must match JWT claim
- ✅ Database query verifies ownership before update
- ✅ Returns 404 (not 403) if task not found or not owned

**Skills Used**: `user-scoped-query.md`

---

## Data Model

### Task Entity

```typescript
interface Task {
  id: number;                    // Primary key (auto-increment)
  user_id: number;               // Owner ID (from JWT)
  title: string;                 // Required, max 255 chars
  description: string | null;    // Optional, max 10,000 chars
  completed: boolean;            // Default false
  created_at: string;            // ISO 8601 timestamp (UTC)
  updated_at: string;            // ISO 8601 timestamp (UTC)
}
```

### Validation Rules

| Field | Rules |
|-------|-------|
| `title` | Required, not empty, max 255 characters, trimmed |
| `description` | Optional, max 10,000 characters, trimmed |
| `completed` | Boolean only (true/false) |
| `user_id` | Must match authenticated JWT user_id |

---

## API Contracts

### Create Task

**Request**:
```http
POST /api/123/tasks HTTP/1.1
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-02T10:00:00Z",
  "updated_at": "2026-01-02T10:00:00Z"
}
```

---

### List Tasks

**Request**:
```http
GET /api/123/tasks HTTP/1.1
Authorization: Bearer <JWT>
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": 123,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-02T10:00:00Z",
    "updated_at": "2026-01-02T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": 123,
    "title": "Finish hackathon",
    "description": null,
    "completed": true,
    "created_at": "2026-01-02T11:00:00Z",
    "updated_at": "2026-01-02T12:00:00Z"
  }
]
```

---

### Get Single Task

**Request**:
```http
GET /api/123/tasks/1 HTTP/1.1
Authorization: Bearer <JWT>
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-02T10:00:00Z",
  "updated_at": "2026-01-02T10:00:00Z"
}
```

---

### Update Task

**Request**:
```http
PUT /api/123/tasks/1 HTTP/1.1
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "title": "Buy groceries and cook",
  "description": "Milk, eggs, bread, vegetables",
  "completed": false
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Buy groceries and cook",
  "description": "Milk, eggs, bread, vegetables",
  "completed": false,
  "created_at": "2026-01-02T10:00:00Z",
  "updated_at": "2026-01-02T15:30:00Z"
}
```

---

### Delete Task

**Request**:
```http
DELETE /api/123/tasks/1 HTTP/1.1
Authorization: Bearer <JWT>
```

**Response** (204 No Content):
```
(Empty response body)
```

---

### Toggle Completion

**Request**:
```http
PATCH /api/123/tasks/1/complete HTTP/1.1
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "completed": true
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-02T10:00:00Z",
  "updated_at": "2026-01-02T16:00:00Z"
}
```

---

## UI/UX Patterns

### Task List View

**Layout**:
```
┌─────────────────────────────────────────────┐
│  Evolution of Todo             [Logout]     │
├─────────────────────────────────────────────┤
│  [+ New Task]                               │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ ☐ Buy groceries            [Edit] [X]│   │
│  │   Milk, eggs, bread...               │   │
│  │   Created: 2 hours ago               │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │ ☑ Finish hackathon         [Edit] [X]│   │
│  │   (strikethrough style)              │   │
│  │   Completed: 1 hour ago              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Empty State

**Message**: "No tasks yet. Create your first task to get started!"  
**Action Button**: "Create Task"

### Task Form (Create/Edit)

**Fields**:
- Title (text input, required)
- Description (textarea, optional)
- Completed (checkbox, edit mode only)

**Actions**:
- Save button (primary)
- Cancel button (secondary)

---

## Error Handling

### Frontend Error Messages

| Scenario | User-Facing Message |
|----------|---------------------|
| Title empty | "Title is required" |
| Title too long | "Title must be 255 characters or less" |
| Description too long | "Description must be 10,000 characters or less" |
| Network error | "Unable to save task. Please try again." |
| Unauthorized | (Redirect to login) |
| Not found | "Task not found" |

### Backend Error Responses

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Missing title | `{"detail": "Field required: title"}` |
| 400 | Title too long | `{"detail": "Title must be 255 characters or less"}` |
| 401 | Missing/invalid JWT | `{"detail": "Unauthorized"}` |
| 401 | user_id mismatch | `{"detail": "Unauthorized"}` |
| 404 | Task not found/not owned | `{"detail": "Task not found"}` |

---

## Security Requirements

### User Isolation (CRITICAL)

**Enforcement Points**:
1. ✅ API middleware validates JWT and extracts user_id
2. ✅ Path parameter user_id must match JWT user_id
3. ✅ Database queries ALWAYS filter by authenticated user_id
4. ✅ Return 404 (not 403) for unauthorized access attempts

**Test Cases**:
- ❌ User A cannot list User B's tasks
- ❌ User A cannot view User B's task by ID
- ❌ User A cannot update User B's task
- ❌ User A cannot delete User B's task
- ❌ User A cannot toggle User B's task completion

**Skills Used**: `user-scoped-query.md`

### Input Validation

**Frontend**:
- Client-side validation for immediate feedback
- Max length constraints enforced
- Required field validation

**Backend**:
- Pydantic models validate all inputs
- Max length constraints enforced
- SQL injection prevented (ORM parameterized queries)

---

## Performance Requirements

| Operation | Target Response Time (p95) |
|-----------|----------------------------|
| List tasks | < 200ms |
| Create task | < 150ms |
| Get single task | < 100ms |
| Update task | < 150ms |
| Delete task | < 100ms |
| Toggle completion | < 100ms |

**Optimization Strategies**:
- Database indexes on user_id
- Connection pooling (SQLModel default)
- Minimal data transfer (no unnecessary fields)

---

## Testing Strategy

### Manual Test Cases

#### Test 1: Create Task Success
1. Log in as User A
2. Click "New Task"
3. Enter title: "Test task"
4. Enter description: "Test description"
5. Submit
6. **Expected**: Task appears in list, success message

#### Test 2: Create Task Empty Title
1. Click "New Task"
2. Leave title empty
3. Submit
4. **Expected**: Error "Title is required"

#### Test 3: List Tasks User Isolation
1. Log in as User A, create task "A's task"
2. Log out, log in as User B, create task "B's task"
3. **Expected**: User A only sees "A's task", User B only sees "B's task"

#### Test 4: View Task Details
1. Log in, create task
2. Click task to view details
3. **Expected**: Full title and description displayed

#### Test 5: Update Task Success
1. Log in, create task
2. Click edit, change title to "Updated"
3. Submit
4. **Expected**: Task updated, new title displayed

#### Test 6: Delete Task Success
1. Log in, create task
2. Click delete, confirm
3. **Expected**: Task removed from list

#### Test 7: Toggle Completion
1. Log in, create task (incomplete)
2. Click checkbox
3. **Expected**: Task marked complete, visual feedback
4. Click checkbox again
5. **Expected**: Task marked incomplete

#### Test 8: Unauthorized Access (Security)
1. Log in as User A, note task ID
2. Log out, log in as User B
3. Manually navigate to User A's task ID
4. **Expected**: 404 error or redirect

---

## Phase Compliance

### Phase II Allowed ✅
- ✅ Basic CRUD operations (Create, Read, Update, Delete)
- ✅ Task completion toggle
- ✅ User isolation
- ✅ Simple list view (chronological)

### Phase II Forbidden ❌
- ❌ Task sharing/collaboration
- ❌ Task assignment to other users
- ❌ Categories, tags, priorities
- ❌ Due dates and reminders
- ❌ Advanced search/filtering
- ❌ Custom sorting
- ❌ Soft delete/trash

**Constitutional Compliance**: ✅ This feature adheres to Article VII (Security Mandates)

---

## References

- Constitution: `.specify/memory/constitution.md` (Article VII)
- Architecture: `specs/architecture.md`
- Database Schema: `specs/database/schema.md`
- API Specification: `specs/api/rest-endpoints.md`
- Skills: `.claude/skills/user-scoped-query.md`

---

**Status**: ✅ Approved for Implementation  
**Next Step**: Proceed to UI specifications (pages and components)

