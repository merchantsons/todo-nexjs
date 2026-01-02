import React from 'react';

interface ErrorMessageProps {
  message: string;
  onClose?: () => void;
  className?: string;
}

export default function ErrorMessage({
  message,
  onClose,
  className = "",
}: ErrorMessageProps) {
  return (
    <div
      className={`bg-red-50 border border-red-200 text-red-800 px-3 sm:px-4 py-2 sm:py-3 rounded-lg flex items-center gap-2 text-sm sm:text-base ${className}`}
      role="alert"
    >
      <span className="text-red-600 text-base sm:text-lg">⚠️</span>
      <span className="flex-1 break-words">{message}</span>
      {onClose && (
        <button
          onClick={onClose}
          className="text-red-600 hover:text-red-800 focus:outline-none cursor-pointer"
          aria-label="Close error message"
        >
          ✕
        </button>
      )}
    </div>
  );
}


