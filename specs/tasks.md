# Phase II Task Breakdown — Evolution of Todo

**Version**: 1.0.0  
**Created**: 2026-01-02  
**Status**: Ready for Execution  
**Phase**: Phase II — Full-Stack Web Application  
**Source**: `specs/plan.md`  
**Authority**: SpecKitPlus Constitution Article II

---

## Task Execution Guide

### How to Use This Document

1. **Pick Next Task**: Start with lowest incomplete task number
2. **Check Dependencies**: Verify all prerequisite tasks complete
3. **Execute Task**: Follow steps in order
4. **Validate**: Run acceptance tests
5. **Mark Complete**: Check off task when validated
6. **Update History**: Document progress in PHR

### Task Status Legend

- [ ] **Pending**: Not started
- [→] **In Progress**: Currently working
- [✓] **Complete**: Validated and done
- [✗] **Blocked**: Dependency not met

---

## PHASE 1: BACKEND FOUNDATION

### SPRINT 1.1: PROJECT SETUP & DATABASE

#### TASK-001: Initialize FastAPI Project
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Backend Specialist  
**Depends**: None

**Do**:
```bash
mkdir backend && cd backend
mkdir -p app/{models,dependencies,routes}
touch app/{__init__,main,config}.py
touch app/models/{__init__,user,task}.py
touch app/dependencies/{__init__,auth,database}.py
touch app/routes/{__init__,health,tasks}.py
touch requirements.txt .env.example README.md
```

**requirements.txt**:
```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
sqlmodel>=0.0.14
psycopg2-binary>=2.9.9
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.6
pydantic>=2.0.0
pydantic-settings>=2.0.0
bcrypt>=4.0.1
```

**.env.example**:
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=your-256-bit-secret-here
CORS_ORIGINS=http://localhost:3000
```

**Validate**:
```bash
pip install -r requirements.txt  # Should complete without errors
```

**Done When**: [ ] Structure created, [ ] Dependencies installed

---

#### TASK-002: Configure Database Connection
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 20 min  
**Agent**: Backend Specialist  
**Depends**: TASK-001  
**Spec**: `specs/database/schema.md`

**Do**:

`app/config.py`:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    cors_origins: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

`app/dependencies/database.py`:
```python
from sqlmodel import Session, create_engine
from app.config import settings

engine = create_engine(settings.database_url, echo=True)

def get_db_session():
    with Session(engine) as session:
        yield session
```

**Validate**:
```bash
# Create .env with valid DATABASE_URL
python -c "from app.dependencies.database import engine; print('✓ Engine created')"
```

**Done When**: [ ] Config loads env, [ ] Engine connects

---

#### TASK-003: Create SQLModel Definitions
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Backend Specialist  
**Depends**: TASK-002  
**Spec**: `specs/database/schema.md` (SQLModel sections)

**Do**:

`app/models/user.py`:
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

`app/models/task.py`:
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

`app/models/__init__.py`:
```python
from app.models.user import User
from app.models.task import Task

__all__ = ["User", "Task"]
```

**Validate**:
```bash
python -c "from app.models import User, Task; print('✓ Models imported')"
```

**Done When**: [ ] User model, [ ] Task model, [ ] Imports work

---

#### TASK-004: Create Database Tables
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 15 min  
**Agent**: Backend Specialist  
**Depends**: TASK-003  
**Spec**: `specs/database/schema.md` (Initialization)

**Do**:

`init_db.py` (project root):
```python
import os
from sqlmodel import SQLModel, create_engine
from app.models import User, Task

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

def init_database():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("✓ Database initialized!")

if __name__ == "__main__":
    init_database()
```

**Run**:
```bash
python init_db.py
```

**Validate**:
```sql
-- Connect to database:
\dt  -- Should show: users, tasks
\d tasks  -- Should show FK to users
```

**Done When**: [ ] Script runs, [ ] Tables exist, [ ] FK created

---

### SPRINT 1.2: AUTHENTICATION & JWT

#### TASK-005: Create JWT Validation Dependency
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Auth Security Agent  
**Depends**: TASK-001  
**Spec**: `specs/features/authentication.md`  
**Skill**: `secure-jwt-guard.md`

**Do**:

`app/dependencies/auth.py`:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

security = HTTPBearer()

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """Validates JWT and extracts user_id. Skills: secure-jwt-guard.md"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token, 
            settings.better_auth_secret, 
            algorithms=["HS256"]
        )
        user_id: int = payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id claim"
            )
        
        return user_id
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
```

**Validate**:
```bash
# After creating test JWT:
curl -H "Authorization: Bearer invalid" http://localhost:8000/api/123/tasks
# Should return: 401 Unauthorized
```

**Done When**: [ ] Extracts user_id, [ ] Returns 401 on invalid

---

### SPRINT 1.3: TASK CRUD ENDPOINTS

#### TASK-006: Health Check Endpoint
**Status**: [ ] Pending  
**Priority**: High  
**Time**: 10 min  
**Agent**: Backend Specialist  
**Depends**: TASK-001  
**Spec**: `specs/api/rest-endpoints.md`

**Do**:

`app/routes/health.py`:
```python
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }
```

`app/main.py`:
```python
from fastapi import FastAPI
from app.routes import health

app = FastAPI(title="Evolution of Todo API", version="1.0.0")
app.include_router(health.router, prefix="/api")
```

**Validate**:
```bash
uvicorn app.main:app --reload
curl http://localhost:8000/api/health
# Should return: {"status":"healthy",...}
```

**Done When**: [ ] Returns 200, [ ] JSON response correct

---

#### TASK-007: List Tasks Endpoint
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Backend Specialist  
**Depends**: TASK-005, TASK-004  
**Spec**: `specs/api/rest-endpoints.md`  
**Skill**: `user-scoped-query.md`

**Do**:

`app/routes/tasks.py`:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Task
from app.dependencies.auth import get_current_user_id
from app.dependencies.database import get_db_session

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: int,
    authenticated_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # User-scoped query (Skills: user-scoped-query.md)
    statement = select(Task).where(Task.user_id == authenticated_user_id)
    tasks = session.exec(statement).all()
    return tasks
```

Update `app/main.py`:
```python
from app.routes import tasks
app.include_router(tasks.router)
```

**Validate**:
```bash
curl -H "Authorization: Bearer <valid_jwt>" http://localhost:8000/api/123/tasks
# Should return: [] or task array
```

**Done When**: [ ] Requires JWT, [ ] Returns user's tasks only

---

#### TASK-008: Create Task Endpoint
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Backend Specialist  
**Depends**: TASK-007  
**Spec**: `specs/api/rest-endpoints.md`

**Do** (add to `app/routes/tasks.py`):

```python
from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

@router.post("/api/{user_id}/tasks", status_code=201)
async def create_task(
    user_id: int,
    task_data: TaskCreate,
    authenticated_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    task = Task(
        user_id=authenticated_user_id,
        title=task_data.title,
        description=task_data.description
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Validate**:
```bash
curl -X POST http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Desc"}'
# Should return: 201 with task object
```

**Done When**: [ ] Creates task, [ ] Returns 201

---

#### TASK-009: Get Single Task Endpoint
**Status**: [ ] Pending  
**Priority**: High  
**Time**: 20 min  
**Agent**: Backend Specialist  
**Depends**: TASK-007  
**Spec**: `specs/api/rest-endpoints.md`

**Do** (add to `app/routes/tasks.py`):

```python
@router.get("/api/{user_id}/tasks/{task_id}")
async def get_task(
    user_id: int,
    task_id: int,
    authenticated_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == authenticated_user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task
```

**Validate**:
```bash
curl -H "Authorization: Bearer <jwt>" http://localhost:8000/api/123/tasks/1
# Should return: task object or 404
```

**Done When**: [ ] Returns task, [ ] 404 for non-owned

---

#### TASK-010: Update Task Endpoint
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Backend Specialist  
**Depends**: TASK-009  
**Spec**: `specs/api/rest-endpoints.md`

**Do** (add to `app/routes/tasks.py`):

```python
class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

@router.put("/api/{user_id}/tasks/{task_id}")
async def update_task(
    user_id: int,
    task_id: int,
    task_data: TaskUpdate,
    authenticated_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == authenticated_user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Validate**:
```bash
curl -X PUT http://localhost:8000/api/123/tasks/1 \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","completed":true}'
# Should return: 200 with updated task
```

**Done When**: [ ] Updates task, [ ] Refreshes timestamp

---

#### TASK-011: Delete Task Endpoint
**Status**: [ ] Pending  
**Priority**: High  
**Time**: 20 min  
**Agent**: Backend Specialist  
**Depends**: TASK-009  
**Spec**: `specs/api/rest-endpoints.md`

**Do** (add to `app/routes/tasks.py`):

```python
@router.delete("/api/{user_id}/tasks/{task_id}", status_code=204)
async def delete_task(
    user_id: int,
    task_id: int,
    authenticated_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == authenticated_user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(task)
    session.commit()
    return None
```

**Validate**:
```bash
curl -X DELETE http://localhost:8000/api/123/tasks/1 \
  -H "Authorization: Bearer <jwt>"
# Should return: 204, task deleted
```

**Done When**: [ ] Deletes task, [ ] Returns 204

---

#### TASK-012: Toggle Completion Endpoint
**Status**: [ ] Pending  
**Priority**: Medium  
**Time**: 20 min  
**Agent**: Backend Specialist  
**Depends**: TASK-010  
**Spec**: `specs/api/rest-endpoints.md`

**Do** (add to `app/routes/tasks.py`):

```python
class TaskComplete(BaseModel):
    completed: bool

@router.patch("/api/{user_id}/tasks/{task_id}/complete")
async def toggle_complete(
    user_id: int,
    task_id: int,
    data: TaskComplete,
    authenticated_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == authenticated_user_id
    )
    task = session.exec(statement).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = data.completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

**Validate**:
```bash
curl -X PATCH http://localhost:8000/api/123/tasks/1/complete \
  -H "Authorization: Bearer <jwt>" \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
# Should return: 200 with updated task
```

**Done When**: [ ] Toggles completion, [ ] Updates timestamp

---

#### TASK-013: Configure CORS
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 10 min  
**Agent**: Backend Specialist  
**Depends**: TASK-006  
**Spec**: `specs/api/rest-endpoints.md`

**Do** (update `app/main.py`):

```python
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(title="Evolution of Todo API", version="1.0.0")

# CORS
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)
```

**Validate**:
```bash
curl -X OPTIONS http://localhost:8000/api/health \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
# Should return: 200 with CORS headers
```

**Done When**: [ ] CORS configured, [ ] Preflight works

---

### SPRINT 1.4: BACKEND TESTING

#### TASK-014: Manual API Testing
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 60 min  
**Agent**: Backend Specialist  
**Depends**: TASK-006 through TASK-013

**Test Checklist**:
- [ ] Health check returns 200
- [ ] List tasks returns array
- [ ] Create task returns 201
- [ ] Get task returns 200 or 404
- [ ] Update task returns 200
- [ ] Delete task returns 204
- [ ] Toggle completion returns 200
- [ ] Invalid JWT returns 401
- [ ] user_id mismatch returns 401
- [ ] Cross-user access returns 404

**Done When**: All 10 tests pass

---

## PHASE 2: FRONTEND FOUNDATION

### SPRINT 2.1: PROJECT & COMPONENTS

#### TASK-015: Initialize Next.js Project
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Frontend Specialist  
**Depends**: None

**Do**:
```bash
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
npm install better-auth date-fns
```

**Structure**:
```
frontend/
├── app/
│   ├── page.tsx
│   ├── login/page.tsx
│   ├── register/page.tsx
│   └── dashboard/
│       ├── page.tsx
│       └── tasks/[id]/page.tsx
├── components/
│   ├── auth/
│   ├── layout/
│   ├── tasks/
│   └── ui/
└── lib/
    ├── auth-client.ts
    └── api-client.ts
```

**.env.local**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret
BETTER_AUTH_URL=http://localhost:3000
```

**Validate**:
```bash
npm run dev  # Should start on :3000
```

**Done When**: [ ] Project created, [ ] Structure ready

---

#### TASK-016: Create Atomic UI Components
**Status**: [ ] Pending  
**Priority**: High  
**Time**: 90 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-015  
**Spec**: `specs/ui/components.md`

**Create**:
- [ ] `components/ui/Button.tsx` (Primary, Secondary, Danger)
- [ ] `components/ui/Input.tsx` (with validation)
- [ ] `components/ui/Textarea.tsx` (with counter)
- [ ] `components/ui/Checkbox.tsx` (custom styled)
- [ ] `components/ui/LoadingSpinner.tsx` (animated)
- [ ] `components/ui/ErrorMessage.tsx` (with icon)

**Validate**: Create test page at `app/test/page.tsx` to render all

**Done When**: All 6 components render without errors

---

#### TASK-017: Create Molecule Components
**Status**: [ ] Pending  
**Priority**: High  
**Time**: 60 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-016  
**Spec**: `specs/ui/components.md`

**Create**:
- [ ] `components/tasks/TaskCard.tsx`
- [ ] `components/tasks/EmptyState.tsx`
- [ ] `components/ui/ConfirmDialog.tsx`

**Validate**: Add to test page

**Done When**: All 3 components render correctly

---

### SPRINT 2.2: AUTHENTICATION FLOW

#### TASK-018: Configure Better Auth
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-015  
**Spec**: `specs/features/authentication.md`

**Do**:

`lib/auth-client.ts`:
```typescript
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});
```

`components/auth/AuthProvider.tsx`:
```typescript
"use client";
import { createContext, useContext, useEffect, useState } from "react";
import { authClient } from "@/lib/auth-client";

const AuthContext = createContext<any>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    authClient.getSession().then((session) => setUser(session?.user || null));
  }, []);
  
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

**Validate**: Test session retrieval in browser console

**Done When**: [ ] Auth client works, [ ] Context available

---

#### TASK-019: Create API Client with JWT
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-018  
**Spec**: `specs/features/authentication.md`  
**Skill**: `frontend-auth-api-client.md`

**Do**:

`lib/api-client.ts`:
```typescript
import { authClient } from "./auth-client";

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const session = await authClient.getSession();
  
  if (!session?.accessToken) {
    window.location.href = "/login";
    throw new Error("Unauthenticated");
  }
  
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${session.accessToken}`,
      "Content-Type": "application/json",
    },
  });
  
  if (response.status === 401) {
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }
  
  return response;
}
```

**Validate**: Test after authentication working

**Done When**: [ ] JWT injection works, [ ] 401 handling works

---

#### TASK-020: Create Login Page
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 45 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-018, TASK-016  
**Spec**: `specs/ui/pages.md`

**Create**:
- [ ] `components/auth/LoginForm.tsx`
- [ ] `app/login/page.tsx`

**Validate**:
- [ ] Form renders
- [ ] Validation works
- [ ] Login succeeds → redirects to dashboard
- [ ] Error messages display

**Done When**: Login flow complete

---

#### TASK-021: Create Register Page
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 45 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-018, TASK-016  
**Spec**: `specs/ui/pages.md`

**Create**:
- [ ] `components/auth/RegisterForm.tsx`
- [ ] `app/register/page.tsx`

**Validate**:
- [ ] Form renders
- [ ] Password validation works
- [ ] Registration succeeds → redirects
- [ ] Duplicate email error displays

**Done When**: Registration flow complete

---

#### TASK-022: Create Protected Route Component
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 20 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-018  
**Spec**: `specs/ui/components.md`

**Do**:

`components/auth/ProtectedRoute.tsx`:
```typescript
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    authClient.getSession().then((session) => {
      if (!session) {
        router.push("/login");
      } else {
        setLoading(false);
      }
    });
  }, [router]);
  
  if (loading) return <LoadingSpinner />;
  return <>{children}</>;
}
```

**Validate**: Wrap test page, verify redirect when logged out

**Done When**: [ ] Checks auth, [ ] Redirects if unauthenticated

---

### SPRINT 2.3: TASK MANAGEMENT UI

#### TASK-023: Create Header Component
**Status**: [ ] Pending  
**Priority**: High  
**Time**: 30 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-016, TASK-018  
**Spec**: `specs/ui/components.md`

**Do**: `components/layout/Header.tsx`

**Features**:
- [ ] Logo/branding
- [ ] User email display
- [ ] Logout button

**Done When**: Renders on dashboard

---

#### TASK-024: Create Task List Components
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 60 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-017, TASK-019  
**Spec**: `specs/ui/components.md`

**Do**: `components/tasks/TaskList.tsx`

**Features**:
- [ ] Fetch tasks from API
- [ ] Loading state
- [ ] Empty state
- [ ] Render TaskCards
- [ ] Toggle completion
- [ ] Delete with confirmation

**Validate**: All task operations work

**Done When**: Full task list functional

---

#### TASK-025: Create Task Form Component
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 45 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-016, TASK-019  
**Spec**: `specs/ui/components.md`

**Do**: `components/tasks/TaskForm.tsx`

**Features**:
- [ ] Title input (required)
- [ ] Description textarea (optional)
- [ ] Completed checkbox (edit mode)
- [ ] Validation
- [ ] Create and Edit modes

**Validate**: Both create and edit work

**Done When**: Form functional for both modes

---

#### TASK-026: Create Dashboard Page
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-023, TASK-024, TASK-025, TASK-022  
**Spec**: `specs/ui/pages.md`

**Do**: `app/dashboard/page.tsx`

**Structure**:
- [ ] ProtectedRoute wrapper
- [ ] Header
- [ ] TaskList

**Validate**:
- [ ] Requires auth
- [ ] Tasks load
- [ ] All operations work
- [ ] Responsive

**Done When**: Dashboard fully functional

---

#### TASK-027: Create Task Details Page
**Status**: [ ] Pending  
**Priority**: High  
**Time**: 30 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-025  
**Spec**: `specs/ui/pages.md`

**Do**: `app/dashboard/tasks/[id]/page.tsx`

**Features**:
- [ ] Fetch task by ID
- [ ] TaskForm in edit mode
- [ ] Save updates
- [ ] Delete task
- [ ] Back button

**Validate**:
- [ ] Loads task
- [ ] Save works
- [ ] Delete works
- [ ] 404 for invalid ID

**Done When**: Task details page functional

---

#### TASK-028: Create Landing Page
**Status**: [ ] Pending  
**Priority**: Medium  
**Time**: 30 min  
**Agent**: Frontend Specialist  
**Depends**: TASK-016  
**Spec**: `specs/ui/pages.md`

**Do**: `app/page.tsx`

**Features**:
- [ ] Hero section
- [ ] Feature cards
- [ ] CTA buttons (Login, Register)
- [ ] Responsive

**Validate**: Visually appealing, links work

**Done When**: Landing page complete

---

## PHASE 3: INTEGRATION & DEPLOYMENT

### SPRINT 3.1: TESTING

#### TASK-029: End-to-End Testing
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 60 min  
**Agent**: Main Agent  
**Depends**: All Phase 1 & 2 tasks

**Test Flows**:

**Flow 1: Registration to First Task**
1. [ ] Navigate to landing
2. [ ] Click Register
3. [ ] Submit valid registration
4. [ ] Redirects to dashboard
5. [ ] Empty state shows
6. [ ] Create first task
7. [ ] Task appears

**Flow 2: Login and CRUD**
1. [ ] Login
2. [ ] View tasks
3. [ ] Toggle completion
4. [ ] Edit task
5. [ ] Delete task

**Flow 3: Security**
1. [ ] Login as User A
2. [ ] Note task ID
3. [ ] Login as User B
4. [ ] Cannot access User A's task

**Done When**: All 3 flows pass

---

### SPRINT 3.2: DEPLOYMENT

#### TASK-030: Deploy to Neon & Vercel
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 60 min  
**Agent**: Backend & Frontend Specialists  
**Depends**: TASK-029

**Steps**:
1. [ ] Create Neon database
2. [ ] Run migrations
3. [ ] Deploy backend to Vercel
4. [ ] Set backend env vars
5. [ ] Deploy frontend to Vercel
6. [ ] Set frontend env vars
7. [ ] Update CORS origins
8. [ ] Test production

**Validate**:
- [ ] Health check works
- [ ] Can register
- [ ] Can create tasks
- [ ] CORS working

**Done When**: Production deployment successful

---

#### TASK-031: Final Production Validation
**Status**: [ ] Pending  
**Priority**: Critical  
**Time**: 30 min  
**Agent**: All Agents  
**Depends**: TASK-030

**Validate**:
- [ ] All features work in production
- [ ] Mobile responsive
- [ ] Multiple browsers tested
- [ ] Lighthouse score > 90
- [ ] No security issues
- [ ] Performance acceptable

**Done When**: Production system fully validated

---

## TASK EXECUTION SUMMARY

**Total Tasks**: 31  
**Estimated Time**: 18.25 hours  
**Critical Path**: TASK-001 → TASK-031 (sequential)

**Phase Breakdown**:
- Phase 1 (Backend): TASK-001 to TASK-014 (14 tasks, ~6 hours)
- Phase 2 (Frontend): TASK-015 to TASK-028 (14 tasks, ~10 hours)
- Phase 3 (Integration): TASK-029 to TASK-031 (3 tasks, ~2.5 hours)

---

## QUICK REFERENCE

### Start Implementation
```bash
# Task 001: Initialize FastAPI Project
cd /path/to/project
mkdir backend && cd backend
# Follow TASK-001 steps...
```

### Track Progress
- Update task status: [ ] → [→] → [✓]
- Document blockers immediately
- Update PHR after each sprint

### Get Help
- Spec unclear? → Consult `specs/<relevant>.md`
- Security question? → Reference Constitution Article VII
- Agent stuck? → Escalate to SpecKitPlus

---

**Status**: ✅ Ready for Execution  
**Next Task**: TASK-001 (Initialize FastAPI Project)  
**Next Agent**: Backend Specialist

---

**END OF TASK BREAKDOWN**


