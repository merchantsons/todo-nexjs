"use client";

import { authClient } from '@/lib/auth-client';
import LoginForm from '@/components/auth/LoginForm';

export default function LoginPage() {
  async function handleLogin(email: string, password: string) {
    await authClient.signIn({ email, password });
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <LoginForm onSubmit={handleLogin} />
    </div>
  );
}

