"use client";

import React from 'react';
import { formatDistanceToNow } from 'date-fns';
import Checkbox from '@/components/ui/Checkbox';
import Button from '@/components/ui/Button';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number, completed: boolean) => void;
  onEdit: (id: number) => void;
  onDelete: (id: number) => void;
}

export default function TaskCard({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskCardProps) {
  const truncatedDescription = task.description
    ? task.description.length > 100
      ? task.description.substring(0, 100) + "..."
      : task.description
    : null;
  
  const timeAgo = formatDistanceToNow(new Date(task.updated_at), { addSuffix: true });
  
  return (
    <div
      className={`group border rounded-lg p-4 sm:p-6 hover:shadow-lg transition-all ${
        task.completed 
          ? "bg-gray-50 opacity-75 border-gray-200" 
          : "bg-white border-green-200 hover:border-green-300"
      }`}
    >
      <div className="flex flex-col sm:flex-row items-start gap-3 sm:gap-4">
        <div className="flex items-center gap-3 sm:gap-4 w-full sm:w-auto">
          <div className="pt-1">
            <Checkbox
              checked={task.completed}
              onChange={(checked) => onToggleComplete(task.id, checked)}
            />
          </div>
          
          <div className="flex-1 min-w-0 sm:flex-none sm:flex-1">
            <h3
              className={`text-base sm:text-lg font-semibold mb-1 sm:mb-2 ${
                task.completed ? "line-through text-gray-500" : "text-gray-900"
              }`}
            >
              {task.title}
            </h3>
            
            {truncatedDescription && (
              <p className="text-gray-600 text-xs sm:text-sm mb-1 sm:mb-2">{truncatedDescription}</p>
            )}
            
            <p className="text-xs text-gray-400">
              {task.completed ? "Completed" : "Created"} {timeAgo}
            </p>
          </div>
        </div>
        
        <div className="flex gap-2 w-full sm:w-auto sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
          <Button
            variant="secondary"
            onClick={() => onEdit(task.id)}
            className="text-xs sm:text-sm px-3 sm:px-3 py-1.5 sm:py-1 flex-1 sm:flex-initial"
          >
            Edit
          </Button>
          <Button
            variant="danger"
            onClick={() => onDelete(task.id)}
            className="text-xs sm:text-sm px-3 sm:px-3 py-1.5 sm:py-1 flex-1 sm:flex-initial"
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
}

