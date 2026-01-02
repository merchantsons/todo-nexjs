"""
Tests for task CRUD endpoints
"""
import pytest

def test_list_tasks_empty(client, auth_token, test_user):
    """Test listing tasks when user has no tasks"""
    response = client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    assert response.json() == []

def test_create_task(client, auth_token, test_user):
    """Test creating a task"""
    response = client.post(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "New Task",
            "description": "Task description"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Task"
    assert data["description"] == "Task description"
    assert data["completed"] is False
    assert data["user_id"] == test_user.id
    assert "id" in data

def test_create_task_no_description(client, auth_token, test_user):
    """Test creating a task without description"""
    response = client.post(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "Task Without Description"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Task Without Description"
    assert data["description"] is None

def test_list_tasks(client, auth_token, test_user, test_task):
    """Test listing tasks"""
    response = client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == test_task.id
    assert tasks[0]["title"] == "Test Task"

def test_get_task(client, auth_token, test_user, test_task):
    """Test getting a single task"""
    response = client.get(
        f"/api/{test_user.id}/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_task.id
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"

def test_get_task_not_found(client, auth_token, test_user):
    """Test getting a non-existent task"""
    response = client.get(
        f"/api/{test_user.id}/tasks/99999",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_task(client, auth_token, test_user, test_task):
    """Test updating a task"""
    response = client.put(
        f"/api/{test_user.id}/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True

def test_delete_task(client, auth_token, test_user, test_task):
    """Test deleting a task"""
    response = client.delete(
        f"/api/{test_user.id}/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 204
    
    # Verify task is deleted
    get_response = client.get(
        f"/api/{test_user.id}/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404

def test_toggle_complete(client, auth_token, test_user, test_task):
    """Test toggling task completion"""
    # Toggle to completed
    response = client.patch(
        f"/api/{test_user.id}/tasks/{test_task.id}/complete",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"completed": True}
    )
    
    assert response.status_code == 200
    assert response.json()["completed"] is True
    
    # Toggle back to incomplete
    response = client.patch(
        f"/api/{test_user.id}/tasks/{test_task.id}/complete",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"completed": False}
    )
    
    assert response.status_code == 200
    assert response.json()["completed"] is False

def test_list_tasks_unauthorized(client, test_user):
    """Test listing tasks without authentication"""
    response = client.get(f"/api/{test_user.id}/tasks")
    
    # FastAPI HTTPBearer returns 401 for missing token
    assert response.status_code == 401

def test_create_task_unauthorized(client, test_user):
    """Test creating task without authentication"""
    response = client.post(
        f"/api/{test_user.id}/tasks",
        json={"title": "Task"}
    )
    
    # FastAPI HTTPBearer returns 401 for missing token
    assert response.status_code == 401

