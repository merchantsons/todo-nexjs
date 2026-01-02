"use client";

import Link from 'next/link';
import { authClient } from '@/lib/auth-client';
import LoginForm from '@/components/auth/LoginForm';
import Footer from '@/components/layout/Footer';

export default function LoginPage() {
  async function handleLogin(email: string, password: string) {
    await authClient.signIn({ email, password });
  }
  
  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-green-50 to-white">
      <header className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 w-full">
        <Link href="/" className="flex items-center gap-2 sm:gap-3 justify-center sm:justify-start">
          <span className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl">📚</span>
          <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold cursor-pointer" style={{ color: '#0d2818', fontFamily: 'var(--font-poppins)' }}>Evolution of Todo</h1>
        </Link>
      </header>
      <div className="flex-1 flex items-center justify-center px-4 py-4">
        <LoginForm onSubmit={handleLogin} />
      </div>
      <Footer />
    </div>
  );
}

