"use client";

import ProtectedRoute from '@/components/auth/ProtectedRoute';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
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
      <div className="min-h-screen flex flex-col bg-gradient-to-b from-green-50 to-white">
        <Header />
        <main className="flex-1 max-w-7xl mx-auto p-4 sm:p-6 md:p-8 w-full">
          <h1 className="text-2xl sm:text-3xl font-bold mb-4 sm:mb-6 gradient-green bg-clip-text text-transparent">My Tasks</h1>
          
          {showForm ? (
            <div className="bg-white rounded-lg p-4 sm:p-6 shadow-lg border border-green-100">
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
        <Footer />
      </div>
    </ProtectedRoute>
  );
}


