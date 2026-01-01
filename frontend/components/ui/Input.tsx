"use client";

import React, { useState } from 'react';

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

export default function Input({
  label,
  type = "text",
  value,
  onChange,
  error,
  required = false,
  placeholder,
  disabled = false,
  maxLength,
  className = "",
}: InputProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [focused, setFocused] = useState(false);
  
  const hasValue = value.length > 0;
  const showLabel = focused || hasValue;
  
  const inputId = `input-${label.toLowerCase().replace(/\s+/g, '-')}`;
  
  const baseInputStyles = "w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 transition-colors";
  const normalStyles = "border-gray-300 focus:ring-blue-500 focus:border-blue-500";
  const errorStyles = "border-red-500 focus:ring-red-500 focus:border-red-500";
  const inputStyles = error ? errorStyles : normalStyles;
  
  return (
    <div className={`relative ${className}`}>
      <label
        htmlFor={inputId}
        className={`absolute left-4 transition-all duration-200 pointer-events-none ${
          showLabel
            ? "top-2 text-xs text-gray-600"
            : "top-3 text-base text-gray-500"
        }`}
      >
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      
      <div className="relative">
        <input
          id={inputId}
          type={type === "password" && showPassword ? "text" : type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder={placeholder}
          disabled={disabled}
          maxLength={maxLength}
          required={required}
          className={`${baseInputStyles} ${inputStyles} ${hasValue || focused ? "pt-6 pb-2" : "pt-3 pb-2"} ${disabled ? "bg-gray-100 cursor-not-allowed" : ""}`}
        />
        
        {type === "password" && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
          >
            {showPassword ? "👁️" : "👁️‍🗨️"}
          </button>
        )}
      </div>
      
      {maxLength && (
        <div className="text-xs text-gray-500 mt-1 text-right">
          {value.length}/{maxLength}
        </div>
      )}
      
      {error && (
        <div className="text-sm text-red-600 mt-1">{error}</div>
      )}
    </div>
  );
}

