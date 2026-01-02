"""
Pytest configuration and fixtures for testing
"""
import pytest
import os
from sqlmodel import SQLModel, create_engine, Session
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Task
from app.dependencies.database import get_db_session

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"
TEST_JWT_SECRET = "test-secret-key-for-jwt-testing-only-not-for-production-use"

@pytest.fixture(scope="function")
def test_db():
    """Create a test database for each test function"""
    engine = create_engine(TEST_DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup - close all connections first
    engine.dispose()
    SQLModel.metadata.drop_all(engine)
    try:
        if os.path.exists("./test.db"):
            os.remove("./test.db")
    except PermissionError:
        # On Windows, file might still be locked, ignore
        pass

@pytest.fixture(scope="function")
def db_session(test_db):
    """Create a database session for testing"""
    with Session(test_db) as session:
        yield session
        session.rollback()

@pytest.fixture(scope="function")
def client(test_db, monkeypatch):
    """Create a test client with test database"""
    # Override database dependency
    def override_get_db():
        with Session(test_db) as session:
            yield session
    
    # Override JWT secret for testing
    monkeypatch.setenv("BETTER_AUTH_SECRET", TEST_JWT_SECRET)
    from app.config import settings
    settings.better_auth_secret = TEST_JWT_SECRET
    
    app.dependency_overrides[get_db_session] = override_get_db
    
    yield TestClient(app)
    
    # Cleanup
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    import bcrypt
    password_hash = bcrypt.hashpw("testpassword123".encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
    user = User(
        email="test@example.com",
        password_hash=password_hash
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_user2(db_session):
    """Create a second test user"""
    import bcrypt
    password_hash = bcrypt.hashpw("testpassword123".encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
    user = User(
        email="test2@example.com",
        password_hash=password_hash
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_token(client, test_user):
    """Get auth token for test user"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    return response.json()["accessToken"]

@pytest.fixture
def auth_token_user2(client, test_user2):
    """Get auth token for second test user"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test2@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    return response.json()["accessToken"]

@pytest.fixture
def test_task(db_session, test_user):
    """Create a test task"""
    task = Task(
        user_id=test_user.id,
        title="Test Task",
        description="Test Description",
        completed=False
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task

