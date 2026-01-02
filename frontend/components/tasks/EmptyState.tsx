import React from 'react';
import Button from '@/components/ui/Button';

interface EmptyStateProps {
  title: string;
  message: string;
  actionLabel?: string;
  onAction?: () => void;
}

export default function EmptyState({
  title,
  message,
  actionLabel,
  onAction,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-8 sm:py-12 px-4">
      <div className="text-4xl sm:text-5xl md:text-6xl mb-3 sm:mb-4">📋</div>
      <h2 className="text-xl sm:text-2xl font-bold text-gray-900 mb-2 text-center">{title}</h2>
      <p className="text-sm sm:text-base text-gray-600 mb-4 sm:mb-6 text-center max-w-md px-4">{message}</p>
      {actionLabel && onAction && (
        <Button variant="primary" onClick={onAction} className="w-full sm:w-auto">
          {actionLabel}
        </Button>
      )}
    </div>
  );
}


