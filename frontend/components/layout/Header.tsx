"use client";

import React from 'react';
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
    <header className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">Evolution of Todo</h1>
          </div>
          
          {user && (
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">Hi, {user.email}</span>
              <Button variant="secondary" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}

