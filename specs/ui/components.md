# UI Components Specification — Evolution of Todo (Phase II)

**Version**: 1.0.0  
**Last Updated**: 2026-01-02  
**Status**: Approved  
**Phase**: Phase II — Full-Stack Web Application  
**Authority**: SpecKitPlus Constitution Article II (Spec-First Doctrine)

---

## Overview

This document defines all reusable UI components for Evolution of Todo Phase II frontend, establishing component APIs, props, states, and styling requirements for a consistent, maintainable React component library.

**Framework**: React 19+ with TypeScript  
**Styling**: Tailwind CSS  
**Component Pattern**: Function components with hooks  
**File Convention**: PascalCase (e.g., `Button.tsx`)

---

## Component Library Inventory

| Component | Category | Reusable | Description |
|-----------|----------|----------|-------------|
| `<Button>` | Atom | ✅ Yes | Primary/secondary action button |
| `<Input>` | Atom | ✅ Yes | Text input with validation |
| `<Textarea>` | Atom | ✅ Yes | Multi-line text input |
| `<Checkbox>` | Atom | ✅ Yes | Checkbox with label |
| `<Header>` | Organism | ✅ Yes | Navigation bar |
| `<LoginForm>` | Organism | ❌ No | Login form with validation |
| `<RegisterForm>` | Organism | ❌ No | Registration form with validation |
| `<TaskCard>` | Molecule | ✅ Yes | Individual task display |
| `<TaskList>` | Organism | ✅ Yes | Task list container |
| `<TaskForm>` | Organism | ✅ Yes | Create/edit task form |
| `<EmptyState>` | Molecule | ✅ Yes | Empty state message |
| `<LoadingSpinner>` | Atom | ✅ Yes | Loading indicator |
| `<ErrorMessage>` | Atom | ✅ Yes | Error display |
| `<ConfirmDialog>` | Molecule | ✅ Yes | Confirmation modal |
| `<ProtectedRoute>` | HOC | ✅ Yes | Auth route wrapper |

---

## Atomic Components

### Component: `<Button>`

**Purpose**: Primary, secondary, and danger action buttons

**Props**:
```typescript
interface ButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "danger";
  type?: "button" | "submit" | "reset";
  onClick?: () => void;
  disabled?: boolean;
  fullWidth?: boolean;
  className?: string;
}
```

**Variants**:
- **Primary**: Blue background, white text (main actions)
- **Secondary**: Gray background, dark text (cancel actions)
- **Danger**: Red background, white text (delete actions)

**Styles**:
```tsx
// Primary
className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"

// Secondary
className="bg-gray-200 hover:bg-gray-300 text-gray-900 px-6 py-3 rounded-lg"

// Danger
className="bg-red-500 hover:bg-red-600 text-white px-6 py-3 rounded-lg"
```

**States**:
- Default
- Hover (darker shade)
- Disabled (opacity 50%, no pointer events)
- Focus (outline ring)

**Usage**:
```tsx
<Button variant="primary" onClick={handleSubmit}>
  Save Changes
</Button>

<Button variant="danger" onClick={handleDelete}>
  Delete Task
</Button>
```

**File Location**: `components/ui/Button.tsx`

---

### Component: `<Input>`

**Purpose**: Single-line text input with validation and error messages

**Props**:
```typescript
interface InputProps {
  label: string;
  type?: "text" | "email" | "password";
  value: string;
  onChange: (value: string) => void;
  error?: string;
  required?: boolean;
  placeholder?: string;
  disabled?: boolean;
  maxLength?: number;
  className?: string;
}
```

**Features**:
- ✅ Floating label (moves up when focused or has value)
- ✅ Error state with red border and message
- ✅ Character counter (if maxLength provided)
- ✅ Password visibility toggle (if type="password")

**Styles**:
```tsx
// Default
className="border border-gray-300 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"

// Error state
className="border border-red-500 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-red-500"
```

**States**:
- Default (gray border)
- Focus (blue ring)
- Error (red border, error message below)
- Disabled (gray background, no interaction)

**Usage**:
```tsx
<Input
  label="Email"
  type="email"
  value={email}
  onChange={setEmail}
  error={emailError}
  required
  placeholder="you@example.com"
/>
```

**File Location**: `components/ui/Input.tsx`

---

### Component: `<Textarea>`

**Purpose**: Multi-line text input for descriptions

**Props**:
```typescript
interface TextareaProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  required?: boolean;
  placeholder?: string;
  rows?: number;
  maxLength?: number;
  className?: string;
}
```

**Features**:
- ✅ Auto-resize (optional)
- ✅ Character counter
- ✅ Error state

**Styles**:
```tsx
className="border border-gray-300 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 resize-vertical"
```

**Usage**:
```tsx
<Textarea
  label="Description"
  value={description}
  onChange={setDescription}
  placeholder="Enter task description..."
  rows={4}
  maxLength={10000}
/>
```

**File Location**: `components/ui/Textarea.tsx`

---

### Component: `<Checkbox>`

**Purpose**: Checkbox with label for task completion

**Props**:
```typescript
interface CheckboxProps {
  label?: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
  className?: string;
}
```

**Features**:
- ✅ Custom checkmark icon
- ✅ Accessible (keyboard navigable)

**Styles**:
```tsx
// Unchecked
className="w-5 h-5 border-2 border-gray-400 rounded"

// Checked
className="w-5 h-5 bg-blue-600 border-2 border-blue-600 rounded flex items-center justify-center"
```

**Usage**:
```tsx
<Checkbox
  checked={completed}
  onChange={setCompleted}
  label="Mark as complete"
/>
```

**File Location**: `components/ui/Checkbox.tsx`

---

### Component: `<LoadingSpinner>`

**Purpose**: Animated loading indicator

**Props**:
```typescript
interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
  color?: string;
  className?: string;
}
```

**Styles**:
```tsx
// Medium size
className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"
```

**Usage**:
```tsx
<LoadingSpinner size="md" />
```

**File Location**: `components/ui/LoadingSpinner.tsx`

---

### Component: `<ErrorMessage>`

**Purpose**: Display error messages with icon

**Props**:
```typescript
interface ErrorMessageProps {
  message: string;
  onClose?: () => void;
  className?: string;
}
```

**Styles**:
```tsx
className="bg-red-50 border border-red-200 text-red-800 px-4 py-3 rounded-lg flex items-center gap-2"
```

**Usage**:
```tsx
<ErrorMessage message="Unable to save task" onClose={clearError} />
```

**File Location**: `components/ui/ErrorMessage.tsx`

---

## Molecule Components

### Component: `<TaskCard>`

**Purpose**: Display individual task with actions

**Props**:
```typescript
interface TaskCardProps {
  task: {
    id: number;
    title: string;
    description: string | null;
    completed: boolean;
    created_at: string;
    updated_at: string;
  };
  onToggleComplete: (id: number, completed: boolean) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}
```

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ ☐ Task Title                     [Edit] [Delete]│
│   Task description preview...                    │
│   Created 2 hours ago                            │
└─────────────────────────────────────────────────┘
```

**Features**:
- ✅ Checkbox for completion toggle
- ✅ Strikethrough text when completed
- ✅ Truncated description (max 100 characters)
- ✅ Relative timestamp ("2 hours ago")
- ✅ Edit and delete buttons (visible on hover)

**Styles**:
```tsx
// Default
className="border border-gray-300 rounded-lg p-6 hover:shadow-lg transition-shadow"

// Completed
className="border border-gray-300 rounded-lg p-6 bg-gray-50 opacity-75"
```

**Usage**:
```tsx
<TaskCard
  task={task}
  onToggleComplete={handleToggle}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

**File Location**: `components/tasks/TaskCard.tsx`

---

### Component: `<EmptyState>`

**Purpose**: Display message when no tasks exist

**Props**:
```typescript
interface EmptyStateProps {
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}
```

**Layout**:
```
┌─────────────────────────────────┐
│         📋 (Icon)               │
│     No tasks yet                │
│  Create your first task to      │
│  get started!                   │
│                                 │
│  [Create Task]                  │
└─────────────────────────────────┘
```

**Usage**:
```tsx
<EmptyState
  title="No tasks yet"
  message="Create your first task to get started!"
  actionLabel="Create Task"
  onAction={openTaskForm}
/>
```

**File Location**: `components/tasks/EmptyState.tsx`

---

### Component: `<ConfirmDialog>`

**Purpose**: Modal confirmation dialog for destructive actions

**Props**:
```typescript
interface ConfirmDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
  variant?: "danger" | "warning";
}
```

**Layout**:
```
┌─────────────────────────────────┐
│ Delete Task?                    │
│                                 │
│ Are you sure you want to delete │
│ this task? This action cannot   │
│ be undone.                      │
│                                 │
│        [Cancel]  [Delete]       │
└─────────────────────────────────┘
```

**Features**:
- ✅ Modal overlay (darkened background)
- ✅ Focus trap (Escape key closes)
- ✅ Click outside to close

**Usage**:
```tsx
<ConfirmDialog
  isOpen={showConfirm}
  title="Delete Task?"
  message="Are you sure you want to delete this task? This action cannot be undone."
  confirmLabel="Delete"
  cancelLabel="Cancel"
  onConfirm={handleConfirmDelete}
  onCancel={closeConfirmDialog}
  variant="danger"
/>
```

**File Location**: `components/ui/ConfirmDialog.tsx`

---

## Organism Components

### Component: `<Header>`

**Purpose**: Top navigation bar with branding and user info

**Props**:
```typescript
interface HeaderProps {
  user?: {
    email: string;
  };
  onLogout?: () => void;
}
```

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ Evolution of Todo    Hi, user@email.com [Logout]│
└─────────────────────────────────────────────────┘
```

**Variants**:
- **Logged Out**: Logo + Login/Register buttons
- **Logged In**: Logo + User email + Logout button

**Responsive**:
- **Desktop**: Full layout
- **Mobile**: Hamburger menu (optional for Phase II)

**Usage**:
```tsx
<Header user={currentUser} onLogout={handleLogout} />
```

**File Location**: `components/layout/Header.tsx`

---

### Component: `<LoginForm>`

**Purpose**: Login form with email/password validation

**Props**:
```typescript
interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  error?: string;
}
```

**Features**:
- ✅ Email and password fields
- ✅ Client-side validation
- ✅ Password visibility toggle
- ✅ Loading state during submission
- ✅ Error message display
- ✅ Link to registration page

**Usage**:
```tsx
<LoginForm onSubmit={handleLogin} error={loginError} />
```

**File Location**: `components/auth/LoginForm.tsx`

---

### Component: `<RegisterForm>`

**Purpose**: Registration form with email/password validation

**Props**:
```typescript
interface RegisterFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  error?: string;
}
```

**Features**:
- ✅ Email and password fields
- ✅ Client-side validation (password complexity)
- ✅ Password strength indicator
- ✅ Password visibility toggle
- ✅ Loading state during submission
- ✅ Error message display
- ✅ Link to login page

**Usage**:
```tsx
<RegisterForm onSubmit={handleRegister} error={registerError} />
```

**File Location**: `components/auth/RegisterForm.tsx`

---

### Component: `<TaskList>`

**Purpose**: Container for displaying all user's tasks

**Props**:
```typescript
interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  error?: string;
  onToggleComplete: (id: number, completed: boolean) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
  onCreateTask: () => void;
}
```

**Features**:
- ✅ Loading skeleton when fetching
- ✅ Empty state when no tasks
- ✅ Error message on failure
- ✅ "New Task" button
- ✅ Responsive grid layout

**States**:
- Loading → Show `<LoadingSpinner>`
- Error → Show `<ErrorMessage>`
- Empty → Show `<EmptyState>`
- Success → Show `<TaskCard>` list

**Usage**:
```tsx
<TaskList
  tasks={tasks}
  loading={isLoading}
  error={error}
  onToggleComplete={handleToggle}
  onEdit={handleEdit}
  onDelete={handleDelete}
  onCreateTask={openTaskForm}
/>
```

**File Location**: `components/tasks/TaskList.tsx`

---

### Component: `<TaskForm>`

**Purpose**: Create or edit task with title, description, completion

**Props**:
```typescript
interface TaskFormProps {
  task?: {
    id: number;
    title: string;
    description: string | null;
    completed: boolean;
  };
  onSubmit: (data: { title: string; description: string | null; completed: boolean }) => Promise<void>;
  onCancel: () => void;
  submitLabel?: string;
}
```

**Features**:
- ✅ Title input (required)
- ✅ Description textarea (optional)
- ✅ Completion checkbox (edit mode only)
- ✅ Client-side validation
- ✅ Loading state during submission
- ✅ Error message display

**Modes**:
- **Create**: Empty form, no completion checkbox
- **Edit**: Pre-filled form with completion checkbox

**Usage**:
```tsx
// Create mode
<TaskForm onSubmit={handleCreate} onCancel={closeForm} submitLabel="Create Task" />

// Edit mode
<TaskForm task={existingTask} onSubmit={handleUpdate} onCancel={closeForm} submitLabel="Save Changes" />
```

**File Location**: `components/tasks/TaskForm.tsx`

---

## Higher-Order Components

### Component: `<ProtectedRoute>`

**Purpose**: Wrapper component to protect authenticated routes

**Props**:
```typescript
interface ProtectedRouteProps {
  children: React.ReactNode;
}
```

**Features**:
- ✅ Checks for JWT in storage
- ✅ Redirects to `/login` if unauthenticated
- ✅ Shows loading spinner during auth check

**Usage**:
```tsx
// In page component
export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <TaskList />
    </ProtectedRoute>
  );
}
```

**File Location**: `components/auth/ProtectedRoute.tsx`

---

## Component Structure

### File Organization

```
components/
├── auth/
│   ├── LoginForm.tsx
│   ├── RegisterForm.tsx
│   └── ProtectedRoute.tsx
├── layout/
│   └── Header.tsx
├── tasks/
│   ├── TaskCard.tsx
│   ├── TaskList.tsx
│   ├── TaskForm.tsx
│   └── EmptyState.tsx
└── ui/
    ├── Button.tsx
    ├── Input.tsx
    ├── Textarea.tsx
    ├── Checkbox.tsx
    ├── LoadingSpinner.tsx
    ├── ErrorMessage.tsx
    └── ConfirmDialog.tsx
```

---

## Accessibility Requirements

### Keyboard Navigation
- ✅ All interactive components focusable
- ✅ Tab order follows visual order
- ✅ Escape key closes modals/dialogs
- ✅ Enter key submits forms

### Screen Reader Support
- ✅ Semantic HTML (button, input, label)
- ✅ ARIA labels for icon-only buttons
- ✅ Form labels associated with inputs (htmlFor)
- ✅ Error announcements (aria-live)

### Color Contrast
- ✅ WCAG AA compliance (4.5:1 minimum)
- ✅ Focus indicators visible (outline ring)

---

## Testing Strategy

### Component Tests (Manual for Phase II)

**Test Cases**:
1. ✅ Button renders with all variants
2. ✅ Input validates email format
3. ✅ Textarea enforces character limit
4. ✅ Checkbox toggles on click
5. ✅ TaskCard displays task data correctly
6. ✅ TaskForm validates required fields
7. ✅ ConfirmDialog closes on cancel
8. ✅ EmptyState displays when no data
9. ✅ ProtectedRoute redirects when unauthenticated

---

## Phase Compliance

### Phase II Allowed ✅
- ✅ Basic UI components (buttons, inputs, forms)
- ✅ Task management components
- ✅ Authentication components
- ✅ Loading and error states

### Phase II Forbidden ❌
- ❌ Real-time collaboration components (Phase III)
- ❌ Chat/messaging components (Phase III)
- ❌ Advanced filtering components (Phase III)
- ❌ Role management components (Phase IV)

**Constitutional Compliance**: ✅ This specification adheres to Article II (Spec-First Doctrine)

---

## References

- Architecture: `specs/architecture.md`
- Pages Specification: `specs/ui/pages.md`
- Tailwind CSS Docs: https://tailwindcss.com/docs
- React Docs: https://react.dev

---

**Status**: ✅ Approved for Implementation  
**Next Step**: Begin implementation with backend (FastAPI) followed by frontend (Next.js)




