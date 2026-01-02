# Phase II Implementation Plan — Evolution of Todo

**Version**: 1.0.0  
**Created**: 2026-01-02  
**Status**: Ready for Execution  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution + Approved Specifications  
**Estimated Duration**: 3-5 implementation sessions

---

## Executive Summary

This plan establishes the complete implementation roadmap for Evolution of Todo Phase II, transforming approved specifications into executable tasks with clear dependencies, acceptance criteria, and validation steps.

**Approach**: Backend-First → Frontend → Integration → Deployment  
**Rationale**: Backend provides stable API contract for frontend consumption  
**Risk Mitigation**: Test each layer independently before integration

---

## Planning Principles

### Constitutional Compliance
- ✅ All tasks derive from approved specifications (Spec-First Doctrine)
- ✅ No Phase III+ features permitted (Phase Boundary Doctrine)
- ✅ Security enforced at every layer (Least-Trust Security Doctrine)
- ✅ Reusable patterns preferred (Reusability Doctrine)

### Implementation Philosophy
- **Backend First**: Stable API contract before frontend development
- **Test as You Go**: Manual testing after each component
- **Incremental Delivery**: Small, testable increments
- **No Gold-Plating**: Implement specifications exactly, no extras

---

## Implementation Phases

```
Phase 1: Backend Foundation (40% of work)
  ├─ Database Setup
  ├─ Models & Migrations
  ├─ JWT Middleware
  └─ CRUD Endpoints

Phase 2: Frontend Foundation (40% of work)
  ├─ Project Setup
  ├─ UI Components
  ├─ Authentication Pages
  └─ Task Management UI

Phase 3: Integration & Deployment (20% of work)
  ├─ API Integration
  ├─ End-to-End Testing
  └─ Deployment
```

---

## Phase 1: Backend Foundation (FastAPI)

### Sprint 1.1: Project Setup & Database

**Objective**: Initialize FastAPI project and establish database connection

**Tasks**:

#### Task 1.1.1: Initialize FastAPI Project
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: None  
**Estimated Time**: 30 minutes

**Steps**:
1. Create project directory structure:
   ```
   backend/
   ├── app/
   │   ├── __init__.py
   │   ├── main.py
   │   ├── models/
   │   │   ├── __init__.py
   │   │   ├── user.py
   │   │   └── task.py
   │   ├── dependencies/
   │   │   ├── __init__.py
   │   │   ├── auth.py
   │   │   └── database.py
   │   ├── routes/
   │   │   ├── __init__.py
   │   │   ├── health.py
   │   │   └── tasks.py
   │   └── config.py
   ├── requirements.txt
   ├── .env.example
   └── README.md
   ```

2. Create `requirements.txt`:
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

3. Create `.env.example`:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   BETTER_AUTH_SECRET=your-256-bit-secret-here
   CORS_ORIGINS=http://localhost:3000
   ```

**Acceptance Criteria**:
- ✅ Project structure created
- ✅ Dependencies documented in requirements.txt
- ✅ Environment template provided

**Validation**:
```bash
cd backend
pip install -r requirements.txt
# Should complete without errors
```

---

#### Task 1.1.2: Configure Database Connection
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.1.1  
**Estimated Time**: 20 minutes

**Specification Reference**: `specs/database/schema.md` (Database Connection section)

**Steps**:
1. Create `app/config.py`:
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

2. Create `app/dependencies/database.py`:
   ```python
   from sqlmodel import Session, create_engine
   from app.config import settings
   
   engine = create_engine(settings.database_url, echo=True)
   
   def get_db_session():
       with Session(engine) as session:
           yield session
   ```

**Acceptance Criteria**:
- ✅ Database URL loaded from environment
- ✅ SQLModel engine created
- ✅ Session dependency available

**Validation**:
```bash
# Set DATABASE_URL in .env, then:
python -c "from app.dependencies.database import engine; print(engine)"
# Should print engine object without errors
```

---

#### Task 1.1.3: Create SQLModel Definitions
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.1.2  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/database/schema.md` (SQLModel Definition sections)

**Steps**:
1. Create `app/models/user.py`:
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

2. Create `app/models/task.py`:
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

3. Create `app/models/__init__.py`:
   ```python
   from app.models.user import User
   from app.models.task import Task
   
   __all__ = ["User", "Task"]
   ```

**Acceptance Criteria**:
- ✅ User model matches schema specification
- ✅ Task model matches schema specification
- ✅ Foreign key constraint defined
- ✅ Indexes configured

**Validation**:
```bash
python -c "from app.models import User, Task; print('Models loaded successfully')"
```

---

#### Task 1.1.4: Create Database Tables
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.1.3  
**Estimated Time**: 15 minutes

**Specification Reference**: `specs/database/schema.md` (Initialization Script)

**Steps**:
1. Create `init_db.py` (root level):
   ```python
   import os
   from sqlmodel import SQLModel, create_engine
   from app.models import User, Task
   
   DATABASE_URL = os.getenv("DATABASE_URL")
   engine = create_engine(DATABASE_URL, echo=True)
   
   def init_database():
       print("Creating database tables...")
       SQLModel.metadata.create_all(engine)
       print("Database initialized successfully!")
   
   if __name__ == "__main__":
       init_database()
   ```

2. Run initialization:
   ```bash
   python init_db.py
   ```

**Acceptance Criteria**:
- ✅ `users` table created in database
- ✅ `tasks` table created in database
- ✅ Foreign key constraint exists
- ✅ Indexes created

**Validation**:
```sql
-- Connect to database and verify:
\dt  -- Should show users and tasks tables
\d users  -- Should show schema
\d tasks  -- Should show schema with FK
```

---

### Sprint 1.2: Authentication & JWT

**Objective**: Implement JWT validation middleware

#### Task 1.2.1: Create JWT Validation Dependency
**Assigned To**: Auth Security Agent  
**Priority**: Critical  
**Dependencies**: Task 1.1.1  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/features/authentication.md` (JWT Validation Dependency)  
**Skills Used**: `secure-jwt-guard.md`

**Steps**:
1. Create `app/dependencies/auth.py`:
   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   from jose import jwt, JWTError
   from app.config import settings
   
   security = HTTPBearer()
   
   def get_current_user_id(
       credentials: HTTPAuthorizationCredentials = Depends(security)
   ) -> int:
       """
       Validates JWT and extracts user_id claim.
       Returns user_id if valid, raises 401 if invalid.
       
       Skills: secure-jwt-guard.md
       """
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

**Acceptance Criteria**:
- ✅ Extracts user_id from JWT
- ✅ Verifies JWT signature
- ✅ Returns 401 for invalid token
- ✅ Returns 401 for expired token
- ✅ Returns 401 for missing user_id claim

**Validation**:
```bash
# Test with curl (after creating test JWT):
curl -H "Authorization: Bearer invalid_token" http://localhost:8000/api/123/tasks
# Should return 401
```

---

### Sprint 1.3: Task CRUD Endpoints

**Objective**: Implement all task management API endpoints

#### Task 1.3.1: Create Health Check Endpoint
**Assigned To**: Backend Specialist  
**Priority**: High  
**Dependencies**: Task 1.1.1  
**Estimated Time**: 10 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (Health Check)

**Steps**:
1. Create `app/routes/health.py`:
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

2. Register in `app/main.py`:
   ```python
   from fastapi import FastAPI
   from app.routes import health
   
   app = FastAPI(title="Evolution of Todo API", version="1.0.0")
   
   app.include_router(health.router, prefix="/api")
   ```

**Acceptance Criteria**:
- ✅ GET /api/health returns 200
- ✅ Response includes status, timestamp, version

**Validation**:
```bash
curl http://localhost:8000/api/health
# Should return JSON with status: "healthy"
```

---

#### Task 1.3.2: Create List Tasks Endpoint
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.2.1, Task 1.1.4  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (List Tasks)  
**Skills Used**: `user-scoped-query.md`

**Steps**:
1. Create `app/routes/tasks.py`:
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
       # Verify user_id matches JWT
       if user_id != authenticated_user_id:
           raise HTTPException(status_code=401, detail="Unauthorized")
       
       # User-scoped query (Skills: user-scoped-query.md)
       statement = select(Task).where(Task.user_id == authenticated_user_id)
       tasks = session.exec(statement).all()
       
       return tasks
   ```

2. Register in `app/main.py`:
   ```python
   from app.routes import tasks
   app.include_router(tasks.router)
   ```

**Acceptance Criteria**:
- ✅ Requires JWT authentication
- ✅ Verifies user_id matches JWT
- ✅ Returns only authenticated user's tasks
- ✅ Returns empty array if no tasks
- ✅ Returns 401 if user_id mismatch

**Validation**:
```bash
# With valid JWT:
curl -H "Authorization: Bearer <valid_jwt>" http://localhost:8000/api/123/tasks
# Should return user's tasks (or empty array)
```

---

#### Task 1.3.3: Create Task Endpoint
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.3.2  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (Create Task)  
**Skills Used**: `user-scoped-query.md`

**Steps**:
1. Add Pydantic models in `app/routes/tasks.py`:
   ```python
   from pydantic import BaseModel
   
   class TaskCreate(BaseModel):
       title: str
       description: str | None = None
   ```

2. Add create endpoint:
   ```python
   @router.post("/api/{user_id}/tasks", status_code=201)
   async def create_task(
       user_id: int,
       task_data: TaskCreate,
       authenticated_user_id: int = Depends(get_current_user_id),
       session: Session = Depends(get_db_session)
   ):
       # Verify user_id matches JWT
       if user_id != authenticated_user_id:
           raise HTTPException(status_code=401, detail="Unauthorized")
       
       # Create task with authenticated user_id
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

**Acceptance Criteria**:
- ✅ Requires JWT authentication
- ✅ Verifies user_id matches JWT
- ✅ Creates task with authenticated user_id
- ✅ Returns 201 with created task
- ✅ Validates title is required
- ✅ Returns 401 if user_id mismatch

**Validation**:
```bash
curl -X POST http://localhost:8000/api/123/tasks \
  -H "Authorization: Bearer <valid_jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Test"}'
# Should return 201 with task object
```

---

#### Task 1.3.4: Get Single Task Endpoint
**Assigned To**: Backend Specialist  
**Priority**: High  
**Dependencies**: Task 1.3.2  
**Estimated Time**: 20 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (Get Single Task)  
**Skills Used**: `user-scoped-query.md`

**Steps**:
1. Add endpoint in `app/routes/tasks.py`:
   ```python
   @router.get("/api/{user_id}/tasks/{task_id}")
   async def get_task(
       user_id: int,
       task_id: int,
       authenticated_user_id: int = Depends(get_current_user_id),
       session: Session = Depends(get_db_session)
   ):
       # Verify user_id matches JWT
       if user_id != authenticated_user_id:
           raise HTTPException(status_code=401, detail="Unauthorized")
       
       # User-scoped query
       statement = select(Task).where(
           Task.id == task_id,
           Task.user_id == authenticated_user_id
       )
       task = session.exec(statement).first()
       
       if not task:
           raise HTTPException(status_code=404, detail="Task not found")
       
       return task
   ```

**Acceptance Criteria**:
- ✅ Requires JWT authentication
- ✅ Verifies ownership (user_id filter)
- ✅ Returns 404 if task not found
- ✅ Returns 404 if task belongs to another user
- ✅ Returns 401 if user_id mismatch

**Validation**:
```bash
curl -H "Authorization: Bearer <valid_jwt>" http://localhost:8000/api/123/tasks/1
# Should return task if owned by user, 404 otherwise
```

---

#### Task 1.3.5: Update Task Endpoint
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.3.4  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (Update Task)  
**Skills Used**: `user-scoped-query.md`

**Steps**:
1. Add Pydantic model:
   ```python
   class TaskUpdate(BaseModel):
       title: str
       description: str | None = None
       completed: bool = False
   ```

2. Add update endpoint:
   ```python
   @router.put("/api/{user_id}/tasks/{task_id}")
   async def update_task(
       user_id: int,
       task_id: int,
       task_data: TaskUpdate,
       authenticated_user_id: int = Depends(get_current_user_id),
       session: Session = Depends(get_db_session)
   ):
       # Verify user_id matches JWT
       if user_id != authenticated_user_id:
           raise HTTPException(status_code=401, detail="Unauthorized")
       
       # Find task with ownership check
       statement = select(Task).where(
           Task.id == task_id,
           Task.user_id == authenticated_user_id
       )
       task = session.exec(statement).first()
       
       if not task:
           raise HTTPException(status_code=404, detail="Task not found")
       
       # Update task
       task.title = task_data.title
       task.description = task_data.description
       task.completed = task_data.completed
       task.updated_at = datetime.utcnow()
       
       session.add(task)
       session.commit()
       session.refresh(task)
       
       return task
   ```

**Acceptance Criteria**:
- ✅ Verifies ownership before update
- ✅ Updates title, description, completed
- ✅ Updates updated_at timestamp
- ✅ Returns 404 if not found/not owned
- ✅ Returns 401 if user_id mismatch

**Validation**:
```bash
curl -X PUT http://localhost:8000/api/123/tasks/1 \
  -H "Authorization: Bearer <valid_jwt>" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated", "completed": true}'
# Should return 200 with updated task
```

---

#### Task 1.3.6: Delete Task Endpoint
**Assigned To**: Backend Specialist  
**Priority**: High  
**Dependencies**: Task 1.3.4  
**Estimated Time**: 20 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (Delete Task)  
**Skills Used**: `user-scoped-query.md`

**Steps**:
1. Add delete endpoint:
   ```python
   @router.delete("/api/{user_id}/tasks/{task_id}", status_code=204)
   async def delete_task(
       user_id: int,
       task_id: int,
       authenticated_user_id: int = Depends(get_current_user_id),
       session: Session = Depends(get_db_session)
   ):
       # Verify user_id matches JWT
       if user_id != authenticated_user_id:
           raise HTTPException(status_code=401, detail="Unauthorized")
       
       # Find task with ownership check
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

**Acceptance Criteria**:
- ✅ Verifies ownership before delete
- ✅ Returns 204 No Content on success
- ✅ Returns 404 if not found/not owned
- ✅ Returns 401 if user_id mismatch

**Validation**:
```bash
curl -X DELETE http://localhost:8000/api/123/tasks/1 \
  -H "Authorization: Bearer <valid_jwt>"
# Should return 204, task deleted from database
```

---

#### Task 1.3.7: Toggle Completion Endpoint
**Assigned To**: Backend Specialist  
**Priority**: Medium  
**Dependencies**: Task 1.3.5  
**Estimated Time**: 20 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (Toggle Completion)  
**Skills Used**: `user-scoped-query.md`

**Steps**:
1. Add Pydantic model:
   ```python
   class TaskComplete(BaseModel):
       completed: bool
   ```

2. Add toggle endpoint:
   ```python
   @router.patch("/api/{user_id}/tasks/{task_id}/complete")
   async def toggle_complete(
       user_id: int,
       task_id: int,
       data: TaskComplete,
       authenticated_user_id: int = Depends(get_current_user_id),
       session: Session = Depends(get_db_session)
   ):
       # Verify user_id matches JWT
       if user_id != authenticated_user_id:
           raise HTTPException(status_code=401, detail="Unauthorized")
       
       # Find task with ownership check
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

**Acceptance Criteria**:
- ✅ Verifies ownership before update
- ✅ Updates only completed status
- ✅ Updates updated_at timestamp
- ✅ Returns 404 if not found/not owned

**Validation**:
```bash
curl -X PATCH http://localhost:8000/api/123/tasks/1/complete \
  -H "Authorization: Bearer <valid_jwt>" \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
# Should return 200 with updated task
```

---

#### Task 1.3.8: Configure CORS
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.1.1  
**Estimated Time**: 10 minutes

**Specification Reference**: `specs/api/rest-endpoints.md` (CORS Configuration)

**Steps**:
1. Update `app/main.py`:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   from app.config import settings
   
   app = FastAPI(title="Evolution of Todo API", version="1.0.0")
   
   # CORS configuration
   origins = settings.cors_origins.split(",")
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=origins,
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
       allow_headers=["Authorization", "Content-Type"],
   )
   ```

**Acceptance Criteria**:
- ✅ CORS configured for frontend origin
- ✅ Allows Authorization header
- ✅ Allows all required HTTP methods

**Validation**:
```bash
# Test CORS preflight:
curl -X OPTIONS http://localhost:8000/api/health \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
# Should return 200 with CORS headers
```

---

### Sprint 1.4: Backend Testing & Validation

**Objective**: Validate all backend endpoints manually

#### Task 1.4.1: Manual API Testing
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: All Sprint 1.3 tasks  
**Estimated Time**: 60 minutes

**Steps**:
1. Start backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Test health check:
   ```bash
   curl http://localhost:8000/api/health
   ```

3. Create test user in database (manual SQL or registration flow)

4. Generate test JWT with user_id claim

5. Test all endpoints:
   - List tasks (empty)
   - Create task
   - List tasks (with task)
   - Get single task
   - Update task
   - Toggle completion
   - Delete task

6. Test security:
   - Request without JWT → 401
   - Request with invalid JWT → 401
   - Request with user_id mismatch → 401
   - Access other user's task → 404

**Acceptance Criteria**:
- ✅ All endpoints return expected responses
- ✅ User isolation verified
- ✅ JWT validation working
- ✅ No SQL errors
- ✅ Timestamps auto-populated

**Validation Checklist**:
- [ ] Health check returns 200
- [ ] List tasks returns array
- [ ] Create task returns 201
- [ ] Get task returns 200 or 404
- [ ] Update task returns 200
- [ ] Delete task returns 204
- [ ] Toggle completion returns 200
- [ ] Invalid JWT returns 401
- [ ] User_id mismatch returns 401
- [ ] Cross-user access returns 404

---

## Phase 2: Frontend Foundation (Next.js)

### Sprint 2.1: Project Setup & UI Components

**Objective**: Initialize Next.js project and build atomic components

#### Task 2.1.1: Initialize Next.js Project
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: None  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/ui/pages.md`, `specs/ui/components.md`

**Steps**:
1. Create Next.js project:
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --app
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install better-auth
   npm install date-fns  # For timestamp formatting
   ```

3. Create directory structure:
   ```
   frontend/
   ├── app/
   │   ├── page.tsx (landing)
   │   ├── login/
   │   │   └── page.tsx
   │   ├── register/
   │   │   └── page.tsx
   │   └── dashboard/
   │       ├── page.tsx
   │       └── tasks/
   │           └── [id]/
   │               └── page.tsx
   ├── components/
   │   ├── auth/
   │   ├── layout/
   │   ├── tasks/
   │   └── ui/
   └── lib/
       ├── auth-client.ts
       └── api-client.ts
   ```

4. Configure `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-256-bit-secret
   BETTER_AUTH_URL=http://localhost:3000
   ```

**Acceptance Criteria**:
- ✅ Next.js project created with TypeScript
- ✅ Tailwind CSS configured
- ✅ App Router structure established
- ✅ Dependencies installed

**Validation**:
```bash
npm run dev
# Should start on http://localhost:3000
```

---

#### Task 2.1.2: Create Atomic UI Components
**Assigned To**: Frontend Specialist  
**Priority**: High  
**Dependencies**: Task 2.1.1  
**Estimated Time**: 90 minutes

**Specification Reference**: `specs/ui/components.md` (Atomic Components section)

**Steps**:
1. Create `components/ui/Button.tsx` (Primary, Secondary, Danger variants)
2. Create `components/ui/Input.tsx` (with validation and error states)
3. Create `components/ui/Textarea.tsx` (with character counter)
4. Create `components/ui/Checkbox.tsx` (custom styled)
5. Create `components/ui/LoadingSpinner.tsx` (animated)
6. Create `components/ui/ErrorMessage.tsx` (with icon)

**Acceptance Criteria**:
- ✅ All components match specification props
- ✅ TypeScript interfaces defined
- ✅ Tailwind CSS styling applied
- ✅ Components render without errors

**Validation**:
Create test page to render all components:
```tsx
// app/test-components/page.tsx
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
// ... import all components

export default function TestPage() {
  return (
    <div className="p-8 space-y-4">
      <Button variant="primary">Primary Button</Button>
      <Button variant="secondary">Secondary Button</Button>
      <Button variant="danger">Danger Button</Button>
      <Input label="Email" type="email" value="" onChange={() => {}} />
      {/* Test all components */}
    </div>
  );
}
```

---

#### Task 2.1.3: Create Molecule Components
**Assigned To**: Frontend Specialist  
**Priority**: High  
**Dependencies**: Task 2.1.2  
**Estimated Time**: 60 minutes

**Specification Reference**: `specs/ui/components.md` (Molecule Components section)

**Steps**:
1. Create `components/tasks/TaskCard.tsx` (display task with actions)
2. Create `components/tasks/EmptyState.tsx` (no tasks message)
3. Create `components/ui/ConfirmDialog.tsx` (modal confirmation)

**Acceptance Criteria**:
- ✅ Components use atomic components
- ✅ Props interfaces defined
- ✅ Visual design matches specification
- ✅ Interactive elements functional

**Validation**:
Add to test page and verify rendering

---

### Sprint 2.2: Authentication Flow

**Objective**: Implement login, register, and auth protection

#### Task 2.2.1: Configure Better Auth
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.1.1  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/features/authentication.md` (Better Auth Configuration)

**Steps**:
1. Create `lib/auth-client.ts`:
   ```typescript
   import { createAuthClient } from "better-auth/client";
   
   export const authClient = createAuthClient({
     baseURL: process.env.NEXT_PUBLIC_API_URL,
   });
   ```

2. Create auth context `components/auth/AuthProvider.tsx`:
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

**Acceptance Criteria**:
- ✅ Better Auth client configured
- ✅ Auth context provider created
- ✅ Session retrieval working

**Validation**:
```bash
# Test in browser console:
import { authClient } from "@/lib/auth-client";
authClient.getSession();
```

---

#### Task 2.2.2: Create API Client with JWT
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.2.1  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/features/authentication.md` (API Client with JWT Injection)  
**Skills Used**: `frontend-auth-api-client.md`

**Steps**:
1. Create `lib/api-client.ts`:
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

**Acceptance Criteria**:
- ✅ Automatically injects JWT into requests
- ✅ Redirects to login on 401
- ✅ Handles missing session

**Validation**:
Test with backend endpoint after auth is working

---

#### Task 2.2.3: Create Login Page
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.2.1, Task 2.1.2  
**Estimated Time**: 45 minutes

**Specification Reference**: `specs/ui/pages.md` (Login Page)

**Steps**:
1. Create `components/auth/LoginForm.tsx` (form with validation)
2. Create `app/login/page.tsx`:
   ```typescript
   "use client";
   import LoginForm from "@/components/auth/LoginForm";
   import { authClient } from "@/lib/auth-client";
   import { useRouter } from "next/navigation";
   
   export default function LoginPage() {
     const router = useRouter();
     
     async function handleLogin(email: string, password: string) {
       try {
         await authClient.signIn.email({ email, password });
         router.push("/dashboard");
       } catch (error) {
         throw error; // LoginForm will display error
       }
     }
     
     return (
       <div className="min-h-screen flex items-center justify-center">
         <LoginForm onSubmit={handleLogin} />
       </div>
     );
   }
   ```

**Acceptance Criteria**:
- ✅ Login form renders
- ✅ Email and password validation
- ✅ Successful login redirects to dashboard
- ✅ Error messages displayed

**Validation**:
1. Navigate to http://localhost:3000/login
2. Test form validation (empty fields, invalid email)
3. Test login with valid credentials
4. Verify redirect to dashboard

---

#### Task 2.2.4: Create Register Page
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.2.1, Task 2.1.2  
**Estimated Time**: 45 minutes

**Specification Reference**: `specs/ui/pages.md` (Register Page)

**Steps**:
1. Create `components/auth/RegisterForm.tsx` (with password strength)
2. Create `app/register/page.tsx` (similar to login)

**Acceptance Criteria**:
- ✅ Registration form renders
- ✅ Password complexity validation
- ✅ Successful registration redirects to dashboard
- ✅ Duplicate email error displayed

**Validation**:
1. Navigate to http://localhost:3000/register
2. Test password validation (weak passwords rejected)
3. Test registration with new email
4. Verify redirect to dashboard

---

#### Task 2.2.5: Create Protected Route Component
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.2.1  
**Estimated Time**: 20 minutes

**Specification Reference**: `specs/ui/components.md` (ProtectedRoute)

**Steps**:
1. Create `components/auth/ProtectedRoute.tsx`:
   ```typescript
   "use client";
   import { useEffect } from "react";
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

**Acceptance Criteria**:
- ✅ Checks for JWT on mount
- ✅ Redirects to login if unauthenticated
- ✅ Shows loading spinner during check
- ✅ Renders children if authenticated

**Validation**:
Wrap dashboard page and verify redirect when logged out

---

### Sprint 2.3: Task Management UI

**Objective**: Build dashboard and task management features

#### Task 2.3.1: Create Header Component
**Assigned To**: Frontend Specialist  
**Priority**: High  
**Dependencies**: Task 2.1.2, Task 2.2.1  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/ui/components.md` (Header)

**Steps**:
1. Create `components/layout/Header.tsx`:
   - Logo/branding
   - User email display
   - Logout button

**Acceptance Criteria**:
- ✅ Displays user email when logged in
- ✅ Logout clears JWT and redirects
- ✅ Responsive design

**Validation**:
Render on dashboard page

---

#### Task 2.3.2: Create Task List Components
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.1.3, Task 2.2.2  
**Estimated Time**: 60 minutes

**Specification Reference**: `specs/ui/components.md` (TaskList, TaskCard)

**Steps**:
1. Create `components/tasks/TaskList.tsx`:
   - Fetches tasks from API
   - Handles loading/error states
   - Renders TaskCard for each task
   - Shows EmptyState if no tasks

2. Implement task operations:
   - Toggle completion (PATCH API)
   - Delete task (DELETE API)
   - Navigate to task details (edit)

**Acceptance Criteria**:
- ✅ Fetches tasks on mount
- ✅ Loading spinner during fetch
- ✅ Empty state when no tasks
- ✅ TaskCards render correctly
- ✅ Toggle completion works
- ✅ Delete with confirmation works

**Validation**:
1. Load dashboard with existing tasks
2. Test toggle completion
3. Test delete task
4. Verify API calls in network tab

---

#### Task 2.3.3: Create Task Form Component
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.1.2, Task 2.2.2  
**Estimated Time**: 45 minutes

**Specification Reference**: `specs/ui/components.md` (TaskForm)

**Steps**:
1. Create `components/tasks/TaskForm.tsx`:
   - Title input (required)
   - Description textarea (optional)
   - Completed checkbox (edit mode only)
   - Submit button
   - Cancel button

2. Support both create and edit modes

**Acceptance Criteria**:
- ✅ Form validation (title required)
- ✅ Character counters work
- ✅ Create mode posts to API
- ✅ Edit mode updates task
- ✅ Loading state during submission
- ✅ Error messages displayed

**Validation**:
Test both create and edit flows

---

#### Task 2.3.4: Create Dashboard Page
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 2.3.1, Task 2.3.2, Task 2.3.3, Task 2.2.5  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/ui/pages.md` (Dashboard)

**Steps**:
1. Create `app/dashboard/page.tsx`:
   ```typescript
   "use client";
   import ProtectedRoute from "@/components/auth/ProtectedRoute";
   import Header from "@/components/layout/Header";
   import TaskList from "@/components/tasks/TaskList";
   
   export default function DashboardPage() {
     return (
       <ProtectedRoute>
         <Header />
         <main className="max-w-7xl mx-auto p-8">
           <h1 className="text-3xl font-bold mb-6">My Tasks</h1>
           <TaskList />
         </main>
       </ProtectedRoute>
     );
   }
   ```

**Acceptance Criteria**:
- ✅ Protected by authentication
- ✅ Header with user info
- ✅ Task list with all features
- ✅ Responsive layout

**Validation**:
1. Navigate to /dashboard (logged in)
2. Verify tasks load
3. Test all task operations
4. Test responsive design (mobile/desktop)

---

#### Task 2.3.5: Create Task Details Page
**Assigned To**: Frontend Specialist  
**Priority**: High  
**Dependencies**: Task 2.3.3  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/ui/pages.md` (Task Details)

**Steps**:
1. Create `app/dashboard/tasks/[id]/page.tsx`:
   - Fetch task by ID
   - Render TaskForm in edit mode
   - Handle save and delete
   - Back to dashboard button

**Acceptance Criteria**:
- ✅ Fetches task on load
- ✅ Form pre-populated with task data
- ✅ Save updates task
- ✅ Delete removes task and navigates back
- ✅ 404 handling for invalid task IDs

**Validation**:
1. Navigate to /dashboard/tasks/1
2. Edit task and save
3. Delete task
4. Try invalid task ID

---

#### Task 2.3.6: Create Landing Page
**Assigned To**: Frontend Specialist  
**Priority**: Medium  
**Dependencies**: Task 2.1.2  
**Estimated Time**: 30 minutes

**Specification Reference**: `specs/ui/pages.md` (Landing Page)

**Steps**:
1. Create `app/page.tsx`:
   - Hero section with app intro
   - Feature cards (Secure, Simple, Private)
   - CTA buttons (Login, Register)

**Acceptance Criteria**:
- ✅ Visually appealing design
- ✅ Links to login/register
- ✅ Responsive layout

**Validation**:
Navigate to http://localhost:3000 and verify

---

## Phase 3: Integration & Deployment

### Sprint 3.1: End-to-End Testing

**Objective**: Validate complete user flows

#### Task 3.1.1: Test Complete User Journeys
**Assigned To**: QA / Main Agent  
**Priority**: Critical  
**Dependencies**: All Phase 2 tasks  
**Estimated Time**: 60 minutes

**Test Flows**:

**Flow 1: New User Registration to First Task**
1. Navigate to landing page
2. Click "Get Started" → /register
3. Enter email and valid password
4. Submit registration
5. Verify redirect to /dashboard
6. Verify empty state displayed
7. Click "New Task"
8. Enter title and description
9. Submit form
10. Verify task appears in list

**Flow 2: Login and Task Management**
1. Navigate to /login
2. Enter credentials
3. Submit login
4. Verify redirect to /dashboard
5. Verify existing tasks displayed
6. Toggle task completion
7. Edit task title
8. Delete task
9. Verify all operations succeed

**Flow 3: Security Validation**
1. Log in as User A
2. Note a task ID
3. Log out
4. Log in as User B
5. Attempt to navigate to User A's task
6. Verify 404 or redirect
7. Verify User B cannot see User A's tasks

**Acceptance Criteria**:
- ✅ All user flows complete without errors
- ✅ User isolation verified
- ✅ Authentication working correctly
- ✅ All CRUD operations functional

---

### Sprint 3.2: Deployment

**Objective**: Deploy to production environment

#### Task 3.2.1: Set Up Neon Database
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 1.1.4  
**Estimated Time**: 20 minutes

**Steps**:
1. Create Neon account at neon.tech
2. Create new project "evolution-todo"
3. Copy DATABASE_URL
4. Run migrations:
   ```bash
   DATABASE_URL=<neon_url> python init_db.py
   ```
5. Verify tables created

**Acceptance Criteria**:
- ✅ Neon database created
- ✅ Tables exist in production database
- ✅ Connection string secured

---

#### Task 3.2.2: Deploy Backend to Vercel
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 3.2.1  
**Estimated Time**: 30 minutes

**Steps**:
1. Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app/main.py"
       }
     ]
   }
   ```

2. Deploy:
   ```bash
   cd backend
   vercel --prod
   ```

3. Configure environment variables in Vercel dashboard:
   - DATABASE_URL
   - BETTER_AUTH_SECRET
   - CORS_ORIGINS

4. Test deployed API:
   ```bash
   curl https://your-backend.vercel.app/api/health
   ```

**Acceptance Criteria**:
- ✅ Backend deployed successfully
- ✅ Health check endpoint works
- ✅ Environment variables configured

---

#### Task 3.2.3: Deploy Frontend to Vercel
**Assigned To**: Frontend Specialist  
**Priority**: Critical  
**Dependencies**: Task 3.2.2  
**Estimated Time**: 20 minutes

**Steps**:
1. Update `.env.local` with production API URL:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
   ```

2. Deploy:
   ```bash
   cd frontend
   vercel --prod
   ```

3. Configure environment variables in Vercel dashboard:
   - NEXT_PUBLIC_API_URL
   - BETTER_AUTH_SECRET
   - BETTER_AUTH_URL

4. Test deployed app:
   - Navigate to https://your-frontend.vercel.app
   - Test registration flow
   - Test task creation

**Acceptance Criteria**:
- ✅ Frontend deployed successfully
- ✅ Can register and login
- ✅ Can create and manage tasks
- ✅ CORS working correctly

---

#### Task 3.2.4: Update CORS for Production
**Assigned To**: Backend Specialist  
**Priority**: Critical  
**Dependencies**: Task 3.2.3  
**Estimated Time**: 5 minutes

**Steps**:
1. Update CORS_ORIGINS environment variable in Vercel backend:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000
   ```

2. Redeploy backend if needed

**Acceptance Criteria**:
- ✅ Frontend can call backend API
- ✅ No CORS errors in browser console

---

#### Task 3.2.5: Final Production Testing
**Assigned To**: All Agents  
**Priority**: Critical  
**Dependencies**: Task 3.2.4  
**Estimated Time**: 30 minutes

**Steps**:
1. Test complete user flow on production:
   - Registration
   - Login
   - Task CRUD
   - Logout

2. Test from multiple devices:
   - Desktop browser
   - Mobile browser
   - Different browsers (Chrome, Firefox, Safari)

3. Verify security:
   - No sensitive data in console
   - HTTPS enforced
   - JWT working correctly

4. Performance check:
   - Lighthouse audit (target: >90)
   - API response times

**Acceptance Criteria**:
- ✅ All features working in production
- ✅ Responsive on mobile
- ✅ Performance meets targets
- ✅ No security issues

---

## Risk Management

### High Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Better Auth + FastAPI integration issues | High | Medium | Use shared JWT secret, validate manually |
| User isolation bypass | Critical | Low | Enforce user-scoped queries, test thoroughly |
| CORS configuration errors | Medium | Medium | Test preflight requests, verify origins |
| Database connection issues | High | Low | Use connection pooling, test failover |

### Contingency Plans

**If Better Auth integration fails**:
- Fallback: Implement custom JWT generation in FastAPI
- Time impact: +2 hours

**If Vercel deployment fails**:
- Fallback: Deploy backend to Railway or Render
- Time impact: +1 hour

**If user isolation has bugs**:
- STOP implementation immediately
- Review all query patterns
- Re-test security thoroughly
- Time impact: +2 hours (non-negotiable)

---

## Success Criteria

### Functional Requirements
- ✅ User registration and login working
- ✅ JWT authentication enforced
- ✅ All 5 task CRUD operations functional
- ✅ User isolation verified (cannot access other users' tasks)
- ✅ Responsive UI on desktop and mobile

### Non-Functional Requirements
- ✅ API response times < 200ms (p95)
- ✅ Frontend loads in < 3s
- ✅ No linter errors
- ✅ Accessible (keyboard navigation, screen readers)

### Process Requirements
- ✅ All code follows specifications
- ✅ No Phase III+ features implemented
- ✅ Constitutional compliance maintained
- ✅ History documented (PHRs)

---

## Deliverables Checklist

### Backend
- [ ] FastAPI project structure
- [ ] SQLModel models (User, Task)
- [ ] JWT validation middleware
- [ ] Database connection handling
- [ ] Task CRUD endpoints (7 endpoints)
- [ ] CORS configuration
- [ ] Environment variables configured
- [ ] Deployed to Vercel

### Frontend
- [ ] Next.js App Router project
- [ ] Better Auth configured
- [ ] UI component library (15 components)
- [ ] Authentication pages (login, register)
- [ ] Dashboard page
- [ ] Task management features
- [ ] API client with JWT
- [ ] Responsive design
- [ ] Deployed to Vercel

### Documentation
- [ ] README with setup instructions
- [ ] Environment variables guide (.env.example files)
- [ ] Deployment documentation
- [ ] Prompt History Records (PHRs)

---

## Timeline Estimate

### Optimistic (Experienced Developer)
- Phase 1 (Backend): 4-5 hours
- Phase 2 (Frontend): 4-5 hours
- Phase 3 (Integration): 1-2 hours
- **Total**: 10-12 hours (2-3 sessions)

### Realistic (Average Developer)
- Phase 1 (Backend): 6-8 hours
- Phase 2 (Frontend): 6-8 hours
- Phase 3 (Integration): 2-3 hours
- **Total**: 14-19 hours (3-4 sessions)

### Conservative (Learning Curve)
- Phase 1 (Backend): 8-10 hours
- Phase 2 (Frontend): 8-10 hours
- Phase 3 (Integration): 3-4 hours
- **Total**: 19-24 hours (4-5 sessions)

---

## Next Steps

### Immediate Action
**Start with Sprint 1.1 (Backend Foundation)**
- Task 1.1.1: Initialize FastAPI project
- Assignee: Backend Specialist Agent
- Estimated time: 30 minutes

### Command to Begin
```
# Activate Backend Specialist Agent
Use agent: Backend Specialist (Phase II)
Context: specs/architecture.md, specs/database/schema.md, specs/api/rest-endpoints.md
Task: Execute Sprint 1.1 (Tasks 1.1.1 through 1.1.4)
```

---

## Constitutional Compliance Statement

This plan has been generated in full compliance with:
- ✅ Article II: Spec-First Doctrine (plan follows approved specifications)
- ✅ Article VI: Phase Boundary Doctrine (only Phase II features)
- ✅ Article VII: Least-Trust Security Doctrine (security enforced at all layers)
- ✅ Article IV: Reusability Doctrine (skills referenced where applicable)

**Authorization**: This plan is APPROVED for execution by specialized agents.

---

**Plan Status**: ✅ Ready for Execution  
**Created By**: SpecKitPlus (Planning Governor)  
**Next Agent**: Backend Specialist (Phase II)  
**Next Document**: Prompt History Record for this planning session

---

**END OF IMPLEMENTATION PLAN**


