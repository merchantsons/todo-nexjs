# Evolution of Todo — Project Overview

**Project Name**: Evolution of Todo  
**Hackathon**: Hackathon II  
**Phase**: Phase II — Full-Stack Web Application  
**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Specification Phase

---

## Executive Summary

**Evolution of Todo** is a multi-phase hackathon project demonstrating progressive complexity in software architecture. Phase II transforms the Phase I console-based todo application into a **production-ready, secure, multi-user web application** with persistent storage, stateless JWT authentication, and a modern responsive UI.

**Core Objective**: Build a hackathon-winning full-stack web application that prioritizes security, spec-driven development, and architectural discipline while delivering all core todo management features.

---

## Project Context

### What This Is
A secure, multi-user todo management web application built using modern full-stack technologies:
- **Frontend**: Next.js 16+ with TypeScript, Tailwind CSS, and Better Auth
- **Backend**: FastAPI with SQLModel ORM and JWT verification
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Stateless JWT with shared secret

### What This Is NOT
- ❌ A real-time collaborative editing platform (Phase III+)
- ❌ An AI-powered chatbot system (Phase III+)
- ❌ A distributed microservices architecture (Phase IV+)
- ❌ An enterprise role-based access control system
- ❌ A proof-of-concept or prototype (this is production-ready)

---

## Success Criteria

### Functional Requirements (MUST HAVE)
1. ✅ **User Registration**: New users can create accounts
2. ✅ **User Login**: Existing users can authenticate
3. ✅ **Add Task**: Users can create new todo items
4. ✅ **View Tasks**: Users can see their task list
5. ✅ **Update Task**: Users can edit task title and description
6. ✅ **Delete Task**: Users can remove tasks
7. ✅ **Mark Complete**: Users can toggle task completion status

### Non-Functional Requirements (MUST HAVE)
1. ✅ **Security**: JWT authentication enforced on all endpoints
2. ✅ **User Isolation**: Users cannot access other users' data
3. ✅ **Persistence**: All data stored in PostgreSQL database
4. ✅ **Stateless Backend**: No session storage, horizontally scalable
5. ✅ **Responsive UI**: Functional on desktop and mobile
6. ✅ **Error Handling**: Clean error messages and states
7. ✅ **Deployability**: Ready for Vercel deployment

### Process Requirements (MUST HAVE)
1. ✅ **Spec-Driven Development**: All code generated from specifications
2. ✅ **Constitutional Compliance**: Adheres to SpecKitPlus Constitution
3. ✅ **Prompt History**: PHRs created for all major activities
4. ✅ **Agent Discipline**: Agents operate within defined boundaries
5. ✅ **Security-First**: Zero-trust architecture enforced

---

## Phase Boundaries

### Phase II Scope (CURRENT)
**Allowed**: Basic multi-user todo CRUD with authentication

**Core Features**:
- User registration and login (Better Auth frontend)
- JWT-based stateless authentication
- Todo CRUD operations (5 core operations)
- User-scoped data isolation (query-level enforcement)
- Responsive web UI with Tailwind CSS
- RESTful API backend with FastAPI
- PostgreSQL persistence via SQLModel

**Explicitly Forbidden**:
- Real-time features (WebSockets, SSE, polling)
- Collaboration features (shared lists, multi-user editing)
- Advanced auth (OAuth, refresh tokens, RBAC)
- AI/Chatbot integration
- MCP servers
- Kafka/message streaming
- Kubernetes orchestration

### Phase III Preview (NOT IN SCOPE)
Phase II must be **architecturally ready** for Phase III AI integration, but no Phase III features may be implemented:
- AI chatbot for natural language task management
- MCP server integration
- Agent-based task automation
- (Details deferred to Phase III specifications)

---

## Architecture Philosophy

### Spec-Driven Development (SDD)
Every feature follows this workflow:
1. **Specification** → Define requirements, acceptance criteria, constraints
2. **Planning** → Design architecture, identify dependencies
3. **Tasks** → Break down into testable implementation tasks
4. **Implementation** → Generate code from specs (backend first, frontend second)
5. **Validation** → Verify against acceptance criteria
6. **Revision** → If incorrect, revise spec and regenerate (never code-first fixes)

### Security-First Mindset
**Zero-trust architecture**:
- Backend never trusts frontend claims
- JWT is single source of truth for user identity
- User isolation enforced at every query
- Stateless design enables horizontal scaling
- No session storage on backend

### Constitutional Governance
All development governed by **SpecKitPlus Constitution** (`.specify/memory/constitution.md`):
- Article II: Spec-First Doctrine (mandatory)
- Article VI: Phase Enforcement (Phase II only)
- Article VII: Security Mandates (JWT, stateless, user isolation)
- Article VIII: No code-first fixes (specs must be updated first)

---

## User Personas

### Primary Persona: Individual User
**Profile**: 
- Needs personal task management
- Values privacy and security
- Expects modern, responsive UI
- Uses desktop and mobile devices

**User Journey**:
1. Registers for account with email/password
2. Logs in and receives JWT
3. Views empty task list
4. Creates first task
5. Marks task as complete
6. Edits task details
7. Deletes completed task
8. Logs out

**Security Guarantee**: User can NEVER see or access another user's tasks

### Anti-Persona: Team Collaborator
**NOT supported in Phase II**: Users expecting to share tasks, collaborate in real-time, or assign tasks to others.

---

## Technology Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth (JWT-enabled)
- **State Management**: React Hooks
- **Deployment**: Vercel

**Why Next.js?**
- Server-side rendering for SEO
- App Router for modern routing patterns
- Native TypeScript support
- Vercel deployment integration
- Better Auth compatibility

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **ORM**: SQLModel
- **Validation**: Pydantic (built into FastAPI)
- **Authentication**: JWT verification with `BETTER_AUTH_SECRET`
- **Deployment**: Vercel Serverless Functions or standalone

**Why FastAPI?**
- Automatic OpenAPI documentation
- Type safety with Pydantic
- High performance (async support)
- Clean dependency injection
- Easy JWT integration

### Database
- **Provider**: Neon Serverless PostgreSQL
- **Connection**: `DATABASE_URL` environment variable
- **Schema Management**: SQLModel migrations
- **Backups**: Neon automated backups

**Why Neon?**
- Serverless (no infrastructure management)
- PostgreSQL compatibility (ACID transactions)
- Generous free tier for hackathons
- Branch-based development environments
- Automatic scaling

### Authentication
- **Strategy**: Stateless JWT (JSON Web Tokens)
- **Frontend Library**: Better Auth
- **Backend Verification**: JWT signature validation
- **Shared Secret**: `BETTER_AUTH_SECRET` (environment variable)
- **Token Transmission**: `Authorization: Bearer <token>` header

**Why JWT?**
- Stateless (no session storage required)
- Horizontally scalable
- Standard, well-supported format
- Contains user identity claims
- Phase III agent-compatible

---

## API Contract

### Base Path
All API endpoints are prefixed with `/api`

### Authentication
**Required**: All endpoints require `Authorization: Bearer <JWT>` header

### Endpoints (RESTful)

| Method | Path | Description | Auth Required |
|--------|------|-------------|---------------|
| GET | `/api/{user_id}/tasks` | List all user's tasks | Yes |
| POST | `/api/{user_id}/tasks` | Create new task | Yes |
| GET | `/api/{user_id}/tasks/{id}` | Get specific task | Yes |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | Yes |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | Yes |

**Security Rule**: JWT `user_id` claim MUST match path `{user_id}` parameter, otherwise return `401 Unauthorized`

---

## Database Schema

### Tasks Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| user_id | String | Required, Indexed, FK to users |
| title | String | Required, Max 255 chars |
| description | Text | Nullable |
| completed | Boolean | Default false |
| created_at | Timestamp | Auto-populated |
| updated_at | Timestamp | Auto-updated |

**Ownership Rule**: Every task query MUST filter by authenticated `user_id`

---

## User Workflows

### 1. Registration Flow
```
User → Frontend Form → Better Auth → Database → JWT → Frontend Storage
```

### 2. Login Flow
```
User → Frontend Form → Better Auth → Verify Password → JWT → Frontend Storage
```

### 3. Task Creation Flow
```
User → Frontend Form → API Client (+ JWT) → Backend Verify JWT → Database INSERT → Response
```

### 4. Task Listing Flow
```
User → Frontend Request (+ JWT) → Backend Verify JWT → Database SELECT WHERE user_id → Response
```

### 5. Task Update Flow
```
User → Frontend Form → API Client (+ JWT) → Backend Verify JWT → Database UPDATE WHERE user_id AND id → Response
```

### 6. Task Deletion Flow
```
User → Frontend Confirm → API Client (+ JWT) → Backend Verify JWT → Database DELETE WHERE user_id AND id → Response
```

---

## Security Model

### Authentication Flow
1. User submits credentials to Better Auth
2. Better Auth validates and issues signed JWT
3. Frontend stores JWT securely
4. Frontend attaches JWT to every API request
5. Backend verifies JWT signature using shared secret
6. Backend extracts `user_id` from JWT claims
7. Backend enforces user_id matching and query filtering

### Threat Model Mitigations

| Threat | Mitigation |
|--------|-----------|
| Unauthorized Access | JWT required on all endpoints |
| Cross-user Data Leaks | Query-level user_id filtering |
| Token Tampering | Signature verification with secret |
| Man-in-the-Middle | HTTPS only (production) |
| SQL Injection | SQLModel parameterized queries |
| XSS | React auto-escaping + CSP headers |
| CSRF | SameSite cookies (Better Auth) |
| Password Exposure | bcrypt hashing, no logging |

### Security Guarantees
1. ✅ **Authentication**: No unauthenticated access to tasks
2. ✅ **Authorization**: Users cannot access others' tasks
3. ✅ **Integrity**: Tasks cannot be modified by other users
4. ✅ **Confidentiality**: Task data encrypted in transit (HTTPS)
5. ✅ **Accountability**: User actions tied to JWT identity

---

## Development Workflow

### Spec-Driven Phases
1. **Specification** (Current phase)
   - Define all requirements
   - Document API contracts
   - Establish acceptance criteria
   
2. **Backend Implementation**
   - FastAPI project structure
   - SQLModel definitions
   - JWT authentication dependency
   - Task CRUD endpoints
   - User isolation enforcement
   
3. **Frontend Implementation**
   - Next.js project structure
   - Better Auth configuration
   - Authentication pages
   - Task management UI
   - API client with JWT
   
4. **Integration & Deployment**
   - Database connection
   - CORS configuration
   - Environment variables
   - End-to-end testing
   - Vercel deployment

### Quality Gates
Each phase must pass before proceeding:
- ✅ Specifications complete and approved
- ✅ Implementation matches specification
- ✅ Security requirements enforced
- ✅ Manual testing passes
- ✅ PHRs documented

---

## Deliverables

### Phase II Completion Checklist

**Specifications** (9 documents):
- [x] config.yaml — Phase definition
- [x] overview.md — This document
- [ ] architecture.md — System design
- [ ] features/authentication.md — Auth specification
- [ ] features/task-crud.md — Task operations
- [ ] api/rest-endpoints.md — API contracts
- [ ] database/schema.md — Database design
- [ ] ui/pages.md — Frontend pages
- [ ] ui/components.md — React components

**Backend Code**:
- [ ] FastAPI project structure
- [ ] SQLModel models (Task)
- [ ] JWT authentication dependency
- [ ] Database session handling
- [ ] Task CRUD endpoints
- [ ] Environment configuration

**Frontend Code**:
- [ ] Next.js App Router structure
- [ ] Better Auth setup
- [ ] Authentication pages (login, register)
- [ ] Task management pages
- [ ] Task UI components
- [ ] API client with JWT

**Documentation**:
- [ ] README with setup instructions
- [ ] Environment variables guide
- [ ] Deployment instructions
- [ ] Prompt History Records (PHRs)
- [ ] Architecture Decision Records (ADRs) if applicable

---

## Success Metrics

### Technical Metrics
- 100% JWT enforcement coverage
- Zero cross-user data leaks in testing
- Stateless backend (verified)
- Response times < 200ms (p95)
- Mobile-responsive UI (verified)

### Functional Metrics
- All 5 core task operations working
- Multi-user registration functional
- Login/logout flow complete
- Data persistence confirmed
- Error handling graceful

### Process Metrics
- All code generated from specs
- PHRs created for all activities
- Constitutional compliance maintained
- Agent boundaries respected
- Zero code-first fixes

---

## Risk Assessment

### High Risks
1. **Better Auth + FastAPI Integration**
   - Mitigation: Use shared secret, validate JWT claims explicitly
   
2. **User Isolation Bypass**
   - Mitigation: Query-level filtering, security reviews, manual testing

### Medium Risks
1. **CORS Configuration Errors**
   - Mitigation: Explicit frontend origin whitelisting
   
2. **Environment Variable Mismanagement**
   - Mitigation: `.env.example` template, clear documentation

### Low Risks
1. **UI Responsiveness Issues**
   - Mitigation: Tailwind utility classes, mobile-first design

---

## Phase III Readiness

While Phase III features are forbidden in Phase II, the architecture must support future integration:

**Ready For**:
- AI chatbot agents accessing task data
- MCP server integration for task automation
- Agent-based natural language task creation

**Architecture Decisions Supporting Phase III**:
- RESTful API (agent-callable)
- Stateless backend (agent-compatible)
- JWT authentication (agent can authenticate)
- Clear data models (agent can understand)

---

## References

### Internal Documents
- Constitution: `.specify/memory/constitution.md`
- Config: `.spec-kit/config.yaml`
- Hackathon Architect: `.claude/agents/hackathon-architect.md`
- Backend Specialist: `.claude/agents/backend-specialist-phase-ii.md`
- Auth Security Agent: `.claude/agents/auth-security-agent.md`

### Skills
- Secure JWT Guard: `.claude/skills/secure-jwt-guard.md`
- User-Scoped Query: `.claude/skills/user-scoped-query.md`
- Frontend Auth API Client: `.claude/skills/frontend-auth-api-client.md`

### External References
- Next.js Documentation: https://nextjs.org/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- Better Auth Documentation: https://www.better-auth.com
- SQLModel Documentation: https://sqlmodel.tiangolo.com
- Neon Documentation: https://neon.tech/docs

---

**Document Status**: ✅ Complete and approved for implementation  
**Next Steps**: Proceed to `specs/architecture.md` for technical design details


