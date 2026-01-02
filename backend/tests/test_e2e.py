"""
End-to-end tests for complete user flows
"""
import pytest

def test_full_user_flow(client):
    """Test complete user flow: register -> login -> create task -> list -> update -> delete"""
    # 1. Register a new user
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "e2e@example.com",
            "password": "e2epassword123"
        }
    )
    assert register_response.status_code == 201
    register_data = register_response.json()
    user_id = register_data["user"]["id"]
    token = register_data["accessToken"]
    
    # 2. Login with the same credentials
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "e2e@example.com",
            "password": "e2epassword123"
        }
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["user"]["id"] == user_id
    assert "accessToken" in login_data
    
    # 3. Create a task
    create_response = client.post(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "E2E Test Task",
            "description": "Testing end-to-end flow"
        }
    )
    assert create_response.status_code == 201
    task_data = create_response.json()
    task_id = task_data["id"]
    assert task_data["title"] == "E2E Test Task"
    assert task_data["completed"] is False
    
    # 4. List tasks (should have 1 task)
    list_response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id
    
    # 5. Get the task
    get_response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "E2E Test Task"
    
    # 6. Update the task
    update_response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Updated E2E Task",
            "description": "Updated description",
            "completed": True
        }
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated E2E Task"
    assert updated_task["completed"] is True
    
    # 7. Toggle completion
    toggle_response = client.patch(
        f"/api/{user_id}/tasks/{task_id}/complete",
        headers={"Authorization": f"Bearer {token}"},
        json={"completed": False}
    )
    assert toggle_response.status_code == 200
    assert toggle_response.json()["completed"] is False
    
    # 8. Delete the task
    delete_response = client.delete(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 204
    
    # 9. Verify task is deleted
    verify_response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert verify_response.status_code == 404
    
    # 10. List tasks (should be empty)
    final_list = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert final_list.status_code == 200
    assert len(final_list.json()) == 0

def test_multi_user_isolation_flow(client):
    """Test that multiple users can work independently"""
    # Create two users
    user1_response = client.post(
        "/api/auth/register",
        json={"email": "user1@test.com", "password": "password123"}
    )
    user1_id = user1_response.json()["user"]["id"]
    user1_token = user1_response.json()["accessToken"]
    
    user2_response = client.post(
        "/api/auth/register",
        json={"email": "user2@test.com", "password": "password123"}
    )
    user2_id = user2_response.json()["user"]["id"]
    user2_token = user2_response.json()["accessToken"]
    
    # User 1 creates tasks
    task1 = client.post(
        f"/api/{user1_id}/tasks",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "User 1 Task 1"}
    ).json()
    
    task2 = client.post(
        f"/api/{user1_id}/tasks",
        headers={"Authorization": f"Bearer {user1_token}"},
        json={"title": "User 1 Task 2"}
    ).json()
    
    # User 2 creates tasks
    task3 = client.post(
        f"/api/{user2_id}/tasks",
        headers={"Authorization": f"Bearer {user2_token}"},
        json={"title": "User 2 Task 1"}
    ).json()
    
    # Verify isolation
    user1_tasks = client.get(
        f"/api/{user1_id}/tasks",
        headers={"Authorization": f"Bearer {user1_token}"}
    ).json()
    
    user2_tasks = client.get(
        f"/api/{user2_id}/tasks",
        headers={"Authorization": f"Bearer {user2_token}"}
    ).json()
    
    assert len(user1_tasks) == 2
    assert len(user2_tasks) == 1
    assert all(t["user_id"] == user1_id for t in user1_tasks)
    assert all(t["user_id"] == user2_id for t in user2_tasks)
    
    # User 2 cannot access User 1's tasks (using wrong user_id in URL)
    access_attempt = client.get(
        f"/api/{user1_id}/tasks/{task1['id']}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )
    assert access_attempt.status_code == 401

