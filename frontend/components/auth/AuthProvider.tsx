"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { authClient } from "@/lib/auth-client";

interface User {
  id: number;
  email: string;
}

interface AuthContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  
  const refreshUser = async () => {
    const session = await authClient.getSession();
    setUser(session?.user || null);
  };
  
  useEffect(() => {
    refreshUser();
  }, []);
  
  return (
    <AuthContext.Provider value={{ user, setUser, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};

