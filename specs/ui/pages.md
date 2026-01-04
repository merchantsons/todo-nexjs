# UI Pages Specification — Evolution of Todo (Phase II)

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Approved  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution Article II (Spec-First Doctrine)

---

## Overview

This document defines all user-facing pages for Evolution of Todo Phase II frontend, establishing layouts, routes, components, navigation flows, and responsive design requirements.

**Framework**: Next.js 16+ (App Router)  
**Styling**: Tailwind CSS  
**Routing**: File-based (Next.js convention)  
**Authentication**: Protected routes with Better Auth

---

## Page Inventory

| Page | Route | Auth Required | Purpose |
|------|-------|---------------|---------|
| Landing | `/` | ❌ No | Welcome page with app intro |
| Login | `/login` | ❌ No | User login form |
| Register | `/register` | ❌ No | User registration form |
| Dashboard | `/dashboard` | ✅ Yes | Main task management interface |
| Task Details | `/dashboard/tasks/[id]` | ✅ Yes | Single task view/edit |

---

## Page: Landing (`/`)

### Purpose
Introduce the application and guide users to login or register.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Evolution of Todo                      [Login] [Register]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                   Evolution of Todo                         │
│         Your personal task management solution              │
│                                                             │
│              [Get Started →] (routes to /register)          │
│              Already have an account? [Log in]              │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  ✓ Secure    │  │  ✓ Simple    │  │  ✓ Private   │     │
│  │  Your data   │  │  Clean UI    │  │  Your tasks  │     │
│  │  protected   │  │  easy to use │  │  only yours  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components
- `<Header>` — Navigation bar
- `<HeroSection>` — Main call-to-action
- `<FeatureCards>` — App benefits

### User Actions
- Click "Get Started" → Navigate to `/register`
- Click "Log in" → Navigate to `/login`
- Click "Login" button (header) → Navigate to `/login`
- Click "Register" button (header) → Navigate to `/register`

### Responsive Design
- **Desktop**: Full-width hero, 3-column feature cards
- **Tablet**: Full-width hero, 2-column feature cards
- **Mobile**: Stacked layout, single-column feature cards

### File Location
`app/page.tsx`

---

## Page: Login (`/login`)

### Purpose
Allow existing users to authenticate with email and password.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Evolution of Todo                           [← Back Home]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              ┌─────────────────────────────┐               │
│              │      Log in to your account │               │
│              │                             │               │
│              │  Email                      │               │
│              │  [________________]         │               │
│              │                             │               │
│              │  Password                   │               │
│              │  [________________] [👁]    │               │
│              │                             │               │
│              │  [Login Button (Primary)]  │               │
│              │                             │               │
│              │  Don't have an account?     │               │
│              │  [Sign up →]                │               │
│              └─────────────────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components
- `<Header>` — Navigation bar
- `<LoginForm>` — Email/password form with validation

### Form Fields

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Email | text | Yes | Valid email format |
| Password | password | Yes | Not empty |

### User Actions
- Enter email and password
- Click "Login" → Authenticate via Better Auth
- On success → Navigate to `/dashboard`
- On failure → Display error message
- Click "Sign up" link → Navigate to `/register`
- Click "Back Home" → Navigate to `/`

### Error Handling

| Error | Message |
|-------|---------|
| Invalid credentials | "Invalid email or password" |
| Empty email | "Email is required" |
| Invalid email format | "Please enter a valid email address" |
| Empty password | "Password is required" |
| Network error | "Unable to connect. Please try again." |

### Success Flow
1. User submits credentials
2. Better Auth validates and issues JWT
3. JWT stored in localStorage/cookies
4. Redirect to `/dashboard`

### Responsive Design
- **Desktop**: Centered card (max-width 400px)
- **Tablet**: Centered card (max-width 400px)
- **Mobile**: Full-width form with padding

### File Location
`app/login/page.tsx`

---

## Page: Register (`/register`)

### Purpose
Allow new users to create an account with email and password.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Evolution of Todo                           [← Back Home]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              ┌─────────────────────────────┐               │
│              │   Create your account       │               │
│              │                             │               │
│              │  Email                      │               │
│              │  [________________]         │               │
│              │                             │               │
│              │  Password                   │               │
│              │  [________________] [👁]    │               │
│              │  • Min 8 characters         │               │
│              │  • Uppercase + lowercase    │               │
│              │  • At least one number      │               │
│              │                             │               │
│              │  [Register Button (Primary)]│               │
│              │                             │               │
│              │  Already have an account?   │               │
│              │  [Log in →]                 │               │
│              └─────────────────────────────┘               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components
- `<Header>` — Navigation bar
- `<RegisterForm>` — Registration form with validation
- `<PasswordStrengthIndicator>` — Visual password strength

### Form Fields

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| Email | text | Yes | Valid email format, unique |
| Password | password | Yes | Min 8 chars, uppercase, lowercase, number |

### User Actions
- Enter email and password
- See real-time password strength indicator
- Click "Register" → Create account via Better Auth
- On success → Navigate to `/dashboard`
- On failure → Display error message
- Click "Log in" link → Navigate to `/login`
- Click "Back Home" → Navigate to `/`

### Error Handling

| Error | Message |
|-------|---------|
| Email already exists | "An account with this email already exists" |
| Empty email | "Email is required" |
| Invalid email format | "Please enter a valid email address" |
| Password too short | "Password must be at least 8 characters" |
| Missing uppercase | "Password must contain at least one uppercase letter" |
| Missing lowercase | "Password must contain at least one lowercase letter" |
| Missing number | "Password must contain at least one number" |
| Network error | "Unable to create account. Please try again." |

### Success Flow
1. User submits registration
2. Better Auth creates account and issues JWT
3. JWT stored in localStorage/cookies
4. Redirect to `/dashboard`

### Responsive Design
- **Desktop**: Centered card (max-width 400px)
- **Tablet**: Centered card (max-width 400px)
- **Mobile**: Full-width form with padding

### File Location
`app/register/page.tsx`

---

## Page: Dashboard (`/dashboard`)

### Purpose
Main task management interface where users view and manage their tasks.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Evolution of Todo    Hi, user@example.com    [Logout]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  My Tasks                                                   │
│  [+ New Task]                                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ☐ Buy groceries                      [Edit] [Delete]│   │
│  │   Milk, eggs, bread                                  │   │
│  │   Created 2 hours ago                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ☑ Finish hackathon                   [Edit] [Delete]│   │
│  │   Complete Phase II implementation                   │   │
│  │   Completed 1 hour ago                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ☐ Read documentation                 [Edit] [Delete]│   │
│  │   FastAPI and SQLModel docs                          │   │
│  │   Created 30 minutes ago                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components
- `<Header>` — Navigation bar with user email and logout
- `<TaskList>` — List of all user's tasks
- `<TaskCard>` — Individual task display
- `<NewTaskButton>` — Action button to create task
- `<TaskForm>` — Modal or inline form for create/edit
- `<EmptyState>` — Message when no tasks exist

### User Actions
- Click "New Task" → Show task creation form
- Click checkbox → Toggle task completion (PATCH API)
- Click "Edit" → Show task edit form
- Click "Delete" → Show confirmation, delete task (DELETE API)
- Click task card → Navigate to `/dashboard/tasks/[id]`
- Click "Logout" → Clear JWT, navigate to `/login`

### Empty State

**When**: User has no tasks  
**Message**: "No tasks yet. Create your first task to get started!"  
**Action**: Prominent "Create Task" button

### Data Loading States

| State | Display |
|-------|---------|
| Loading | Skeleton cards with loading animation |
| Success | Task list with all tasks |
| Empty | Empty state message |
| Error | Error message with retry button |

### Responsive Design
- **Desktop**: 2-column task grid (max-width 1200px)
- **Tablet**: 2-column task grid
- **Mobile**: Single-column stacked tasks

### Protected Route
✅ Requires authentication — redirects to `/login` if no JWT

### File Location
`app/dashboard/page.tsx`

---

## Page: Task Details (`/dashboard/tasks/[id]`)

### Purpose
View and edit detailed information for a specific task.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  [← Back to Dashboard]              Hi, user@example.com    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Task Details                                               │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Title                                                │   │
│  │ [Buy groceries                              ]       │   │
│  │                                                      │   │
│  │ Description                                          │   │
│  │ ┌──────────────────────────────────────────────┐   │   │
│  │ │ Milk, eggs, bread, vegetables                │   │   │
│  │ │                                              │   │   │
│  │ └──────────────────────────────────────────────┘   │   │
│  │                                                      │   │
│  │ Status                                               │   │
│  │ ☐ Mark as complete                                  │   │
│  │                                                      │   │
│  │ Created: January 2, 2026 at 10:00 AM                │   │
│  │ Last updated: January 2, 2026 at 10:00 AM           │   │
│  │                                                      │   │
│  │ [Save Changes]  [Delete Task]                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components
- `<Header>` — Navigation bar with back button
- `<TaskDetailForm>` — Editable task form
- `<DeleteConfirmation>` — Modal for delete confirmation

### Form Fields

| Field | Type | Editable | Validation |
|-------|------|----------|------------|
| Title | text | Yes | Required, max 255 chars |
| Description | textarea | Yes | Optional, max 10,000 chars |
| Completed | checkbox | Yes | Boolean |
| Created At | timestamp | No (display only) | ISO 8601 |
| Updated At | timestamp | No (display only) | ISO 8601 |

### User Actions
- Edit title, description, or completion status
- Click "Save Changes" → Update task (PUT API)
- Click "Delete Task" → Show confirmation modal
- Confirm delete → Delete task (DELETE API), navigate to `/dashboard`
- Click "Back to Dashboard" → Navigate to `/dashboard`

### Error Handling

| Error | Message |
|-------|---------|
| Task not found | Display 404 page "Task not found" |
| Unauthorized | Redirect to `/login` |
| Validation error | Inline field error messages |
| Network error | "Unable to save changes. Please try again." |

### Success Flow
1. User loads page → Fetch task (GET API)
2. User edits fields
3. User clicks "Save" → Update task (PUT API)
4. Show success message → Auto-dismiss after 3 seconds
5. Updated data displayed

### Responsive Design
- **Desktop**: Centered form (max-width 600px)
- **Tablet**: Centered form (max-width 600px)
- **Mobile**: Full-width form with padding

### Protected Route
✅ Requires authentication — redirects to `/login` if no JWT

### File Location
`app/dashboard/tasks/[id]/page.tsx`

---

## Navigation Flow

```
        ┌─────────┐
        │   `/`   │ Landing Page
        └────┬────┘
             │
      ┌──────┴──────┐
      │             │
      ↓             ↓
┌──────────┐   ┌──────────┐
│ /login   │   │/register │
└────┬─────┘   └────┬─────┘
     │              │
     └──────┬───────┘
            │ (After auth)
            ↓
     ┌──────────────┐
     │ /dashboard   │ Main app
     └──────┬───────┘
            │
            ↓
     ┌─────────────────────┐
     │ /dashboard/tasks/[id]│ Task details
     └─────────────────────┘
```

---

## Route Protection

### Public Routes (No Auth Required)
- `/` — Landing page
- `/login` — Login page
- `/register` — Registration page

### Protected Routes (Auth Required)
- `/dashboard` — Task list
- `/dashboard/tasks/[id]` — Task details

**Implementation**: `<ProtectedRoute>` wrapper component checks JWT, redirects to `/login` if missing

---

## Theme and Styling

### Color Palette

| Element | Color | Tailwind Class |
|---------|-------|----------------|
| Primary | Blue | `bg-blue-600` |
| Secondary | Gray | `bg-gray-200` |
| Success | Green | `bg-green-500` |
| Danger | Red | `bg-red-500` |
| Background | White | `bg-white` |
| Text Primary | Dark Gray | `text-gray-900` |
| Text Secondary | Medium Gray | `text-gray-600` |
| Border | Light Gray | `border-gray-300` |

### Typography

| Element | Font | Size | Tailwind Class |
|---------|------|------|----------------|
| H1 | Inter | 2.5rem | `text-4xl font-bold` |
| H2 | Inter | 2rem | `text-3xl font-semibold` |
| H3 | Inter | 1.5rem | `text-2xl font-semibold` |
| Body | Inter | 1rem | `text-base` |
| Small | Inter | 0.875rem | `text-sm` |

### Spacing

| Element | Spacing | Tailwind Class |
|---------|---------|----------------|
| Container | Max 1200px | `max-w-7xl mx-auto` |
| Section Padding | 2rem | `p-8` |
| Card Padding | 1.5rem | `p-6` |
| Button Padding | 0.75rem 1.5rem | `px-6 py-3` |
| Form Field Gap | 1rem | `space-y-4` |

---

## Accessibility Requirements

### Keyboard Navigation
- ✅ All interactive elements focusable
- ✅ Logical tab order
- ✅ Visible focus indicators
- ✅ Escape key closes modals

### Screen Readers
- ✅ Semantic HTML (header, nav, main, section)
- ✅ ARIA labels for icon buttons
- ✅ Alt text for images
- ✅ Form labels associated with inputs

### Color Contrast
- ✅ WCAG AA compliance (4.5:1 for normal text)
- ✅ WCAG AAA compliance (7:1 for important text)

---

## Performance Requirements

| Metric | Target |
|--------|--------|
| First Contentful Paint | < 1.5s |
| Time to Interactive | < 3s |
| Lighthouse Performance Score | > 90 |
| Lighthouse Accessibility Score | > 95 |

---

## Phase Compliance

### Phase II Allowed ✅
- ✅ Landing, login, register, dashboard, task details pages
- ✅ Protected routes with authentication
- ✅ Responsive design (desktop, tablet, mobile)
- ✅ Task CRUD operations

### Phase II Forbidden ❌
- ❌ Real-time collaboration pages (Phase III)
- ❌ Admin/settings pages (Phase III)
- ❌ Shared task views (Phase III)
- ❌ Team management pages (Phase IV)

**Constitutional Compliance**: ✅ This specification adheres to Article II (Spec-First Doctrine)

---

## References

- Architecture: `specs/architecture.md`
- Authentication Feature: `specs/features/authentication.md`
- Task CRUD Feature: `specs/features/task-crud.md`
- Component Specification: `specs/ui/components.md`
- Next.js App Router: https://nextjs.org/docs/app

---

**Status**: ✅ Approved for Implementation  
**Next Step**: Proceed to UI components specification




