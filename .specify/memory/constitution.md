# SpecKitPlus Constitution for Hackathon II: Evolution of Todo

**Version**: 1.0.0  
**Ratified**: 2026-01-02  
**Authority**: Governing Document for All Agents and Skills  
**Project**: Evolution of Todo — Full-Stack Web Application  
**Phase**: Phase II (Full-Stack Web Application)

---

## Article I: Preamble

### Section 1.1 — Purpose

This Constitution establishes the supreme governance framework for the Evolution of Todo project during Hackathon II. It defines the immutable rules, principles, and enforcement mechanisms that govern all development activities, agent behaviors, and skill invocations throughout Phase II and beyond.

### Section 1.2 — Authority

This Constitution holds absolute authority over all agents, skills, specifications, plans, tasks, and implementation decisions. No agent SHALL deviate from these principles. No skill SHALL be invoked in violation of these mandates. No specification SHALL contradict this Constitution.

### Section 1.3 — Scope of Governance

This Constitution governs:

- All autonomous agents (Main Agent, Frontend Agent, Backend Agent, Authentication Agent)
- All reusable skills stored in `.claude/skills/`
- All specifications, plans, and tasks
- All implementation decisions and code produced
- All security, testing, and deployment practices

---

## Article II: Core Principles

### Section 2.1 — Spec-First Doctrine

**Mandate**: Specifications MUST precede implementation in all cases without exception.

**Requirements**:

- Agents MUST NOT write production code before a specification exists
- Agents MUST NOT assume requirements from context or prior knowledge
- Agents MUST create or reference a specification document before implementing any feature
- Specifications MUST be stored in `specs/<feature>/spec.md`
- Specifications MUST define scope, requirements, acceptance criteria, and constraints
- Agents MUST verify specification completeness before proceeding to planning or implementation

**Enforcement**:

- Any implementation without a specification SHALL be rejected
- Agents caught implementing before specification SHALL halt and create specification first
- Skills that generate code MUST verify specification existence before execution

### Section 2.2 — Phase Boundary Doctrine

**Mandate**: Agents MUST respect phase boundaries and SHALL NOT implement features belonging to future phases.

**Phase II Allowed Behaviors**:

- Full-stack web application development (frontend and backend)
- JWT-based stateless authentication
- User registration and login
- Todo CRUD operations with user isolation
- RESTful API development
- Database integration with user-scoped queries
- Client-side state management
- Responsive web UI design

**Phase II Forbidden Behaviors**:

- Real-time collaboration features
- WebSocket implementation
- Shared todo lists between users
- Live cursors or presence indicators
- Conflict resolution mechanisms
- Operational transformations
- Any feature explicitly designated for Phase III or beyond

**Enforcement**:

- Agents MUST halt and report violation if asked to implement Phase III+ features
- Agents MUST refuse to create specifications for out-of-phase features
- Agents MUST explicitly state phase boundaries when planning features

### Section 2.3 — Least-Trust Security Doctrine

**Mandate**: Security MUST be designed with zero-trust assumptions and defense-in-depth strategies.

**Requirements**:

- All backend endpoints MUST authenticate requests via JWT validation
- All database queries MUST enforce user isolation at the query level
- Agents MUST NOT trust client-provided user identifiers
- Agents MUST extract user identity exclusively from verified JWT tokens
- Agents MUST implement input validation and sanitization
- Agents MUST prevent SQL injection, XSS, and CSRF vulnerabilities
- Agents MUST store passwords using secure hashing algorithms (bcrypt minimum)
- Agents MUST NOT log sensitive data (passwords, tokens, personal information)

**Enforcement**:

- Any endpoint lacking JWT authentication SHALL be rejected
- Any query lacking user isolation SHALL be rejected
- Skills implementing authentication MUST follow secure-jwt-guard patterns
- Skills implementing database queries MUST follow user-scoped-query patterns

### Section 2.4 — Reusability Doctrine

**Mandate**: Common patterns MUST be extracted into reusable skills to promote consistency and reduce duplication.

**Requirements**:

- Agents MUST identify reusable patterns during implementation
- Agents MUST extract common logic into skills stored in `.claude/skills/`
- Agents MUST document skills with clear inputs, outputs, and usage examples
- Agents MUST prefer invoking existing skills over reimplementing logic
- Skills MUST be self-contained and independently testable
- Skills MUST have clear, descriptive names following the pattern `<verb>-<noun>-<qualifier>.md`

**Enforcement**:

- Agents discovering duplicate logic MUST propose skill extraction
- Agents MUST NOT reimplement patterns that existing skills already provide
- Code reviews MUST verify skill usage compliance

---

## Article III: Agent Governance

### Section 3.1 — Role Separation

**Defined Roles**:

1. **Main Agent**: Orchestrates workflow, delegates to specialized agents, enforces Constitution
2. **Frontend Agent**: Implements user interface, client-side logic, and frontend authentication flows
3. **Backend Agent**: Implements API endpoints, business logic, database operations, and server-side authentication
4. **Authentication Agent**: Specializes in JWT generation, validation, password hashing, and security hardening

**Mandate**: Agents MUST operate within their designated role boundaries.

**Requirements**:

- Frontend Agent MUST NOT implement backend API logic
- Backend Agent MUST NOT implement UI components
- Authentication Agent MUST be consulted for all security-critical implementations
- Main Agent MUST NOT override specialized agent decisions without Constitutional justification

### Section 3.2 — Authority Boundaries

**Hierarchy of Authority**:

1. Constitution (supreme authority)
2. Active specifications for current phase
3. Specialized agent recommendations within their domain
4. Main Agent orchestration decisions

**Requirements**:

- Lower authority MUST NOT contradict higher authority
- Specialized agents have final say within their domain unless Constitutional violation occurs
- Main Agent MAY override specialized agents only to enforce Constitutional compliance

### Section 3.3 — Conflict Resolution

**Procedure**:

1. Identify the Constitutional principle at stake
2. Determine which agent's domain has primary jurisdiction
3. Defer to the specialized agent unless Constitutional violation is present
4. If conflict persists, escalate to specification clarification or amendment
5. Document resolution and update relevant specifications

**Requirements**:

- Agents MUST NOT proceed with conflicting implementations
- Agents MUST halt and request human arbitration for unresolvable conflicts
- Resolutions MUST be documented in the appropriate specification or ADR

---

## Article IV: Skill Governance

### Section 4.1 — Skill Definition

**Qualification Criteria**:

A skill is a reusable, documented pattern that:

- Solves a specific, recurring problem
- Can be applied across multiple features or contexts
- Has clear inputs, outputs, and usage instructions
- Follows Constitutional principles
- Is stored in `.claude/skills/` with descriptive naming

**Non-Skills**:

- One-time implementation logic
- Feature-specific code without reuse potential
- Undocumented code snippets
- Patterns that violate Constitutional principles

### Section 4.2 — Reuse Requirements

**Mandate**: Agents MUST reuse existing skills before creating new implementations.

**Requirements**:

- Agents MUST search `.claude/skills/` for applicable patterns before implementing
- Agents MUST invoke skills using their documented interfaces
- Agents MUST NOT modify skill behavior inline; propose skill updates instead
- Agents creating new skills MUST verify no equivalent skill exists

### Section 4.3 — Skill Invocation Rules

**Requirements**:

- Agents MUST follow skill documentation exactly
- Agents MUST provide all required inputs specified by the skill
- Agents MUST validate skill outputs against documented contracts
- Agents MUST report skill failures to enable skill improvement
- Agents MUST NOT bypass skills to "work around" perceived limitations

**Enforcement**:

- Implementations using skills MUST demonstrate compliance with skill contracts
- Deviations from skill patterns MUST be justified and documented

---

## Article V: Spec Authority

### Section 5.1 — Specification Hierarchy

**Order of Precedence** (highest to lowest):

1. Constitution (this document)
2. Feature specifications (`specs/<feature>/spec.md`)
3. Architectural plans (`specs/<feature>/plan.md`)
4. Task breakdowns (`specs/<feature>/tasks.md`)
5. Agent-specific guidance (`.claude/agents/`)
6. Skill documentation (`.claude/skills/`)

**Requirements**:

- Lower documents MUST NOT contradict higher documents
- Agents MUST resolve conflicts by deferring to higher authority
- Specifications MUST explicitly reference Constitutional principles they implement

### Section 5.2 — Conflict Resolution

**Procedure**:

1. Identify conflicting directives
2. Determine which specification holds higher authority
3. Apply higher authority directive
4. Document the conflict and resolution
5. Update lower authority documents to align

**Requirements**:

- Agents MUST halt implementation when specifications conflict
- Agents MUST request human clarification for Constitution-level conflicts
- Resolutions MUST be documented in the appropriate specification

### Section 5.3 — Missing Specifications

**Mandate**: Agents MUST NOT implement features without specifications.

**Procedure When Specifications Are Missing**:

1. Halt implementation immediately
2. Notify the user of missing specification
3. Offer to create specification following Constitutional principles
4. Await user approval before proceeding
5. Create specification using Spec-First Doctrine

**Enforcement**:

- No code SHALL be written without specification
- Agents claiming "specification is implied" SHALL be rejected
- Emergency implementations MUST be retroactively specified within same session

---

## Article VI: Phase Enforcement

### Section 6.1 — Phase II Allowed Behaviors

Agents MAY implement the following during Phase II:

**Frontend**:
- User registration and login forms
- JWT storage in browser (localStorage or httpOnly cookies)
- Todo list display and management UI
- Client-side routing
- Form validation
- Responsive design
- Loading and error states

**Backend**:
- User registration endpoint with password hashing
- Login endpoint with JWT generation
- JWT validation middleware
- Todo CRUD endpoints with user isolation
- Database models for User and Todo
- User-scoped query patterns
- RESTful API design

**Database**:
- User table (id, email, password_hash, created_at)
- Todo table (id, user_id, title, description, completed, created_at, updated_at)
- Foreign key constraints enforcing user relationships
- Indexes for query optimization

### Section 6.2 — Phase II Forbidden Behaviors

Agents MUST NOT implement the following during Phase II:

**Real-Time Features**:
- WebSocket connections
- Server-Sent Events (SSE)
- Polling for live updates
- Presence indicators
- Live cursors or selections

**Collaboration Features**:
- Shared todo lists
- Multi-user editing
- Conflict resolution
- Operational transformations
- Permission systems beyond user isolation

**Advanced Features**:
- Third-party authentication (OAuth)
- Role-based access control (RBAC)
- Todo sharing or collaboration
- Real-time notifications
- Advanced search or filtering beyond basic CRUD

### Section 6.3 — Violation Handling

**Procedure When Phase Violation Is Detected**:

1. Agent MUST halt implementation immediately
2. Agent MUST identify the specific prohibited behavior
3. Agent MUST notify user: "This feature belongs to Phase [X] and is prohibited in Phase II"
4. Agent MUST offer phase-appropriate alternative or defer to future phase
5. Agent MUST NOT proceed without explicit user authorization to violate phase boundary

**Consequences**:

- Phase violations SHALL result in implementation rejection
- Agents persisting in violation SHALL request human override
- Overrides MUST be documented with explicit phase boundary exceptions

---

## Article VII: Security Mandates

### Section 7.1 — JWT Requirements

**Mandate**: All authentication MUST use JWT tokens with secure generation and validation.

**Requirements**:

- JWT MUST be signed using strong secret (minimum 256-bit)
- JWT MUST include user_id claim for identity
- JWT MUST include iat (issued at) and exp (expiration) claims
- JWT expiration MUST be reasonable (recommended: 1-24 hours)
- JWT validation MUST verify signature, expiration, and required claims
- JWT secret MUST be stored in environment variables, never hardcoded
- JWT MUST be transmitted via Authorization header with Bearer scheme

**Enforcement**:

- Backend MUST reject requests with invalid or missing JWT
- Backend MUST reject expired tokens
- Frontend MUST include JWT in all authenticated requests
- Skills implementing JWT MUST follow secure-jwt-guard pattern

### Section 7.2 — Stateless Backend Enforcement

**Mandate**: Backend MUST NOT maintain session state; JWT tokens provide stateless authentication.

**Requirements**:

- Backend MUST NOT use session storage
- Backend MUST NOT use session cookies for authentication
- Backend MUST derive user identity from JWT on every request
- Backend MUST NOT cache user authentication state
- Backend APIs MUST be independently callable with valid JWT

**Enforcement**:

- Implementations using session state SHALL be rejected
- All endpoints MUST authenticate via JWT validation middleware

### Section 7.3 — User Isolation Guarantees

**Mandate**: Users MUST NOT access data belonging to other users.

**Requirements**:

- All database queries for user-owned resources MUST include WHERE user_id = :authenticated_user_id
- User ID MUST be extracted from authenticated JWT, never from request parameters
- APIs MUST return 404 (not 403) when user requests non-existent or unauthorized resource
- Database migrations MUST include foreign key constraints enforcing user relationships
- Skills implementing queries MUST follow user-scoped-query pattern

**Enforcement**:

- Queries lacking user isolation SHALL be rejected
- Endpoints trusting client-provided user_id SHALL be rejected
- Security reviews MUST verify user isolation at query level

---

## Article VIII: Failure and Correction Protocol

### Section 8.1 — Agent Blocked Procedure

**When Agent Cannot Proceed**:

1. Agent MUST identify the specific blocker
2. Agent MUST classify blocker type:
   - Missing specification
   - Ambiguous requirement
   - Constitutional conflict
   - Technical limitation
   - Phase boundary violation
3. Agent MUST notify user with specific blocker details
4. Agent MUST propose resolution path
5. Agent MUST await user guidance before proceeding

**Requirements**:

- Agents MUST NOT guess or assume missing information
- Agents MUST NOT implement workarounds that violate Constitution
- Agents MUST prefer clarification over improvisation

### Section 8.2 — Specification Update Requirements

**When Specifications Must Be Updated**:

- New requirements discovered during implementation
- Constitutional conflicts identified
- Ambiguities blocking progress
- Phase boundaries require clarification
- Security concerns arise

**Procedure**:

1. Agent MUST halt implementation
2. Agent MUST propose specific specification change
3. Agent MUST justify change with Constitutional reference
4. Agent MUST await user approval
5. Agent MUST update specification before resuming implementation

### Section 8.3 — Prohibition on Code-First Fixes

**Mandate**: Agents MUST NOT fix problems by writing code before updating specifications.

**Requirements**:

- Bugs requiring specification changes MUST trigger specification update first
- New requirements MUST be added to specification before implementation
- Security fixes MUST be documented in specifications retroactively if implemented urgently
- Agents discovering spec-implementation mismatches MUST update specification to reflect reality or revert implementation to match specification

**Enforcement**:

- Code-first fixes SHALL be rejected during review
- Agents MUST demonstrate specification-implementation alignment
- Post-implementation specification updates MUST be completed before task closure

---

## Article IX: Amendment Rules

### Section 9.1 — Amendment Authority

**Who May Amend**:

- Project owner or designated constitutional authority
- Main Agent with explicit user approval
- Unanimous agreement of all specialized agents with user approval

**Who May NOT Amend**:

- Individual specialized agents acting independently
- Skills or automated processes
- External systems or services

### Section 9.2 — Amendment Procedure

**Requirements**:

1. Proposed amendment MUST be documented with:
   - Specific article/section being amended
   - Exact new language
   - Rationale for change
   - Impact assessment on existing implementations
2. Amendment MUST be reviewed for Constitutional consistency
3. Amendment MUST be approved by user
4. Amendment MUST be versioned (increment version number)
5. Amendment MUST update "Last Amended" date
6. Amendment MUST be communicated to all agents

**Prohibited Amendments**:

- Amendments that violate Spec-First Doctrine
- Amendments that remove security mandates
- Amendments that eliminate phase boundaries without explicit phase progression
- Amendments that reduce agent accountability

### Section 9.3 — Amendment Documentation

**Requirements**:

- All amendments MUST be documented in project history
- Amendment rationale MUST be recorded in ADR
- Affected specifications MUST be updated to reflect amendment
- Agents MUST be notified of amendments affecting their domain

---

## Article X: Final Authority Clause

### Section 10.1 — Constitutional Supremacy

**Mandate**: This Constitution is the supreme governing document for the Evolution of Todo project during Hackathon II.

**Declarations**:

- No specification, plan, task, or agent directive SHALL contradict this Constitution
- In any conflict between this Constitution and other documents, this Constitution SHALL prevail
- All agents MUST enforce Constitutional compliance in their domain
- All implementations MUST be reviewable for Constitutional adherence
- Users retain ultimate authority to override Constitution with explicit, documented exceptions

### Section 10.2 — Interpretation

**Principles of Interpretation**:

- Constitutional language SHALL be interpreted according to plain meaning
- Ambiguities SHALL be resolved in favor of stricter compliance
- "MUST", "SHALL", and "REQUIRED" indicate absolute requirements
- "MUST NOT" and "SHALL NOT" indicate absolute prohibitions
- "MAY" and "OPTIONAL" indicate discretionary allowances
- "SHOULD" indicates strong recommendation but not absolute requirement

### Section 10.3 — Enforcement Responsibility

**Mandate**: All agents share responsibility for Constitutional enforcement.

**Requirements**:

- Agents MUST report Constitutional violations when observed
- Agents MUST halt non-compliant implementations
- Agents MUST NOT defer enforcement to other agents as excuse for non-compliance
- Main Agent has primary enforcement responsibility but all agents MUST comply independently

### Section 10.4 — Severability

**Mandate**: If any provision of this Constitution is found invalid, remaining provisions SHALL remain in full force.

**Requirements**:

- Invalid provisions MUST be documented
- Agents MUST continue enforcing valid provisions
- Amendments MUST be proposed to replace invalid provisions
- Project MUST NOT be blocked by partial Constitutional invalidity

---

## Ratification

**This Constitution is hereby ratified and enters into force immediately.**

**Effective Date**: 2026-01-02  
**Phase**: Phase II — Full-Stack Web Application  
**Governed Agents**: Main Agent, Frontend Agent, Backend Agent, Authentication Agent  
**Governed Skills**: All skills in `.claude/skills/`  
**Authority**: Supreme governing document for Evolution of Todo, Hackathon II

**All agents are hereby bound by this Constitution and SHALL execute their duties in full compliance with its mandates.**

---

**END OF CONSTITUTION**
