"use client";

import React, { useState } from 'react';

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

export default function Textarea({
  label,
  value,
  onChange,
  error,
  required = false,
  placeholder,
  rows = 4,
  maxLength,
  className = "",
}: TextareaProps) {
  const [focused, setFocused] = useState(false);
  
  const hasValue = value.length > 0;
  const showLabel = focused || hasValue;
  
  const textareaId = `textarea-${label.toLowerCase().replace(/\s+/g, '-')}`;
  
  const baseStyles = "w-full px-3 sm:px-4 py-2 text-sm sm:text-base border rounded-lg focus:outline-none focus:ring-2 transition-colors resize-vertical";
  const normalStyles = "border-gray-300 focus:ring-blue-500 focus:border-blue-500";
  const errorStyles = "border-red-500 focus:ring-red-500 focus:border-red-500";
  const textareaStyles = error ? errorStyles : normalStyles;
  
  return (
    <div className={className}>
      <label
        htmlFor={textareaId}
        className={`block mb-2 transition-all duration-200 ${
          showLabel
            ? "text-xs sm:text-sm text-gray-600"
            : "text-sm sm:text-base text-gray-500"
        }`}
      >
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      
      <textarea
        id={textareaId}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        placeholder={placeholder}
        rows={rows}
        maxLength={maxLength}
        required={required}
        className={`${baseStyles} ${textareaStyles}`}
      />
      
      {maxLength && (
        <div className="text-xs text-gray-500 mt-1 text-right">
          {value.length}/{maxLength}
        </div>
      )}
      
      {error && (
        <div className="text-xs sm:text-sm text-red-600 mt-1">{error}</div>
      )}
    </div>
  );
}


