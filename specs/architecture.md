# Architecture Specification — Evolution of Todo (Phase II)

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Approved  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution Article II

---

## Overview

This document defines the complete system architecture for the Evolution of Todo Phase II application, establishing the foundational structure for a secure, scalable, stateless full-stack web application.

**Architecture Style**: Layered, Stateless, Security-First  
**Deployment Model**: Serverless (Vercel)  
**Data Flow**: Unidirectional (Frontend → API → Database)

---

## System Context Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER (Browser)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js 16+)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Better Auth Client (JWT Management)                      │  │
│  │  React Components (UI)                                    │  │
│  │  API Client (HTTP + JWT)                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP + JWT
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  JWT Validation Middleware                                │  │
│  │  RESTful API Endpoints                                    │  │
│  │  Business Logic Layer                                     │  │
│  │  SQLModel ORM                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ SQL (Parameterized)
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│              DATABASE (Neon Serverless PostgreSQL)              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  users table                                              │  │
│  │  tasks table (with FK to users)                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### Layer 1: Frontend (Next.js)

**Responsibility**: User interface, client-side logic, authentication UI

**Components**:
- **Better Auth Client**: Manages JWT tokens, login/register flows
- **Pages**: Authentication pages, task management dashboard
- **Components**: Reusable UI elements (forms, task cards, layouts)
- **API Client**: HTTP client with JWT injection for backend communication
- **State Management**: React Hooks for local state

**Technology Stack**:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth
- React 19+

**Deployment**: Vercel Edge Network

**Security Requirements**:
- ✅ Store JWT securely (localStorage or httpOnly cookies)
- ✅ Inject JWT into all API requests via Authorization header
- ✅ Clear JWT on logout
- ✅ Redirect to login on 401 responses
- ✅ Never trust client-side user identity

---

### Layer 2: Backend (FastAPI)

**Responsibility**: Business logic, authentication enforcement, data access

**Components**:
- **JWT Validation Middleware**: Verifies all incoming requests
- **Authentication Endpoints**: Login/register (delegated to Better Auth coordination)
- **Task CRUD Endpoints**: RESTful operations with user isolation
- **Database Session Manager**: Connection pooling, transaction management
- **SQLModel Models**: ORM definitions for User and Task
- **Dependency Injection**: FastAPI dependencies for auth and DB sessions

**Technology Stack**:
- FastAPI 0.100+
- Python 3.13+
- SQLModel
- Pydantic V2
- python-jose (JWT verification)
- bcrypt (password hashing)

**Deployment**: Vercel Serverless Functions or standalone container

**Security Requirements**:
- ✅ Stateless (no session storage)
- ✅ JWT required on all /api/tasks/* endpoints
- ✅ Extract user_id from JWT claims, never from request body
- ✅ Enforce user_id matching in queries
- ✅ Return 401 for invalid/missing JWT
- ✅ Return 404 (not 403) for unauthorized resource access
- ✅ Parameterized queries only (SQL injection prevention)

---

### Layer 3: Database (Neon PostgreSQL)

**Responsibility**: Persistent storage, data integrity, query performance

**Components**:
- **users table**: User accounts and credentials
- **tasks table**: Todo items with user ownership
- **Foreign Key Constraints**: Enforce referential integrity
- **Indexes**: Optimize query performance

**Technology Stack**:
- PostgreSQL 16+
- Neon Serverless Platform

**Connection**: `DATABASE_URL` environment variable

**Security Requirements**:
- ✅ Encrypted connections (TLS)
- ✅ Password hashing (bcrypt, never plaintext)
- ✅ Foreign key constraints prevent orphaned records
- ✅ Row-level isolation (enforced by application queries)

---

## Data Flow Architecture

### Authentication Flow

```
1. User submits credentials → Frontend Better Auth
2. Better Auth validates → Issues signed JWT
3. Frontend stores JWT → localStorage/cookies
4. Frontend includes JWT → All API requests (Authorization: Bearer <token>)
5. Backend middleware validates JWT → Extracts user_id claim
6. Backend proceeds with user_id → Enforces user isolation
```

### Task Creation Flow

```
1. User fills form → Frontend component
2. Frontend calls API client → POST /api/{user_id}/tasks + JWT
3. Backend validates JWT → Extracts user_id from token
4. Backend verifies user_id matches path parameter → Proceeds or 401
5. Backend creates task → INSERT with validated user_id
6. Database stores task → Returns new task record
7. Backend responds → 201 Created with task data
8. Frontend updates UI → Displays new task
```

### Task Query Flow

```
1. User loads dashboard → Frontend component
2. Frontend calls API client → GET /api/{user_id}/tasks + JWT
3. Backend validates JWT → Extracts user_id from token
4. Backend queries database → SELECT * FROM tasks WHERE user_id = :user_id
5. Database returns results → Only user's tasks
6. Backend responds → 200 OK with task array
7. Frontend renders tasks → Displays list
```

---

## Security Architecture

### Zero-Trust Model

**Principle**: Backend never trusts frontend claims

**Implementation**:
- JWT is single source of truth for identity
- User ID extracted from verified JWT token only
- Path parameters validated against JWT claims
- Database queries enforce user_id filtering

### Authentication Layer

**Component**: JWT Validation Middleware

**Responsibilities**:
- Verify JWT signature using `BETTER_AUTH_SECRET`
- Check token expiration
- Extract `user_id` claim
- Inject user_id into request context
- Reject invalid/expired/missing tokens

**Skills Used**: `secure-jwt-guard.md`

### Authorization Layer

**Component**: User-Scoped Query Pattern

**Responsibilities**:
- Enforce user_id filtering on all queries
- Prevent cross-user data access
- Return 404 for non-existent or unauthorized resources
- Never expose existence of other users' data

**Skills Used**: `user-scoped-query.md`

### Data Protection

| Layer | Protection Mechanism |
|-------|---------------------|
| Transport | HTTPS (TLS 1.3) |
| Storage | Encrypted at rest (Neon default) |
| Passwords | bcrypt hashing (cost 12) |
| Tokens | JWT signature (HS256 minimum) |
| Queries | Parameterized (SQLModel ORM) |
| Input | Pydantic validation |

---

## Deployment Architecture

### Vercel Deployment Model

**Frontend**:
- Deployed to Vercel Edge Network
- Static generation + server components
- Automatic HTTPS
- Global CDN distribution

**Backend**:
- Option A: Vercel Serverless Functions (recommended for hackathon)
- Option B: Standalone container (Docker + Cloud Run)

**Database**:
- Neon Serverless PostgreSQL
- Automatic connection pooling
- Branch-based environments (dev/prod)

### Environment Variables

**Frontend** (.env.local):
```
BETTER_AUTH_SECRET=<shared-secret-256-bit>
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend** (.env):
```
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=<shared-secret-256-bit>
CORS_ORIGINS=http://localhost:3000,https://yourdomain.vercel.app
```

---

## API Architecture

### RESTful Design Principles

- Resources identified by URLs (`/tasks/{id}`)
- HTTP verbs map to CRUD operations
- Stateless request/response
- Standard status codes
- JSON request/response bodies

### Endpoint Structure

**Base Path**: `/api`

**Resource Path**: `/api/{user_id}/tasks`

**Authentication**: `Authorization: Bearer <JWT>` header required

**Detailed specification**: See `api/rest-endpoints.md`

---

## Database Architecture

### Schema Design

**Tables**:
1. `users` — User accounts
2. `tasks` — Todo items (owned by users)

**Relationships**:
- `tasks.user_id` → `users.id` (Foreign Key, ON DELETE CASCADE)

**Indexes**:
- `users.email` — Unique index for login lookup
- `tasks.user_id` — Index for user-scoped queries
- `tasks.created_at` — Index for chronological sorting

**Detailed specification**: See `database/schema.md`

---

## State Management Architecture

### Frontend State

**No global state management library required**

**State Locations**:
- **Authentication State**: JWT in localStorage, user info in React Context
- **Task List State**: React useState in dashboard component
- **Form State**: React useState in form components
- **Loading/Error State**: React useState per component

**State Flow**:
```
User Action → Event Handler → API Call → State Update → Re-render
```

### Backend State

**Stateless Design**: No session storage, no in-memory caching

**Request Context**:
- JWT validated per request
- user_id extracted per request
- Database connections from pool per request
- No state persisted between requests

**Why Stateless?**
- Horizontally scalable (add more backend instances)
- No session synchronization needed
- Serverless-compatible (Vercel Functions)
- Phase III agent-compatible

---

## Error Handling Architecture

### Frontend Error Handling

**Strategy**: User-friendly messages with fallback UI

**Categories**:
- Network errors → "Unable to connect, please try again"
- 401 errors → Redirect to login
- 404 errors → "Task not found"
- 500 errors → "Something went wrong, please try again"

**Implementation**: Error boundaries + try/catch in API client

### Backend Error Handling

**Strategy**: Structured JSON responses with appropriate status codes

**Response Format**:
```json
{
  "detail": "Human-readable error message",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2026-01-02T12:00:00Z"
}
```

**Status Codes**:
- 200: Success
- 201: Created
- 400: Bad Request (validation error)
- 401: Unauthorized (JWT invalid/missing)
- 404: Not Found (resource doesn't exist or not owned)
- 500: Internal Server Error (unexpected failure)

---

## Performance Architecture

### Frontend Performance

**Strategies**:
- Server-side rendering for initial load
- Code splitting (Next.js automatic)
- Image optimization (Next.js Image component)
- Lazy loading for below-fold content

**Target Metrics**:
- First Contentful Paint < 1.5s
- Time to Interactive < 3s
- Lighthouse score > 90

### Backend Performance

**Strategies**:
- Connection pooling (SQLModel default)
- Async endpoints (FastAPI native)
- Query optimization (indexes on user_id)
- Minimal data transfer (only required fields)

**Target Metrics**:
- API response time < 200ms (p95)
- Database query time < 50ms (p95)
- JWT validation < 10ms

### Database Performance

**Strategies**:
- Indexed queries (user_id, email)
- Connection pooling (Neon default)
- Query limit pagination (if needed in future)

---

## Scalability Architecture

### Horizontal Scalability

**Frontend**: Infinitely scalable (static + edge)
**Backend**: Horizontally scalable (stateless design)
**Database**: Neon auto-scaling

**Phase II Load Estimate**: < 100 concurrent users (hackathon demo)
**Phase III+ Preparation**: Architecture supports 10,000+ users

### Scalability Constraints

**None identified for Phase II scope**

---

## Testing Architecture

### Frontend Testing

**Strategy**: Manual testing (automated testing out of Phase II scope)

**Test Cases**:
- Registration flow
- Login flow
- Task CRUD operations
- Logout flow
- Error handling
- Responsive design (mobile/desktop)

### Backend Testing

**Strategy**: Manual API testing with curl/Postman

**Test Cases**:
- JWT validation (valid, invalid, expired, missing)
- User isolation (cannot access other users' tasks)
- CRUD operations (all endpoints)
- Error responses (proper status codes)

### Security Testing

**Manual Tests**:
- ✅ Attempt to access tasks without JWT → 401
- ✅ Attempt to access other user's tasks → 404
- ✅ Attempt to modify user_id in JWT → Signature validation failure
- ✅ Attempt SQL injection → Parameterized queries prevent

---

## Phase Compliance

### Phase II Allowed ✅
- ✅ Full-stack web application
- ✅ JWT authentication
- ✅ User registration/login
- ✅ Task CRUD with user isolation
- ✅ RESTful API
- ✅ PostgreSQL database
- ✅ Responsive UI

### Phase II Forbidden ❌
- ❌ Real-time features (WebSockets, SSE)
- ❌ Collaboration (shared lists)
- ❌ AI/Chatbot integration
- ❌ MCP servers
- ❌ Advanced auth (OAuth, RBAC)

**Constitutional Compliance**: ✅ This architecture adheres to all Constitutional mandates

---

## Technology Decisions (ADRs)

### ADR-001: Next.js with App Router
**Decision**: Use Next.js 16+ with App Router  
**Rationale**: Modern routing, server components, Vercel integration, Better Auth support  
**Alternatives Rejected**: React SPA (no SSR), Vue.js (team unfamiliarity)

### ADR-002: FastAPI for Backend
**Decision**: Use FastAPI with async support  
**Rationale**: Type safety, auto-docs, high performance, easy JWT integration  
**Alternatives Rejected**: Express.js (less type safety), Django (heavier framework)

### ADR-003: Neon PostgreSQL
**Decision**: Use Neon Serverless PostgreSQL  
**Rationale**: Serverless, free tier, PostgreSQL compatibility, automatic backups  
**Alternatives Rejected**: MongoDB (prefer relational), SQLite (not serverless)

### ADR-004: Stateless JWT Authentication
**Decision**: JWT-based stateless auth with Better Auth  
**Rationale**: Horizontal scalability, no session storage, Phase III agent-compatible  
**Alternatives Rejected**: Session cookies (stateful), OAuth (Phase III)

### ADR-005: Vercel Deployment
**Decision**: Deploy both frontend and backend to Vercel  
**Rationale**: Integrated deployment, automatic HTTPS, serverless functions, free tier  
**Alternatives Rejected**: AWS (complex setup), Heroku (cost), Docker + Cloud Run (overkill for Phase II)

---

## References

- Constitution: `.specify/memory/constitution.md`
- Project Overview: `specs/overview.md`
- Skills: `.claude/skills/secure-jwt-guard.md`, `.claude/skills/user-scoped-query.md`
- External: Next.js Docs, FastAPI Docs, Better Auth Docs, Neon Docs

---

**Status**: ✅ Approved for Implementation  
**Next Step**: Proceed to database schema specification

