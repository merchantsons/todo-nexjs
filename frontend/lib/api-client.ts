import { authClient } from "./auth-client";

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const session = await authClient.getSession();
  
  if (!session?.accessToken) {
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Unauthenticated");
  }
  
  const API_URL = 
    process.env.NEXT_PUBLIC_API_URL || 
    (typeof window !== "undefined" && window.location.hostname !== "localhost" 
      ? "https://backend-nine-sigma-81.vercel.app" 
      : "http://localhost:8000");
  
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${session.accessToken}`,
      "Content-Type": "application/json",
    },
  });
  
  if (response.status === 401) {
    await authClient.signOut();
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Unauthorized");
  }
  
  return response;
}

