from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from jose import jwt
from datetime import datetime, timedelta
import bcrypt
import os
from app.models import User
from app.dependencies.database import get_db_session
from app.dependencies.auth import get_current_user_id

# Read secret from environment or settings
def get_auth_secret():
    # Try environment variable first (for Vercel)
    secret = os.getenv("BETTER_AUTH_SECRET")
    if secret:
        return secret
    
    # Fall back to settings (reads from .env file)
    try:
        from app.config import settings
        if settings.better_auth_secret:
            return settings.better_auth_secret
    except Exception:
        pass
    
    return ""

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
    
    now = datetime.utcnow()
    # Convert datetime to timestamp (seconds since epoch) for JWT
    iat = int(now.timestamp())
    exp = int((now + timedelta(hours=24)).timestamp())
    
    payload = {
        "user_id": user_id,
        "email": email,
        "iat": iat,
        "exp": exp
    }
    return jwt.encode(payload, secret, algorithm="HS256")

@router.post("/api/auth/register", status_code=201)
async def register(
    request: RegisterRequest,
    session: Session = Depends(get_db_session)
):
    """Register a new user"""
    import sys
    print(f"📝 Registration attempt for: {request.email}", file=sys.stderr, flush=True)
    try:
        # Check if email already exists
        print(f"🔍 Checking if email exists: {request.email}", file=sys.stderr, flush=True)
        statement = select(User).where(User.email == request.email)
        existing_user = session.exec(statement).first()
        
        if existing_user:
            print(f"❌ Email already registered: {request.email}", file=sys.stderr, flush=True)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Validate password
        print(f"🔑 Validating password (length: {len(request.password)})", file=sys.stderr, flush=True)
        if len(request.password) < 8:
            print(f"❌ Password too short: {len(request.password)} characters", file=sys.stderr, flush=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters"
            )
        
        # Hash password
        print(f"🔐 Hashing password...", file=sys.stderr, flush=True)
        password_hash = hash_password(request.password)
        
        # Create user
        print(f"👤 Creating user...", file=sys.stderr, flush=True)
        user = User(
            email=request.email,
            password_hash=password_hash
        )
        
        session.add(user)
        print(f"💾 Committing user to database...", file=sys.stderr, flush=True)
        session.commit()
        session.refresh(user)
        print(f"✅ User created successfully: {user.email} (ID: {user.id})", file=sys.stderr, flush=True)
        # Note: get_db_session handles commit/rollback, but we need explicit commit here
        
        # Generate JWT
        try:
            token = create_jwt(user.id, user.email)
        except Exception as jwt_error:
            import sys
            print(f"❌ JWT creation error: {jwt_error}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate authentication token: {str(jwt_error)}"
            )
        
        result = {
            "user": {
                "id": user.id,
                "email": user.email
            },
            "accessToken": token
        }
        print(f"✅ Registration successful for: {request.email}", file=sys.stderr, flush=True)
        return result
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        import sys
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        print(f"❌ Registration error: {error_msg}", file=sys.stderr, flush=True)
        print(f"Traceback: {error_trace}", file=sys.stderr, flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {error_msg}"
        )

@router.post("/api/auth/login")
async def login(
    request: LoginRequest,
    session: Session = Depends(get_db_session)
):
    """Login user and return JWT"""
    import sys
    print(f"🔐 Login attempt for: {request.email}", file=sys.stderr, flush=True)
    
    try:
        # Find user by email
        print(f"🔍 Searching for user: {request.email}", file=sys.stderr, flush=True)
        statement = select(User).where(User.email == request.email)
        user = session.exec(statement).first()
        
        if not user:
            print(f"❌ User not found: {request.email}", file=sys.stderr, flush=True)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        print(f"✅ User found: {user.email} (ID: {user.id})", file=sys.stderr, flush=True)
        
        # Verify password
        print(f"🔑 Verifying password...", file=sys.stderr, flush=True)
        try:
            password_valid = verify_password(request.password, user.password_hash)
            print(f"🔑 Password verification result: {password_valid}", file=sys.stderr, flush=True)
        except Exception as pwd_error:
            print(f"❌ Password verification error: {pwd_error}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Password verification failed: {str(pwd_error)}"
            )
        
        if not password_valid:
            print(f"❌ Invalid password for: {request.email}", file=sys.stderr, flush=True)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Generate JWT
        print(f"🎫 Generating JWT for user {user.id}...", file=sys.stderr, flush=True)
        try:
            token = create_jwt(user.id, user.email)
            print(f"✅ JWT generated successfully (length: {len(token)})", file=sys.stderr, flush=True)
        except Exception as jwt_error:
            print(f"❌ JWT creation error: {jwt_error}", file=sys.stderr, flush=True)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate authentication token: {str(jwt_error)}"
            )
        
        result = {
            "user": {
                "id": user.id,
                "email": user.email
            },
            "accessToken": token
        }
        print(f"✅ Login successful for: {request.email}", file=sys.stderr, flush=True)
        return result
        
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions as-is (they'll be handled by the HTTPException handler with CORS)
        print(f"⚠️ HTTPException raised: {http_exc.status_code} - {http_exc.detail}", file=sys.stderr, flush=True)
        raise
    except Exception as e:
        import traceback
        error_msg = str(e)
        error_trace = traceback.format_exc()
        print(f"❌ Unexpected login error: {error_msg}", file=sys.stderr, flush=True)
        print(f"Traceback: {error_trace}", file=sys.stderr, flush=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {error_msg}"
        )

class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    password: str | None = None

@router.put("/api/users/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdateRequest,
    authenticated_user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_db_session)
):
    """Update user information (email and/or password) in Neon database"""
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized - can only update your own account"
        )
    
    # Find the user
    statement = select(User).where(User.id == authenticated_user_id)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update email if provided
    if user_data.email is not None:
        # Check if email is already taken by another user
        email_check = select(User).where(
            User.email == user_data.email,
            User.id != authenticated_user_id
        )
        existing_user = session.exec(email_check).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        user.email = user_data.email
    
    # Update password if provided
    if user_data.password is not None:
        if len(user_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters"
            )
        user.password_hash = hash_password(user_data.password)
    
    # Save changes to Neon database
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {
        "user": {
            "id": user.id,
            "email": user.email
        },
        "message": "User updated successfully"
    }

