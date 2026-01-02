"""
Tests for security and user isolation
"""
import pytest

def test_user_isolation_list_tasks(client, auth_token, auth_token_user2, test_user, test_user2, test_task):
    """Test that users can only see their own tasks"""
    # User 1 creates a task
    task1 = client.post(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"title": "User 1 Task"}
    ).json()
    
    # User 2 creates a task
    task2 = client.post(
        f"/api/{test_user2.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token_user2}"},
        json={"title": "User 2 Task"}
    ).json()
    
    # User 1 should only see their own task
    user1_tasks = client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    ).json()
    
    assert len(user1_tasks) == 2  # test_task + task1
    assert all(task["user_id"] == test_user.id for task in user1_tasks)
    
    # User 2 should only see their own task
    user2_tasks = client.get(
        f"/api/{test_user2.id}/tasks",
        headers={"Authorization": f"Bearer {auth_token_user2}"}
    ).json()
    
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["user_id"] == test_user2.id

def test_user_isolation_get_task(client, auth_token, auth_token_user2, test_user, test_user2, test_task):
    """Test that users cannot access other users' tasks"""
    # User 2 tries to access User 1's task with wrong user_id in URL
    # This should fail at user_id check (401)
    response = client.get(
        f"/api/{test_user.id}/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {auth_token_user2}"}
    )
    
    # Should fail because user_id in URL doesn't match authenticated user
    assert response.status_code == 401

def test_user_isolation_update_task(client, auth_token, auth_token_user2, test_user, test_user2, test_task):
    """Test that users cannot update other users' tasks"""
    # User 2 tries to update User 1's task with wrong user_id in URL
    response = client.put(
        f"/api/{test_user.id}/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {auth_token_user2}"},
        json={"title": "Hacked Task", "description": None, "completed": False}
    )
    
    # Should fail because user_id in URL doesn't match authenticated user
    assert response.status_code == 401

def test_user_isolation_delete_task(client, auth_token, auth_token_user2, test_user, test_user2, test_task):
    """Test that users cannot delete other users' tasks"""
    # User 2 tries to delete User 1's task with wrong user_id in URL
    response = client.delete(
        f"/api/{test_user.id}/tasks/{test_task.id}",
        headers={"Authorization": f"Bearer {auth_token_user2}"}
    )
    
    # Should fail because user_id in URL doesn't match authenticated user
    assert response.status_code == 401

def test_user_isolation_wrong_user_id(client, auth_token, test_user):
    """Test that users cannot access tasks with wrong user_id in URL"""
    # Try to access tasks with different user_id
    response = client.get(
        f"/api/{test_user.id + 999}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    assert response.status_code == 401

def test_invalid_token(client, test_user):
    """Test that invalid JWT tokens are rejected"""
    response = client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    
    assert response.status_code == 401

def test_missing_token(client, test_user):
    """Test that missing token is rejected"""
    response = client.get(f"/api/{test_user.id}/tasks")
    
    # FastAPI HTTPBearer returns 401 for missing token
    assert response.status_code == 401

def test_expired_token(client, test_user, monkeypatch):
    """Test that expired tokens are rejected"""
    from datetime import datetime, timedelta
    from jose import jwt
    from app.config import settings
    
    # Create an expired token
    expired_payload = {
        "user_id": test_user.id,
        "email": test_user.email,
        "iat": datetime.utcnow() - timedelta(hours=25),
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    expired_token = jwt.encode(expired_payload, settings.better_auth_secret, algorithm="HS256")
    
    response = client.get(
        f"/api/{test_user.id}/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    assert response.status_code == 401

