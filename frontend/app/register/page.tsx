"use client";

import { authClient } from '@/lib/auth-client';
import RegisterForm from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  async function handleRegister(email: string, password: string) {
    await authClient.signUp({ email, password });
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <RegisterForm onSubmit={handleRegister} />
    </div>
  );
}

