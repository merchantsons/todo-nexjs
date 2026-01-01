"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import ErrorMessage from '@/components/ui/ErrorMessage';

interface RegisterFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  error?: string;
}

export default function RegisterForm({ onSubmit, error }: RegisterFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [formError, setFormError] = useState("");
  const [passwordErrors, setPasswordErrors] = useState<string[]>([]);
  const router = useRouter();
  
  const validatePassword = (pwd: string): string[] => {
    const errors: string[] = [];
    if (pwd.length < 8) errors.push("Password must be at least 8 characters");
    if (!/[A-Z]/.test(pwd)) errors.push("Password must contain at least one uppercase letter");
    if (!/[a-z]/.test(pwd)) errors.push("Password must contain at least one lowercase letter");
    if (!/[0-9]/.test(pwd)) errors.push("Password must contain at least one number");
    return errors;
  };
  
  const handlePasswordChange = (value: string) => {
    setPassword(value);
    setPasswordErrors(validatePassword(value));
  };
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError("");
    
    const errors = validatePassword(password);
    if (errors.length > 0) {
      setPasswordErrors(errors);
      return;
    }
    
    setLoading(true);
    try {
      await onSubmit(email, password);
      // Small delay to ensure session is stored
      await new Promise(resolve => setTimeout(resolve, 100));
      router.push("/dashboard");
      router.refresh();
    } catch (err: any) {
      setFormError(err.message || "Unable to create account");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="w-full max-w-md mx-auto p-8 bg-white rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold text-center mb-6">Create your account</h1>
      
      {(error || formError) && (
        <ErrorMessage
          message={error || formError}
          onClose={() => setFormError("")}
          className="mb-4"
        />
      )}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Email"
          type="email"
          value={email}
          onChange={setEmail}
          required
          placeholder="you@example.com"
        />
        
        <div>
          <Input
            label="Password"
            type="password"
            value={password}
            onChange={handlePasswordChange}
            required
          />
          {passwordErrors.length > 0 && (
            <div className="mt-2 text-sm text-red-600">
              <ul className="list-disc list-inside">
                {passwordErrors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
        
        <Button
          type="submit"
          variant="primary"
          fullWidth
          disabled={loading || passwordErrors.length > 0}
        >
          {loading ? "Creating account..." : "Register"}
        </Button>
      </form>
      
      <p className="mt-4 text-center text-sm text-gray-600">
        Already have an account?{" "}
        <a href="/login" className="text-blue-600 hover:underline">
          Log in →
        </a>
      </p>
    </div>
  );
}

