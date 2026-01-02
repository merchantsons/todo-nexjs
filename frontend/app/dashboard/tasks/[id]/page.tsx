"use client";

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import TaskForm from '@/components/tasks/TaskForm';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import ErrorMessage from '@/components/ui/ErrorMessage';
import Button from '@/components/ui/Button';
import { useAuth } from '@/components/auth/AuthProvider';
import { apiRequest } from '@/lib/api-client';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
}

export default function TaskDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const { user } = useAuth();
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  
  useEffect(() => {
    if (!user || !params.id) return;
    
    const fetchTask = async () => {
      try {
        const response = await apiRequest(`/api/${user.id}/tasks/${params.id}`);
        const data = await response.json();
        setTask(data);
      } catch (err: any) {
        setError(err.message || "Task not found");
      } finally {
        setLoading(false);
      }
    };
    
    fetchTask();
  }, [user, params.id]);
  
  const handleUpdate = async (data: { title: string; description: string | null; completed: boolean }) => {
    if (!user || !task) return;
    
    try {
      await apiRequest(`/api/${user.id}/tasks/${task.id}`, {
        method: "PUT",
        body: JSON.stringify(data),
      });
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Unable to update task");
    }
  };
  
  const handleDelete = async () => {
    if (!user || !task) return;
    
    if (!confirm("Are you sure you want to delete this task?")) return;
    
    try {
      await apiRequest(`/api/${user.id}/tasks/${task.id}`, {
        method: "DELETE",
      });
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Unable to delete task");
    }
  };
  
  return (
    <ProtectedRoute>
      <div className="min-h-screen flex flex-col bg-gradient-to-b from-green-50 to-white">
        <Header />
        <main className="flex-1 max-w-3xl mx-auto p-4 sm:p-6 md:p-8 w-full">
          <Button
            variant="secondary"
            onClick={() => router.push("/dashboard")}
            className="mb-4 sm:mb-6 w-full sm:w-auto text-sm sm:text-base"
          >
            ← Back to Dashboard
          </Button>
          
          <h1 className="text-2xl sm:text-3xl font-bold mb-4 sm:mb-6 gradient-green bg-clip-text text-transparent">Task Details</h1>
          
          {loading ? (
            <div className="flex justify-center py-8 sm:py-12">
              <LoadingSpinner size="lg" />
            </div>
          ) : error ? (
            <ErrorMessage message={error} />
          ) : task ? (
            <div className="bg-white rounded-lg p-4 sm:p-6 shadow-lg border border-green-100">
              <TaskForm
                task={task}
                onSubmit={handleUpdate}
                onCancel={() => router.push("/dashboard")}
                submitLabel="Save Changes"
              />
              
              <div className="mt-4 sm:mt-6 pt-4 sm:pt-6 border-t border-green-200">
                <Button variant="danger" onClick={handleDelete} className="w-full sm:w-auto">
                  Delete Task
                </Button>
              </div>
            </div>
          ) : null}
        </main>
        <Footer />
      </div>
    </ProtectedRoute>
  );
}


