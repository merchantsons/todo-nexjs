from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from jose import jwt
from datetime import datetime, timedelta
import bcrypt
import os
from app.models import User
from app.dependencies.database import get_db_session

# Read secret directly from environment (Vercel provides this)
def get_auth_secret():
    return os.getenv("BETTER_AUTH_SECRET", "")

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def create_jwt(user_id: int, email: str) -> str:
    """Create JWT token with user_id and email claims"""
    secret = get_auth_secret()
    if not secret:
        raise ValueError("BETTER_AUTH_SECRET not configured")
    payload = {
        "user_id": user_id,
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

@router.post("/api/auth/register", status_code=201)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_db_session)
):
    """Register a new user"""
    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Validate password
    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    # Hash password
    password_hash = hash_password(request.password)
    
    # Create user
    user = User(
        email=request.email,
        password_hash=password_hash
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Generate JWT
    token = create_jwt(user.id, user.email)
    
    return {
        "user": {
            "id": user.id,
            "email": user.email
        },
        "accessToken": token
    }

@router.post("/api/auth/login")
async def login(
    request: LoginRequest,
    session: Session = Depends(get_db_session)
):
    """Login user and return JWT"""
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate JWT
    token = create_jwt(user.id, user.email)
    
    return {
        "user": {
            "id": user.id,
            "email": user.email
        },
        "accessToken": token
    }

