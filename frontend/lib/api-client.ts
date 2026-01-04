import { authClient } from "./auth-client";

function getApiUrl(): string {
  // First check environment variable (highest priority)
  // This is required for Vercel deployment
  let apiUrl = process.env.NEXT_PUBLIC_API_URL;
  
  if (apiUrl) {
    // Remove trailing slash to avoid double slashes in URLs
    apiUrl = apiUrl.trim().replace(/\/+$/, "");
    return apiUrl;
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
    console.error("NEXT_PUBLIC_API_URL is not set. Please configure it in Vercel environment variables.");
    throw new Error("NEXT_PUBLIC_API_URL environment variable is not configured. Please set it in Vercel project settings.");
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
    // Ensure endpoint starts with / to avoid double slashes
    const normalizedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    const fullUrl = `${API_URL}${normalizedEndpoint}`;
    
    const response = await fetch(fullUrl, {
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
    const normalizedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
    console.error("API URL attempted:", `${API_URL}${normalizedEndpoint}`);
    
    if (err.message && (err.message.includes("Failed to fetch") || err.message.includes("NetworkError") || err.name === "TypeError")) {
      const errorMessage = `Cannot connect to backend server at ${API_URL}. Possible causes: 1. Backend server is not running 2. CORS configuration issue 3. Network connectivity problem To fix: - If running locally, start the backend: cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 - Check that the backend is accessible at: ${API_URL}/api/health - Verify CORS settings in backend allow requests from: ${typeof window !== "undefined" ? window.location.origin : "your frontend URL"}`;
      throw new Error(errorMessage);
    }
    throw err;
  }
}

