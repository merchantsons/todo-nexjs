from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import datetime
from app.models import Task
from app.dependencies.auth import get_current_user_id
from app.dependencies.database import get_db_session

router = APIRouter()

# Pydantic models for request/response
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskComplete(BaseModel):
    completed: bool

# TASK-007: List Tasks Endpoint
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

# TASK-008: Create Task Endpoint
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

# TASK-009: Get Single Task Endpoint
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

# TASK-010: Update Task Endpoint
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

# TASK-011: Delete Task Endpoint
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

# TASK-012: Toggle Completion Endpoint
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

