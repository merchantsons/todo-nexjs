"use client";

import React, { useState, useEffect } from 'react';
import Input from '@/components/ui/Input';
import Textarea from '@/components/ui/Textarea';
import Checkbox from '@/components/ui/Checkbox';
import Button from '@/components/ui/Button';
import ErrorMessage from '@/components/ui/ErrorMessage';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
}

interface TaskFormProps {
  task?: Task;
  onSubmit: (data: { title: string; description: string | null; completed: boolean }) => Promise<void>;
  onCancel: () => void;
  submitLabel?: string;
}

export default function TaskForm({
  task,
  onSubmit,
  onCancel,
  submitLabel = "Save Changes",
}: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [completed, setCompleted] = useState(task?.completed || false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || "");
      setCompleted(task.completed);
    }
  }, [task]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    
    if (!title.trim()) {
      setError("Title is required");
      return;
    }
    
    setLoading(true);
    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || null,
        completed,
      });
    } catch (err: any) {
      setError(err.message || "Unable to save task");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <ErrorMessage message={error} onClose={() => setError("")} />
      )}
      
      <Input
        label="Title"
        value={title}
        onChange={setTitle}
        required
        maxLength={255}
        placeholder="Enter task title"
      />
      
      <Textarea
        label="Description"
        value={description}
        onChange={setDescription}
        rows={4}
        maxLength={10000}
        placeholder="Enter task description (optional)"
      />
      
      {task && (
        <Checkbox
          label="Mark as complete"
          checked={completed}
          onChange={setCompleted}
        />
      )}
      
      <div className="flex flex-col sm:flex-row gap-3">
        <Button type="submit" variant="primary" disabled={loading} className="w-full sm:w-auto">
          {loading ? "Saving..." : submitLabel}
        </Button>
        <Button type="button" variant="secondary" onClick={onCancel} className="w-full sm:w-auto">
          Cancel
        </Button>
      </div>
    </form>
  );
}


