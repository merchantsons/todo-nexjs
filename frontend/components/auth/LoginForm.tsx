"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';
import Input from '@/components/ui/Input';
import Button from '@/components/ui/Button';
import ErrorMessage from '@/components/ui/ErrorMessage';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
  error?: string;
}

export default function LoginForm({ onSubmit, error }: LoginFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [formError, setFormError] = useState("");
  const router = useRouter();
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError("");
    setLoading(true);
    
    try {
      await onSubmit(email, password);
      // Small delay to ensure session is stored
      await new Promise(resolve => setTimeout(resolve, 100));
      router.push("/dashboard");
      router.refresh();
    } catch (err: any) {
      setFormError(err.message || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="w-full max-w-md mx-auto p-4 sm:p-6 md:p-8 bg-white rounded-lg shadow-lg border border-green-100">
      <h1 className="text-xl sm:text-2xl font-bold text-center mb-4 sm:mb-6 gradient-green bg-clip-text text-white">Log in to your account</h1>
      
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
        
        <Input
          label="Password"
          type="password"
          value={password}
          onChange={setPassword}
          required
        />
        
        <Button
          type="submit"
          variant="primary"
          fullWidth
          disabled={loading}
        >
          {loading ? "Logging in..." : "Login"}
        </Button>
      </form>
      
      <p className="mt-4 text-center text-xs sm:text-sm text-gray-600 px-2">
        Don't have an account?{" "}
        <a href="/register" className="text-green-700 hover:text-green-800 font-medium transition-colors">
          Sign up →
        </a>
      </p>
    </div>
  );
}

