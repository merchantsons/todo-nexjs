"use client";

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import Header from '@/components/layout/Header';
import TaskList from '@/components/tasks/TaskList';
import TaskForm from '@/components/tasks/TaskForm';
import { useAuth } from '@/components/auth/AuthProvider';
import { apiRequest } from '@/lib/api-client';
import { useState } from 'react';

export default function DashboardPage() {
  const { user } = useAuth();
  const [showForm, setShowForm] = useState(false);
  
  const handleCreateTask = async (data: { title: string; description: string | null; completed: boolean }) => {
    if (!user) return;
    
    await apiRequest(`/api/${user.id}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
    
    setShowForm(false);
    window.location.reload();
  };
  
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Header />
        <main className="max-w-7xl mx-auto p-8">
          <h1 className="text-3xl font-bold mb-6">My Tasks</h1>
          
          {showForm ? (
            <div className="bg-white rounded-lg p-6 shadow">
              <TaskForm
                onSubmit={handleCreateTask}
                onCancel={() => setShowForm(false)}
                submitLabel="Create Task"
              />
            </div>
          ) : (
            <TaskList onCreateTask={() => setShowForm(true)} />
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}

