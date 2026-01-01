# Evolution of Todo — Phase II

**Hackathon**: Hackathon II  
**Phase**: Phase II — Full-Stack Web Application  
**Status**: Implementation Complete, Testing Pending

---

## Overview

Evolution of Todo is a secure, multi-user todo management web application built with modern full-stack technologies. Phase II delivers a production-ready application with JWT authentication, user isolation, and complete task management features.

**Tech Stack**:
- **Frontend**: Next.js 16+ with TypeScript and Tailwind CSS
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Stateless JWT

---

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.13+
- PostgreSQL database (Neon recommended)

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=your-256-bit-secret-here
CORS_ORIGINS=http://localhost:3000
EOF

# Initialize database
python init_db.py

# Start server
uvicorn app.main:app --reload
```

Backend runs on http://localhost:8000

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-256-bit-secret-here
BETTER_AUTH_URL=http://localhost:3000
EOF

# Start development server
npm run dev
```

Frontend runs on http://localhost:3000

**Important**: `BETTER_AUTH_SECRET` must be identical in both `.env` files.

---

## Features

### Authentication
- ✅ User registration with email/password
- ✅ User login with JWT generation
- ✅ Protected routes
- ✅ Secure password hashing (bcrypt)

### Task Management
- ✅ Create tasks with title and description
- ✅ List all user's tasks
- ✅ View task details
- ✅ Update tasks
- ✅ Delete tasks
- ✅ Toggle task completion

### Security
- ✅ JWT authentication on all endpoints
- ✅ User isolation (users can only access their own tasks)
- ✅ Stateless backend (horizontally scalable)
- ✅ Password hashing with bcrypt

---

## Project Structure

```
todo-nexjs/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/      # SQLModel definitions
│   │   ├── routes/      # API endpoints
│   │   ├── dependencies/ # Auth & database
│   │   └── main.py      # FastAPI app
│   ├── init_db.py       # Database initialization
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── app/             # Pages (App Router)
│   ├── components/      # React components
│   └── lib/             # Utilities
├── specs/               # Specifications
└── history/             # Prompt History Records
```

---

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

### Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/health` | Health check | No |
| POST | `/api/auth/register` | Register user | No |
| POST | `/api/auth/login` | Login user | No |
| GET | `/api/{user_id}/tasks` | List tasks | Yes |
| POST | `/api/{user_id}/tasks` | Create task | Yes |
| GET | `/api/{user_id}/tasks/{id}` | Get task | Yes |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | Yes |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | Yes |

---

## Development

### Backend Development

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Database Migrations

To recreate database tables:
```bash
cd backend
python init_db.py
```

---

## Testing

### Manual Testing Checklist

1. **Registration**
   - Navigate to `/register`
   - Create account with valid email/password
   - Verify redirect to dashboard

2. **Login**
   - Navigate to `/login`
   - Login with registered credentials
   - Verify redirect to dashboard

3. **Task Operations**
   - Create new task
   - View task list
   - Edit task
   - Toggle completion
   - Delete task

4. **Security**
   - Login as User A, create task
   - Login as User B
   - Verify User B cannot see User A's tasks

---

## Deployment

### Backend (Vercel)

1. Create `vercel.json` in backend directory
2. Deploy: `vercel --prod`
3. Set environment variables in Vercel dashboard

### Frontend (Vercel)

1. Deploy: `vercel --prod`
2. Set environment variables in Vercel dashboard
3. Update `NEXT_PUBLIC_API_URL` to production backend URL

### Database (Neon)

1. Create Neon project
2. Copy connection string to `DATABASE_URL`
3. Run `init_db.py` with production DATABASE_URL

---

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=your-256-bit-secret-here
CORS_ORIGINS=http://localhost:3000,https://yourdomain.vercel.app
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-256-bit-secret-here
BETTER_AUTH_URL=http://localhost:3000
```

---

## Security Notes

- ✅ Passwords are hashed with bcrypt (cost factor 12)
- ✅ JWT tokens expire after 24 hours
- ✅ All API endpoints require JWT authentication
- ✅ User isolation enforced at database query level
- ✅ CORS configured for allowed origins only

---

## Specifications

All specifications are in the `specs/` directory:
- `overview.md` - Project overview
- `architecture.md` - System architecture
- `database/schema.md` - Database design
- `api/rest-endpoints.md` - API contracts
- `features/authentication.md` - Auth specification
- `features/task-crud.md` - Task operations
- `ui/pages.md` - Frontend pages
- `ui/components.md` - UI components

---

## License

Hackathon project for educational purposes.

---

**Status**: ✅ Code Complete | ⚠️ Testing & Deployment Pending

