import { authClient } from "./auth-client";

function getApiUrl(): string {
  // First check environment variable (highest priority)
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  
  // In browser, check if we're on localhost
  if (typeof window !== "undefined") {
    const isLocalhost = window.location.hostname === "localhost" || 
                       window.location.hostname === "127.0.0.1" ||
                       window.location.hostname === "";
    return isLocalhost 
      ? "http://localhost:8000" 
      : "https://backend-nine-sigma-81.vercel.app";
  }
  
  // Server-side default (shouldn't happen in api client, but fallback)
  return "http://localhost:8000";
}

export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const session = await authClient.getSession();
  
  if (!session?.accessToken) {
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new Error("Unauthenticated");
  }
  
  const API_URL = getApiUrl();
  
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

