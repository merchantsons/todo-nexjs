# Database Schema Specification — Evolution of Todo (Phase II)

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Approved  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution Article VII (Security Mandates)

---

## Overview

This document defines the complete database schema for Evolution of Todo Phase II, establishing data models, relationships, constraints, and security requirements.

**Database**: Neon Serverless PostgreSQL  
**ORM**: SQLModel (Pydantic + SQLAlchemy)  
**Migration Strategy**: SQLModel create_all() for Phase II  
**Connection**: `DATABASE_URL` environment variable

---

## Schema Diagram

```
┌─────────────────────────────────────┐
│             users                   │
├─────────────────────────────────────┤
│ id            SERIAL PRIMARY KEY    │
│ email         VARCHAR(255) UNIQUE   │
│ password_hash VARCHAR(255) NOT NULL │
│ created_at    TIMESTAMP DEFAULT NOW │
└──────────────────┬──────────────────┘
                   │
                   │ 1:N
                   │
                   ↓
┌─────────────────────────────────────┐
│             tasks                   │
├─────────────────────────────────────┤
│ id            SERIAL PRIMARY KEY    │
│ user_id       INTEGER NOT NULL FK   │◄─── Foreign Key
│ title         VARCHAR(255) NOT NULL │
│ description   TEXT NULLABLE         │
│ completed     BOOLEAN DEFAULT FALSE │
│ created_at    TIMESTAMP DEFAULT NOW │
│ updated_at    TIMESTAMP DEFAULT NOW │
└─────────────────────────────────────┘
```

---

## Table: `users`

### Purpose
Stores user account information for authentication and ownership tracking.

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique user identifier (auto-increment) |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | User's email address for login |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt-hashed password (never plaintext) |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Account creation timestamp |

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| `users_pkey` | `id` | PRIMARY KEY | Fast user lookup by ID |
| `users_email_unique` | `email` | UNIQUE | Fast login lookup, prevent duplicate emails |

### Constraints

- ✅ `email` must be unique (enforced at database level)
- ✅ `password_hash` must never be NULL
- ✅ `email` must be valid email format (enforced by application)

### Security Requirements

- ✅ Passwords MUST be hashed with bcrypt (cost factor 12 minimum)
- ✅ Passwords MUST NEVER be stored in plaintext
- ✅ Password hashes MUST NEVER be returned in API responses
- ✅ Email addresses are considered PII and should not be logged

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Sample Data

```sql
INSERT INTO users (email, password_hash, created_at) VALUES
  ('alice@example.com', '$2b$12$...hashed...', '2026-01-02 10:00:00'),
  ('bob@example.com', '$2b$12$...hashed...', '2026-01-02 11:00:00');
```

---

## Table: `tasks`

### Purpose
Stores todo items owned by users with completion tracking.

### Columns

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique task identifier (auto-increment) |
| `user_id` | INTEGER | NOT NULL, FOREIGN KEY | Owner of this task (references users.id) |
| `title` | VARCHAR(255) | NOT NULL | Task title (required) |
| `description` | TEXT | NULLABLE | Optional task description (can be empty) |
| `completed` | BOOLEAN | DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Task creation timestamp |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last modification timestamp |

### Indexes

| Index Name | Columns | Type | Purpose |
|------------|---------|------|---------|
| `tasks_pkey` | `id` | PRIMARY KEY | Fast task lookup by ID |
| `tasks_user_id_idx` | `user_id` | INDEX | Fast user-scoped queries (critical for performance) |
| `tasks_created_at_idx` | `created_at` | INDEX | Chronological sorting |

### Constraints

#### Primary Key
- ✅ `id` is unique and auto-incrementing

#### Foreign Key
- ✅ `user_id` REFERENCES `users(id)` ON DELETE CASCADE
- **Enforcement**: When user is deleted, all their tasks are automatically deleted
- **Rationale**: Prevents orphaned tasks, maintains referential integrity

#### Check Constraints
- ✅ `title` must not be empty string (enforced by application)
- ✅ `title` length <= 255 characters

### Security Requirements

**Critical User Isolation Rules**:
- ✅ ALL queries MUST include `WHERE user_id = :authenticated_user_id`
- ✅ User ID MUST come from validated JWT, NEVER from request parameters
- ✅ Queries MUST return 404 (not 403) for non-existent or unauthorized tasks
- ✅ Cross-user data access MUST be impossible

**Skills Used**: `user-scoped-query.md`

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Sample Data

```sql
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at) VALUES
  (1, 'Buy groceries', 'Milk, eggs, bread', false, '2026-01-02 10:05:00', '2026-01-02 10:05:00'),
  (1, 'Finish hackathon', 'Complete Phase II implementation', false, '2026-01-02 10:10:00', '2026-01-02 10:10:00'),
  (2, 'Read documentation', 'FastAPI and SQLModel docs', true, '2026-01-02 11:05:00', '2026-01-02 11:30:00');
```

---

## Relationships

### User → Tasks (One-to-Many)

**Relationship**: One user can have many tasks  
**Foreign Key**: `tasks.user_id` → `users.id`  
**Cascade**: ON DELETE CASCADE (delete user → delete all their tasks)

**Query Pattern (User's Tasks)**:
```sql
SELECT * FROM tasks WHERE user_id = :authenticated_user_id;
```

**Query Pattern (Single Task with Ownership Check)**:
```sql
SELECT * FROM tasks 
WHERE id = :task_id AND user_id = :authenticated_user_id;
```

---

## Database Connection

### Connection String Format
```
postgresql://username:password@host:port/database?sslmode=require
```

### Environment Variable
```
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/evolution_todo?sslmode=require
```

### Connection Pooling
- **Pool Size**: 10 connections (SQLModel default)
- **Max Overflow**: 20 additional connections
- **Timeout**: 30 seconds
- **Recycle**: 3600 seconds (1 hour)

---

## Migration Strategy

### Phase II Approach
**Simple Creation**: Use SQLModel's `create_all()` method

```python
from sqlmodel import SQLModel, create_engine

engine = create_engine(DATABASE_URL)

# Create all tables
SQLModel.metadata.create_all(engine)
```

### Initialization Script

```python
# init_db.py
import os
from sqlmodel import SQLModel, create_engine
from models import User, Task  # Import models

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def init_database():
    """Initialize database tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
```

### Phase III+ Migration
For future phases, consider:
- Alembic migrations for schema changes
- Version-controlled migration files
- Rollback capabilities

---

## Query Patterns (Security-Enforced)

### Pattern 1: List User's Tasks

```python
# ✅ CORRECT: User isolation enforced
from sqlmodel import Session, select

def get_user_tasks(session: Session, user_id: int) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()
```

```python
# ❌ WRONG: No user isolation (FORBIDDEN)
def get_all_tasks(session: Session) -> list[Task]:
    statement = select(Task)  # Returns ALL users' tasks!
    return session.exec(statement).all()
```

### Pattern 2: Get Single Task with Ownership Check

```python
# ✅ CORRECT: Ownership verified
def get_user_task(session: Session, task_id: int, user_id: int) -> Task | None:
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # CRITICAL: Ownership check
    )
    return session.exec(statement).first()
```

```python
# ❌ WRONG: No ownership check (SECURITY VIOLATION)
def get_task(session: Session, task_id: int) -> Task | None:
    statement = select(Task).where(Task.id == task_id)
    return session.exec(statement).first()  # Returns ANY user's task!
```

### Pattern 3: Create Task with User Ownership

```python
# ✅ CORRECT: User ID from JWT
def create_task(session: Session, user_id: int, title: str, description: str | None) -> Task:
    task = Task(
        user_id=user_id,  # From authenticated JWT
        title=title,
        description=description
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Pattern 4: Update Task with Ownership Check

```python
# ✅ CORRECT: Verify ownership before update
def update_task(session: Session, task_id: int, user_id: int, title: str) -> Task | None:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    
    if not task:
        return None  # Return 404 to client
    
    task.title = title
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Pattern 5: Delete Task with Ownership Check

```python
# ✅ CORRECT: Verify ownership before delete
def delete_task(session: Session, task_id: int, user_id: int) -> bool:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    ).first()
    
    if not task:
        return False  # Return 404 to client
    
    session.delete(task)
    session.commit()
    return True
```

---

## Performance Considerations

### Index Optimization

**Most Common Query**: List user's tasks
```sql
SELECT * FROM tasks WHERE user_id = :user_id ORDER BY created_at DESC;
```

**Indexes Required**:
- ✅ `tasks_user_id_idx` — Filter by user
- ✅ `tasks_created_at_idx` — Sort by date

**Query Plan**: Index scan (optimal)

### Query Complexity

| Query Type | Expected Rows | Indexes Used | Performance |
|------------|---------------|--------------|-------------|
| List user's tasks | 10-100 | user_id | Excellent |
| Get single task | 1 | id, user_id | Excellent |
| Create task | N/A | N/A | Excellent |
| Update task | 1 | id, user_id | Excellent |
| Delete task | 1 | id, user_id | Excellent |

---

## Data Validation Rules

### User Table

| Field | Validation |
|-------|------------|
| `email` | Valid email format (RFC 5322) |
| `email` | Lowercase normalized |
| `email` | Max 255 characters |
| `password` | Min 8 characters (before hashing) |
| `password` | Must contain uppercase, lowercase, number |

### Task Table

| Field | Validation |
|-------|------------|
| `title` | Required (not empty) |
| `title` | Max 255 characters |
| `title` | Trimmed whitespace |
| `description` | Optional (can be null or empty) |
| `description` | Max 10,000 characters |
| `completed` | Boolean only (true/false) |

**Validation Layer**: Pydantic models in FastAPI (before database operations)

---

## Security Hardening

### SQL Injection Prevention
✅ **Mitigation**: SQLModel ORM with parameterized queries (automatic)

### Cross-User Data Leaks
✅ **Mitigation**: User-scoped query pattern enforced on all operations

### Password Security
✅ **Mitigation**: bcrypt hashing with cost factor 12+

### Data Encryption
✅ **Mitigation**: Neon provides encryption at rest (automatic)

### Connection Security
✅ **Mitigation**: TLS-encrypted connections (`sslmode=require`)

---

## Testing Strategy

### Schema Validation Tests

**Manual Tests**:
1. ✅ Create users table → Verify structure
2. ✅ Create tasks table → Verify structure and foreign key
3. ✅ Insert user → Verify creation
4. ✅ Insert task with valid user_id → Success
5. ✅ Insert task with invalid user_id → Foreign key violation
6. ✅ Delete user → Verify cascade delete of tasks
7. ✅ Query tasks with user_id filter → Returns only user's tasks

### Security Tests

**Manual Tests**:
1. ✅ Query task without user_id filter → Should be rejected by application
2. ✅ Query other user's task → Returns empty (404)
3. ✅ Attempt to update other user's task → Returns empty (404)
4. ✅ Attempt to delete other user's task → Returns empty (404)

---

## Phase Compliance

### Phase II Allowed ✅
- ✅ User and Task tables
- ✅ Foreign key relationships
- ✅ User isolation at query level
- ✅ Simple schema (no complex joins)

### Phase II Forbidden ❌
- ❌ Shared task lists (Phase III)
- ❌ Task assignment to other users (Phase III)
- ❌ Comments or activity logs (Phase III)
- ❌ Role-based access control (Phase IV)

**Constitutional Compliance**: ✅ This schema adheres to Article VII (Security Mandates)

---

## References

- Constitution: `.specify/memory/constitution.md` (Article VII)
- Architecture: `specs/architecture.md`
- Skills: `.claude/skills/user-scoped-query.md`
- SQLModel Docs: https://sqlmodel.tiangolo.com

---

**Status**: ✅ Approved for Implementation  
**Next Step**: Proceed to API endpoint specification

