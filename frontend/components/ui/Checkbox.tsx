import React from 'react';

interface CheckboxProps {
  label?: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
  className?: string;
}

export default function Checkbox({
  label,
  checked,
  onChange,
  disabled = false,
  className = "",
}: CheckboxProps) {
  const checkboxId = `checkbox-${label?.toLowerCase().replace(/\s+/g, '-') || 'default'}`;
  
  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <input
        id={checkboxId}
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        disabled={disabled}
        className="w-5 h-5 border-2 border-gray-400 rounded focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
      />
      {label && (
        <label
          htmlFor={checkboxId}
          className="text-base text-gray-700 cursor-pointer select-none"
        >
          {label}
        </label>
      )}
    </div>
  );
}




