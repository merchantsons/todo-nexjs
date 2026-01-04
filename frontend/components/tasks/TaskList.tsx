"use client";

import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@/components/auth/AuthProvider';
import { apiRequest } from '@/lib/api-client';
import TaskCard from './TaskCard';
import EmptyState from './EmptyState';
import LoadingSpinner from '@/components/ui/LoadingSpinner';
import ErrorMessage from '@/components/ui/ErrorMessage';
import ConfirmDialog from '@/components/ui/ConfirmDialog';
import Button from '@/components/ui/Button';

interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  onCreateTask: () => void;
}

export default function TaskList({ onCreateTask }: TaskListProps) {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deleteConfirm, setDeleteConfirm] = useState<number | null>(null);
  
  const fetchTasks = useCallback(async () => {
    if (!user) return;
    
    setLoading(true);
    setError("");
    try {
      const response = await apiRequest(`/api/${user.id}/tasks`);
      const data = await response.json();
      
      // Ensure data is an array
      if (Array.isArray(data)) {
        setTasks(data);
      } else if (data && Array.isArray(data.tasks)) {
        // Handle case where API returns { tasks: [...] }
        setTasks(data.tasks);
      } else if (data && typeof data === 'object' && 'detail' in data) {
        // Handle error response from API
        throw new Error(data.detail || "Unable to load tasks");
      } else {
        // Fallback: set empty array if data format is unexpected
        console.warn("Unexpected tasks data format:", data);
        setTasks([]);
      }
    } catch (err: any) {
      console.error("Error fetching tasks:", err);
      setError(err.message || "Unable to load tasks");
      setTasks([]); // Ensure tasks is always an array even on error
    } finally {
      setLoading(false);
    }
  }, [user]);
  
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);
  
  const handleToggleComplete = async (id: number, completed: boolean) => {
    if (!user) return;
    
    try {
      const response = await apiRequest(`/api/${user.id}/tasks/${id}/complete`, {
        method: "PATCH",
        body: JSON.stringify({ completed }),
      });
      await response.json();
      fetchTasks();
    } catch (err: any) {
      setError(err.message || "Unable to update task");
    }
  };
  
  const handleDelete = async (id: number) => {
    if (!user) return;
    
    try {
      await apiRequest(`/api/${user.id}/tasks/${id}`, {
        method: "DELETE",
      });
      fetchTasks();
      setDeleteConfirm(null);
    } catch (err: any) {
      setError(err.message || "Unable to delete task");
    }
  };
  
  const handleEdit = (id: number) => {
    window.location.href = `/dashboard/tasks/${id}`;
  };
  
  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    );
  }
  
  if (error) {
    return (
      <ErrorMessage
        message={error}
        onClose={() => setError("")}
      />
    );
  }
  
  // Ensure tasks is always an array before rendering
  const safeTasks = Array.isArray(tasks) ? tasks : [];

  if (safeTasks.length === 0) {
    return (
      <>
        <div className="mb-6">
          <Button variant="primary" onClick={onCreateTask}>
            + New Task
          </Button>
        </div>
        <EmptyState
          title="No tasks yet"
          message="Create your first task to get started!"
          actionLabel="Create Task"
          onAction={onCreateTask}
        />
      </>
    );
  }

  return (
    <>
      <div className="mb-6">
        <Button variant="primary" onClick={onCreateTask}>
          + New Task
        </Button>
      </div>
      
      <div className="space-y-4">
        {safeTasks.map((task) => (
          <div key={task.id} className="group">
            <TaskCard
              task={task}
              onToggleComplete={handleToggleComplete}
              onEdit={handleEdit}
              onDelete={() => setDeleteConfirm(task.id)}
            />
          </div>
        ))}
      </div>
      
      <ConfirmDialog
        isOpen={deleteConfirm !== null}
        title="Delete Task?"
        message="Are you sure you want to delete this task? This action cannot be undone."
        confirmLabel="Delete"
        cancelLabel="Cancel"
        onConfirm={() => deleteConfirm && handleDelete(deleteConfirm)}
        onCancel={() => setDeleteConfirm(null)}
        variant="danger"
      />
    </>
  );
}




