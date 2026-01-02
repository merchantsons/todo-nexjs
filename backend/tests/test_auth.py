"""
Tests for authentication endpoints
"""
import pytest

def test_register_success(client):
    """Test successful user registration"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert "accessToken" in data
    assert data["user"]["email"] == "newuser@example.com"
    assert "id" in data["user"]

def test_register_duplicate_email(client, test_user):
    """Test registration with duplicate email"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"].lower()

def test_register_short_password(client):
    """Test registration with password too short"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "password": "short"
        }
    )
    
    assert response.status_code == 400
    assert "8 characters" in response.json()["detail"].lower()

def test_register_invalid_email(client):
    """Test registration with invalid email"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "notanemail",
            "password": "password123"
        }
    )
    
    assert response.status_code == 422

def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "accessToken" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["id"] == test_user.id

def test_login_wrong_password(client, test_user):
    """Test login with wrong password"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()

def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


