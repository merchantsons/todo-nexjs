"use client";

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';
import { useAuth } from '@/components/auth/AuthProvider';
import Button from '@/components/ui/Button';

export default function Header() {
  const { user } = useAuth();
  const router = useRouter();
  
  const handleLogout = async () => {
    await authClient.signOut();
    router.push("/login");
    router.refresh();
  };
  
  return (
    <header className="bg-white border-b border-green-200 shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-center gap-3 sm:gap-0 py-3 sm:py-0 h-auto sm:h-20">
          <div className="flex items-center w-full sm:w-auto justify-center sm:justify-start">
            <Link href="/" className="flex items-center gap-2 sm:gap-3">
              <span className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl">📚</span>
              <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold cursor-pointer" style={{ color: '#0d2818', fontFamily: 'var(--font-lavishly-yours), cursive' }}>Evolution of Todo</h1>
            </Link>
          </div>
          
          {user && (
            <div className="flex flex-col sm:flex-row items-center gap-2 sm:gap-4 w-full sm:w-auto">
              <span className="text-xs sm:text-sm text-gray-700 text-center sm:text-left truncate max-w-[200px] sm:max-w-none">{user.email}</span>
              <Button variant="secondary" onClick={handleLogout} className="w-full sm:w-auto text-sm sm:text-base px-4 sm:px-6 py-2 sm:py-3">
                Logout
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

