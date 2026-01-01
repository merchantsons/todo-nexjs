# Authentication Feature Specification — Evolution of Todo (Phase II)

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Approved  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution Article VII (Security Mandates)

---

## Overview

This document defines the authentication feature for Evolution of Todo Phase II, establishing user registration, login, JWT management, and security requirements using Better Auth on the frontend and FastAPI JWT verification on the backend.

**Authentication Strategy**: Stateless JWT  
**Frontend Library**: Better Auth  
**Backend Verification**: python-jose with shared secret  
**Password Security**: bcrypt hashing (cost factor 12+)

---

## Feature Scope

### In Scope (Phase II)
- ✅ User registration with email/password
- ✅ User login with email/password
- ✅ JWT generation and validation
- ✅ Stateless backend authentication
- ✅ User logout (client-side token clearing)
- ✅ Protected routes (redirect to login if unauthenticated)

### Out of Scope (Phase II)
- ❌ OAuth (Google, GitHub) — Phase III
- ❌ Refresh tokens — Phase III
- ❌ Password reset — Phase III
- ❌ Email verification — Phase III
- ❌ Two-factor authentication — Phase IV
- ❌ Role-based access control — Phase IV

---

## User Stories

### US-AUTH-001: User Registration

**As a** new user  
**I want to** create an account with email and password  
**So that** I can securely store my todo items

**Acceptance Criteria**:
- ✅ User can access registration page at `/register`
- ✅ User can enter email and password
- ✅ Email must be valid format (RFC 5322)
- ✅ Password must meet complexity requirements:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one number
- ✅ Password is hashed with bcrypt before storage
- ✅ Email uniqueness is enforced (error if duplicate)
- ✅ Upon success, user receives JWT and is redirected to dashboard
- ✅ Upon failure, clear error message is displayed

**Security Requirements**:
- ✅ Password NEVER sent to backend in plaintext (hashed by Better Auth)
- ✅ Password hash NEVER returned in response
- ✅ Rate limiting on registration endpoint (100 req/hour per IP)

---

### US-AUTH-002: User Login

**As an** existing user  
**I want to** log in with my email and password  
**So that** I can access my todo items

**Acceptance Criteria**:
- ✅ User can access login page at `/login`
- ✅ User can enter email and password
- ✅ Credentials are verified against database
- ✅ Upon success, user receives JWT and is redirected to dashboard
- ✅ Upon failure, generic error message displayed ("Invalid credentials")
- ✅ JWT stored securely in browser (localStorage or httpOnly cookie)

**Security Requirements**:
- ✅ Generic error message (don't reveal if email exists)
- ✅ Password verification uses bcrypt.compare()
- ✅ JWT signed with strong secret (256-bit minimum)
- ✅ JWT includes user_id and expiration claims

---

### US-AUTH-003: Authenticated API Requests

**As a** logged-in user  
**I want** my API requests to be automatically authenticated  
**So that** I can access my data securely

**Acceptance Criteria**:
- ✅ Frontend API client automatically includes JWT in Authorization header
- ✅ Backend validates JWT on every request
- ✅ Invalid/expired JWT returns 401 Unauthorized
- ✅ User is redirected to login on 401 response
- ✅ JWT contains user_id claim for user isolation

**Security Requirements**:
- ✅ JWT signature verified using shared secret
- ✅ JWT expiration checked on every request
- ✅ Backend NEVER trusts client-provided user_id (extracts from JWT)

**Skills Used**: `secure-jwt-guard.md`, `frontend-auth-api-client.md`

---

### US-AUTH-004: User Logout

**As a** logged-in user  
**I want to** log out  
**So that** others cannot access my account on shared devices

**Acceptance Criteria**:
- ✅ User can click logout button
- ✅ JWT is removed from browser storage
- ✅ User is redirected to login page
- ✅ Subsequent API requests return 401 (no JWT)

**Implementation Note**: Stateless logout (client-side token clearing only)

---

### US-AUTH-005: Protected Routes

**As an** unauthenticated visitor  
**I want to** be redirected to login when accessing protected pages  
**So that** I cannot access features without authentication

**Acceptance Criteria**:
- ✅ Dashboard route (`/dashboard`) requires authentication
- ✅ Unauthenticated users redirected to `/login`
- ✅ After login, user redirected back to originally requested page
- ✅ Public routes (`/`, `/login`, `/register`) accessible without auth

---

## Technical Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Better Auth Client                       │ │
│  │  - Login Form Handler                                 │ │
│  │  - Register Form Handler                              │ │
│  │  - JWT Storage Manager                                │ │
│  │  - Token Injection Middleware                         │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Route Protection                         │ │
│  │  - Auth Context Provider                              │ │
│  │  - Protected Route Wrapper                            │ │
│  │  - Redirect Logic                                     │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP + JWT
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          JWT Validation Middleware                    │ │
│  │  - Extract Authorization header                       │ │
│  │  - Verify JWT signature                               │ │
│  │  - Check expiration                                   │ │
│  │  - Extract user_id claim                              │ │
│  │  - Inject into request context                        │ │
│  └───────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────────┐ │
│  │          Authentication Endpoints                     │ │
│  │  - POST /auth/register (Better Auth integration)      │ │
│  │  - POST /auth/login (Better Auth integration)         │ │
│  └───────────────────────────────────────────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ SQL
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              users table                              │ │
│  │  - id, email, password_hash, created_at               │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Frontend Implementation (Next.js + Better Auth)

### Better Auth Configuration

**File**: `lib/auth.ts`

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL,
  },
  secret: process.env.BETTER_AUTH_SECRET,
  session: {
    expiresIn: 60 * 60 * 24, // 24 hours
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Phase II: no email verification
  },
});
```

### Auth Client (Frontend)

**File**: `lib/auth-client.ts`

```typescript
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Usage
await authClient.signUp.email({
  email: "user@example.com",
  password: "SecurePassword123",
});

await authClient.signIn.email({
  email: "user@example.com",
  password: "SecurePassword123",
});

await authClient.signOut();
```

### API Client with JWT Injection

**File**: `lib/api-client.ts`

```typescript
import { authClient } from "./auth-client";

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const session = await authClient.getSession();
  
  if (!session?.accessToken) {
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
    // Redirect to login
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  return response;
}
```

**Skills Used**: `frontend-auth-api-client.md`

### Protected Route Component

**File**: `components/ProtectedRoute.tsx`

```typescript
"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    authClient.getSession().then((session) => {
      if (!session) {
        router.push("/login");
      }
    });
  }, [router]);

  return <>{children}</>;
}
```

---

## Backend Implementation (FastAPI + JWT)

### JWT Validation Dependency

**File**: `app/dependencies/auth.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

security = HTTPBearer()

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Validates JWT and extracts user_id claim.
    Returns user_id if valid, raises 401 if invalid.
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[ALGORITHM])
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

**Skills Used**: `secure-jwt-guard.md`

### Protected Endpoint Example

```python
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user_id

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: int,
    authenticated_user_id: int = Depends(get_current_user_id)
):
    # Verify path user_id matches JWT user_id
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Proceed with user-scoped query
    # ...
```

### User Registration Endpoint

**Note**: Better Auth handles registration automatically, but backend must configure database connection.

**File**: `app/main.py`

```python
from fastapi import FastAPI
from better_auth_fastapi import setup_better_auth

app = FastAPI()

# Better Auth setup (handles /auth/register and /auth/login)
setup_better_auth(
    app,
    secret=os.getenv("BETTER_AUTH_SECRET"),
    database_url=os.getenv("DATABASE_URL"),
)
```

---

## Security Requirements

### Password Security

| Requirement | Implementation |
|-------------|----------------|
| Minimum length | 8 characters (enforced client + server) |
| Complexity | Uppercase + lowercase + number (enforced client) |
| Hashing algorithm | bcrypt with cost factor 12+ |
| Salt | Unique per password (bcrypt automatic) |
| Storage | NEVER store plaintext, only hash |

### JWT Security

| Requirement | Implementation |
|-------------|----------------|
| Signature algorithm | HS256 (HMAC with SHA-256) |
| Secret length | 256-bit minimum (32 characters) |
| Secret storage | Environment variable, NEVER hardcoded |
| Expiration | 24 hours (configurable) |
| Claims | user_id, email, iat, exp |
| Transmission | Authorization: Bearer header (HTTPS only in prod) |

### Authentication Flow Security

| Threat | Mitigation |
|--------|-----------|
| Brute force login | Rate limiting (100 attempts/hour per IP) |
| Credential stuffing | Rate limiting + CAPTCHA (Phase III) |
| Token theft | HTTPS only in production |
| XSS token stealing | httpOnly cookies OR secure localStorage |
| CSRF | SameSite cookies OR CSRF tokens |
| Timing attacks | Constant-time password comparison (bcrypt) |

---

## Error Handling

### Frontend Error Messages

| Scenario | User-Facing Message |
|----------|---------------------|
| Invalid email format | "Please enter a valid email address" |
| Password too short | "Password must be at least 8 characters" |
| Missing uppercase | "Password must contain at least one uppercase letter" |
| Missing number | "Password must contain at least one number" |
| Duplicate email | "An account with this email already exists" |
| Invalid credentials | "Invalid email or password" |
| Network error | "Unable to connect. Please try again." |
| Server error | "Something went wrong. Please try again later." |

### Backend Error Responses

| Status | Condition | Response |
|--------|-----------|----------|
| 400 | Invalid email format | `{"detail": "Invalid email format"}` |
| 400 | Password too short | `{"detail": "Password must be at least 8 characters"}` |
| 409 | Duplicate email | `{"detail": "Email already registered"}` |
| 401 | Invalid credentials | `{"detail": "Invalid credentials"}` |
| 401 | Missing JWT | `{"detail": "Unauthorized"}` |
| 401 | Invalid JWT | `{"detail": "Invalid or expired token"}` |

---

## Testing Strategy

### Manual Test Cases

#### Test 1: User Registration Success
1. Navigate to `/register`
2. Enter valid email: `test@example.com`
3. Enter valid password: `SecurePass123`
4. Submit form
5. **Expected**: Redirect to dashboard, JWT stored, user_id visible

#### Test 2: User Registration Duplicate Email
1. Register user with `test@example.com`
2. Attempt to register again with same email
3. **Expected**: Error message "Email already registered"

#### Test 3: User Login Success
1. Navigate to `/login`
2. Enter registered email: `test@example.com`
3. Enter correct password: `SecurePass123`
4. Submit form
5. **Expected**: Redirect to dashboard, JWT stored

#### Test 4: User Login Invalid Credentials
1. Navigate to `/login`
2. Enter email: `test@example.com`
3. Enter wrong password: `WrongPass123`
4. Submit form
5. **Expected**: Error message "Invalid credentials"

#### Test 5: Protected Route Without Auth
1. Clear JWT from storage
2. Navigate to `/dashboard`
3. **Expected**: Redirect to `/login`

#### Test 6: API Request Without JWT
1. Send API request without Authorization header
2. **Expected**: 401 Unauthorized response

#### Test 7: API Request With Invalid JWT
1. Send API request with tampered JWT
2. **Expected**: 401 Unauthorized response

#### Test 8: User Logout
1. Log in successfully
2. Click logout button
3. **Expected**: Redirect to login, JWT cleared
4. Attempt to access dashboard
5. **Expected**: Redirect to login

---

## Performance Requirements

| Metric | Target |
|--------|--------|
| Login response time | < 300ms |
| Registration response time | < 500ms |
| JWT validation time | < 10ms |
| Password hashing time | < 200ms (bcrypt) |

---

## Phase Compliance

### Phase II Allowed ✅
- ✅ Email/password authentication
- ✅ JWT-based stateless auth
- ✅ User registration and login
- ✅ Protected routes
- ✅ bcrypt password hashing

### Phase II Forbidden ❌
- ❌ OAuth (Google, GitHub)
- ❌ Refresh tokens
- ❌ Password reset
- ❌ Email verification
- ❌ Two-factor authentication
- ❌ Role-based access control

**Constitutional Compliance**: ✅ This feature adheres to Article VII (Security Mandates)

---

## References

- Constitution: `.specify/memory/constitution.md` (Article VII)
- Architecture: `specs/architecture.md`
- Database Schema: `specs/database/schema.md`
- Skills: `.claude/skills/secure-jwt-guard.md`, `.claude/skills/frontend-auth-api-client.md`
- Better Auth Docs: https://www.better-auth.com
- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/

---

**Status**: ✅ Approved for Implementation  
**Next Step**: Proceed to Task CRUD feature specification

