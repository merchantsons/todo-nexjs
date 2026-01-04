import { authClient } from "./auth-client";

function getApiUrl(): string {
  // First check environment variable (highest priority)
  // This is required for Vercel deployment
  if (process.env.NEXT_PUBLIC_API_URL) {
    return process.env.NEXT_PUBLIC_API_URL;
  }
  
  // In browser, check if we're on localhost (for local development only)
  if (typeof window !== "undefined") {
    const isLocalhost = window.location.hostname === "localhost" || 
                       window.location.hostname === "127.0.0.1" ||
                       window.location.hostname === "";
    if (isLocalhost) {
      return "http://localhost:8000";
    }
    // In production, NEXT_PUBLIC_API_URL should be set
    console.warn("NEXT_PUBLIC_API_URL is not set. Please configure it in Vercel environment variables.");
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
  
  try {
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
  } catch (err: any) {
    // Log the actual error for debugging
    console.error("API request error:", err);
    console.error("API URL attempted:", `${API_URL}${endpoint}`);
    
    if (err.message && (err.message.includes("Failed to fetch") || err.message.includes("NetworkError") || err.name === "TypeError")) {
      throw new Error(`Cannot connect to backend server at ${API_URL}. Please check if the backend is running and accessible.`);
    }
    throw err;
  }
}

