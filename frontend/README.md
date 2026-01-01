# Evolution of Todo - Frontend

Next.js frontend for Evolution of Todo Phase II.

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Custom JWT client
- **State Management**: React Hooks

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-256-bit-secret-here
BETTER_AUTH_URL=http://localhost:3000
```

**Important**: `BETTER_AUTH_SECRET` must match the backend secret.

3. Run development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000)

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Landing page
│   ├── login/             # Login page
│   ├── register/          # Registration page
│   └── dashboard/         # Protected dashboard
│       └── tasks/[id]/    # Task details page
├── components/            # React components
│   ├── auth/             # Authentication components
│   ├── layout/           # Layout components
│   ├── tasks/             # Task management components
│   └── ui/                # Reusable UI components
└── lib/                   # Utilities
    ├── auth-client.ts     # Authentication client
    └── api-client.ts      # API client with JWT
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |
| `BETTER_AUTH_SECRET` | JWT signing secret (must match backend) | Yes |
| `BETTER_AUTH_URL` | Frontend URL | Yes |

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

### Features

- ✅ User registration and login
- ✅ JWT-based authentication
- ✅ Protected routes
- ✅ Task CRUD operations
- ✅ Responsive design

## Deployment

Deploy to Vercel:

```bash
vercel --prod
```

Make sure to set environment variables in Vercel dashboard.

## API Integration

The frontend communicates with the backend API at `NEXT_PUBLIC_API_URL`. All authenticated requests automatically include JWT in the `Authorization` header.

**Endpoints Used**:
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/{user_id}/tasks` - List tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
