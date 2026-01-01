"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";
import { useAuth } from "@/components/auth/AuthProvider";
import LoadingSpinner from "@/components/ui/LoadingSpinner";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { refreshUser } = useAuth();
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const checkAuth = async () => {
      const session = await authClient.getSession();
      if (!session) {
        router.push("/login");
      } else {
        await refreshUser();
        setLoading(false);
      }
    };
    checkAuth();
  }, [router, refreshUser]);
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }
  
  return <>{children}</>;
}

