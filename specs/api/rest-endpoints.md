# REST API Specification — Evolution of Todo (Phase II)

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Approved  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution Article VII (Security Mandates)

---

## Overview

This document defines the complete RESTful API specification for Evolution of Todo Phase II backend, establishing endpoint contracts, request/response formats, authentication requirements, and error handling.

**Base URL**: `http://localhost:8000` (development) or `https://api.yourdomain.com` (production)  
**API Prefix**: `/api`  
**Authentication**: JWT Bearer token (required on all endpoints)  
**Content-Type**: `application/json`

---

## Authentication

### Required Header

All endpoints MUST include:

```
Authorization: Bearer <JWT_TOKEN>
```

### JWT Claims Structure

```json
{
  "user_id": 123,
  "email": "user@example.com",
  "iat": 1735819200,
  "exp": 1735905600
}
```

**Critical**: Backend MUST extract `user_id` from JWT claims, NEVER from request body or path parameters

### Authentication Errors

| Status | Error Code | Description |
|--------|------------|-------------|
| 401 | `MISSING_TOKEN` | No Authorization header provided |
| 401 | `INVALID_TOKEN` | JWT signature verification failed |
| 401 | `EXPIRED_TOKEN` | JWT has expired |
| 401 | `MALFORMED_TOKEN` | JWT structure is invalid |

**Skills Used**: `secure-jwt-guard.md`

---

## API Endpoints Summary

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/health` | Health check | ❌ No |
| GET | `/api/{user_id}/tasks` | List user's tasks | ✅ Yes |
| POST | `/api/{user_id}/tasks` | Create new task | ✅ Yes |
| GET | `/api/{user_id}/tasks/{id}` | Get specific task | ✅ Yes |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | ✅ Yes |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | ✅ Yes |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | ✅ Yes |

---

## Endpoint: Health Check

### `GET /api/health`

**Purpose**: Verify API availability (no authentication required)

**Request**:
```http
GET /api/health HTTP/1.1
Host: localhost:8000
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-01-02T12:00:00Z",
  "version": "1.0.0"
}
```

**Errors**: None (always returns 200)

---

## Endpoint: List Tasks

### `GET /api/{user_id}/tasks`

**Purpose**: Retrieve all tasks belonging to authenticated user

**Authentication**: ✅ Required  
**Authorization**: JWT `user_id` claim MUST match path `{user_id}` parameter

**Request**:
```http
GET /api/123/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGc...
```

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User ID (must match JWT claim) |

**Query Parameters**: None (Phase II)

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
    "completed": false,
    "created_at": "2026-01-02T11:00:00Z",
    "updated_at": "2026-01-02T11:00:00Z"
  }
]
```

**Response** (Empty list):
```json
[]
```

**Errors**:
| Status | Condition | Response |
|--------|-----------|----------|
| 401 | JWT missing/invalid | `{"detail": "Unauthorized"}` |
| 401 | JWT user_id ≠ path user_id | `{"detail": "Unauthorized"}` |

**Security Requirements**:
- ✅ Query MUST filter by authenticated user_id
- ✅ NEVER return other users' tasks
- ✅ Return empty array (not 404) if user has no tasks

**Skills Used**: `user-scoped-query.md`

---

## Endpoint: Create Task

### `POST /api/{user_id}/tasks`

**Purpose**: Create new task for authenticated user

**Authentication**: ✅ Required  
**Authorization**: JWT `user_id` claim MUST match path `{user_id}` parameter

**Request**:
```http
POST /api/123/tasks HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "New task",
  "description": "Optional description"
}
```

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User ID (must match JWT claim) |

**Request Body**:
```json
{
  "title": "string (required, max 255 chars)",
  "description": "string (optional, can be null)"
}
```

**Validation Rules**:
| Field | Rules |
|-------|-------|
| `title` | Required, not empty, max 255 characters |
| `description` | Optional, max 10,000 characters |

**Response** (201 Created):
```json
{
  "id": 3,
  "user_id": 123,
  "title": "New task",
  "description": "Optional description",
  "completed": false,
  "created_at": "2026-01-02T12:00:00Z",
  "updated_at": "2026-01-02T12:00:00Z"
}
```

**Errors**:
| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Missing title | `{"detail": "Field required: title"}` |
| 400 | Title too long | `{"detail": "Title must be 255 characters or less"}` |
| 401 | JWT missing/invalid | `{"detail": "Unauthorized"}` |
| 401 | JWT user_id ≠ path user_id | `{"detail": "Unauthorized"}` |

**Security Requirements**:
- ✅ user_id MUST come from JWT claim, NOT request body
- ✅ Created task MUST belong to authenticated user
- ✅ NEVER allow creating tasks for other users

---

## Endpoint: Get Single Task

### `GET /api/{user_id}/tasks/{id}`

**Purpose**: Retrieve specific task (if owned by authenticated user)

**Authentication**: ✅ Required  
**Authorization**: JWT `user_id` claim MUST match path `{user_id}` AND task MUST belong to user

**Request**:
```http
GET /api/123/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGc...
```

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User ID (must match JWT claim) |
| `id` | integer | Yes | Task ID |

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

**Errors**:
| Status | Condition | Response |
|--------|-----------|----------|
| 401 | JWT missing/invalid | `{"detail": "Unauthorized"}` |
| 401 | JWT user_id ≠ path user_id | `{"detail": "Unauthorized"}` |
| 404 | Task not found OR not owned by user | `{"detail": "Task not found"}` |

**Security Requirements**:
- ✅ Query MUST filter by user_id AND task id
- ✅ Return 404 (not 403) if task doesn't exist OR belongs to another user
- ✅ NEVER reveal existence of other users' tasks

**Skills Used**: `user-scoped-query.md`

---

## Endpoint: Update Task

### `PUT /api/{user_id}/tasks/{id}`

**Purpose**: Update task (if owned by authenticated user)

**Authentication**: ✅ Required  
**Authorization**: JWT `user_id` claim MUST match path `{user_id}` AND task MUST belong to user

**Request**:
```http
PUT /api/123/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User ID (must match JWT claim) |
| `id` | integer | Yes | Task ID |

**Request Body**:
```json
{
  "title": "string (required, max 255 chars)",
  "description": "string (optional, can be null)",
  "completed": "boolean (optional, default unchanged)"
}
```

**Validation Rules**:
| Field | Rules |
|-------|-------|
| `title` | Required, not empty, max 255 characters |
| `description` | Optional, max 10,000 characters |
| `completed` | Optional, boolean |

**Response** (200 OK):
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Updated title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2026-01-02T10:00:00Z",
  "updated_at": "2026-01-02T12:30:00Z"
}
```

**Errors**:
| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Missing title | `{"detail": "Field required: title"}` |
| 400 | Title too long | `{"detail": "Title must be 255 characters or less"}` |
| 401 | JWT missing/invalid | `{"detail": "Unauthorized"}` |
| 401 | JWT user_id ≠ path user_id | `{"detail": "Unauthorized"}` |
| 404 | Task not found OR not owned | `{"detail": "Task not found"}` |

**Security Requirements**:
- ✅ Verify ownership before update (user_id filter)
- ✅ Auto-update `updated_at` timestamp
- ✅ Return 404 (not 403) for unauthorized access

**Skills Used**: `user-scoped-query.md`

---

## Endpoint: Delete Task

### `DELETE /api/{user_id}/tasks/{id}`

**Purpose**: Delete task (if owned by authenticated user)

**Authentication**: ✅ Required  
**Authorization**: JWT `user_id` claim MUST match path `{user_id}` AND task MUST belong to user

**Request**:
```http
DELETE /api/123/tasks/1 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGc...
```

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User ID (must match JWT claim) |
| `id` | integer | Yes | Task ID |

**Response** (204 No Content):
```
(Empty response body)
```

**Errors**:
| Status | Condition | Response |
|--------|-----------|----------|
| 401 | JWT missing/invalid | `{"detail": "Unauthorized"}` |
| 401 | JWT user_id ≠ path user_id | `{"detail": "Unauthorized"}` |
| 404 | Task not found OR not owned | `{"detail": "Task not found"}` |

**Security Requirements**:
- ✅ Verify ownership before delete (user_id filter)
- ✅ Return 404 (not 403) for unauthorized access
- ✅ Permanent deletion (no soft delete in Phase II)

**Skills Used**: `user-scoped-query.md`

---

## Endpoint: Toggle Task Completion

### `PATCH /api/{user_id}/tasks/{id}/complete`

**Purpose**: Toggle task completion status (if owned by authenticated user)

**Authentication**: ✅ Required  
**Authorization**: JWT `user_id` claim MUST match path `{user_id}` AND task MUST belong to user

**Request**:
```http
PATCH /api/123/tasks/1/complete HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "completed": true
}
```

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | integer | Yes | User ID (must match JWT claim) |
| `id` | integer | Yes | Task ID |

**Request Body**:
```json
{
  "completed": "boolean (required)"
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
  "updated_at": "2026-01-02T13:00:00Z"
}
```

**Errors**:
| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Missing completed field | `{"detail": "Field required: completed"}` |
| 401 | JWT missing/invalid | `{"detail": "Unauthorized"}` |
| 401 | JWT user_id ≠ path user_id | `{"detail": "Unauthorized"}` |
| 404 | Task not found OR not owned | `{"detail": "Task not found"}` |

**Security Requirements**:
- ✅ Verify ownership before update (user_id filter)
- ✅ Auto-update `updated_at` timestamp
- ✅ Return 404 (not 403) for unauthorized access

---

## Data Models

### Task Response Model

```json
{
  "id": "integer (primary key)",
  "user_id": "integer (owner ID)",
  "title": "string (max 255 chars)",
  "description": "string | null (optional)",
  "completed": "boolean",
  "created_at": "ISO 8601 timestamp (UTC)",
  "updated_at": "ISO 8601 timestamp (UTC)"
}
```

### Task Create Request Model

```json
{
  "title": "string (required, max 255 chars)",
  "description": "string | null (optional)"
}
```

### Task Update Request Model

```json
{
  "title": "string (required, max 255 chars)",
  "description": "string | null (optional)",
  "completed": "boolean (optional)"
}
```

### Task Complete Request Model

```json
{
  "completed": "boolean (required)"
}
```

---

## Error Response Format

### Standard Error Response

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "timestamp": "2026-01-02T12:00:00Z"
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `MISSING_TOKEN` | 401 | Authorization header not provided |
| `INVALID_TOKEN` | 401 | JWT signature verification failed |
| `EXPIRED_TOKEN` | 401 | JWT has expired |
| `UNAUTHORIZED` | 401 | user_id mismatch or invalid auth |
| `NOT_FOUND` | 404 | Resource not found or not owned |
| `VALIDATION_ERROR` | 400 | Request body validation failed |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## CORS Configuration

### Allowed Origins

**Development**:
```
http://localhost:3000
```

**Production**:
```
https://yourdomain.vercel.app
```

### Allowed Methods

```
GET, POST, PUT, PATCH, DELETE, OPTIONS
```

### Allowed Headers

```
Authorization, Content-Type
```

### Exposed Headers

```
Content-Type
```

### Credentials

```
true (for cookies if used)
```

---

## Rate Limiting

**Phase II**: No rate limiting (hackathon scope)

**Phase III+ Consideration**: Implement rate limiting per user (100 req/min)

---

## API Versioning

**Phase II**: No versioning (v1 implicit)

**Future**: Version in URL path (`/api/v2/...`) or Accept header

---

## Performance Requirements

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response time (p95) | < 200ms | Server-side timing |
| Response time (p99) | < 500ms | Server-side timing |
| Throughput | > 100 req/s | Load testing |
| Database query time | < 50ms | Query logging |

---

## Security Requirements

### Authentication
- ✅ JWT required on all `/api/{user_id}/tasks` endpoints
- ✅ JWT signature verified with `BETTER_AUTH_SECRET`
- ✅ JWT expiration checked on every request
- ✅ Invalid/expired tokens return 401

### Authorization
- ✅ User can only access their own tasks
- ✅ user_id extracted from JWT, never from request
- ✅ Path parameter user_id must match JWT claim
- ✅ Database queries always filter by authenticated user_id

### Input Validation
- ✅ Pydantic models validate all request bodies
- ✅ Max length constraints enforced
- ✅ Type checking (string, boolean, integer)
- ✅ SQL injection prevented (ORM parameterized queries)

### Output Security
- ✅ Never expose password hashes
- ✅ Return 404 (not 403) for unauthorized resources
- ✅ Consistent error messages (no info leakage)

**Skills Used**: `secure-jwt-guard.md`, `user-scoped-query.md`

---

## Testing Strategy

### Manual API Tests (curl/Postman)

**Health Check**:
```bash
curl http://localhost:8000/api/health
```

**Create Task** (with JWT):
```bash
curl -X POST http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Test desc"}'
```

**List Tasks** (with JWT):
```bash
curl http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <JWT>"
```

**Update Task** (with JWT):
```bash
curl -X PUT http://localhost:8000/api/123/tasks/1 \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated", "completed": true}'
```

**Delete Task** (with JWT):
```bash
curl -X DELETE http://localhost:8000/api/123/tasks/1 \
  -H "Authorization: Bearer <JWT>"
```

### Security Tests

**Test 1**: Request without JWT → 401
```bash
curl http://localhost:8000/api/123/tasks
# Expected: 401 Unauthorized
```

**Test 2**: Request with invalid JWT → 401
```bash
curl http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer invalid.jwt.token"
# Expected: 401 Unauthorized
```

**Test 3**: Request with user_id mismatch → 401
```bash
# JWT has user_id=123, but request path has user_id=456
curl http://localhost:8000/api/456/tasks \
  -H "Authorization: Bearer <JWT_for_user_123>"
# Expected: 401 Unauthorized
```

**Test 4**: Access other user's task → 404
```bash
# User 123 tries to access user 456's task
curl http://localhost:8000/api/123/tasks/999 \
  -H "Authorization: Bearer <JWT_for_user_123>"
# Expected: 404 Not Found (even if task 999 exists for user 456)
```

---

## Phase Compliance

### Phase II Allowed ✅
- ✅ RESTful CRUD endpoints
- ✅ JWT authentication
- ✅ User isolation
- ✅ JSON request/response
- ✅ Standard HTTP status codes

### Phase II Forbidden ❌
- ❌ WebSocket endpoints (Phase III)
- ❌ Shared task endpoints (Phase III)
- ❌ OAuth endpoints (Phase III)
- ❌ Real-time notifications (Phase III)
- ❌ GraphQL API (Phase IV)

**Constitutional Compliance**: ✅ This API adheres to Article VII (Security Mandates)

---

## References

- Constitution: `.specify/memory/constitution.md` (Article VII)
- Architecture: `specs/architecture.md`
- Database Schema: `specs/database/schema.md`
- Skills: `.claude/skills/secure-jwt-guard.md`, `.claude/skills/user-scoped-query.md`
- FastAPI Docs: https://fastapi.tiangolo.com

---

**Status**: ✅ Approved for Implementation  
**Next Step**: Proceed to feature specifications (authentication and task CRUD)


