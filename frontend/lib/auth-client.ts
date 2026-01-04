// Custom auth client that works with our FastAPI backend
function getApiUrl(): string {
  // First check environment variable (highest priority)
  // This is required for Vercel deployment
  if (process.env.NEXT_PUBLIC_API_URL) {
    const url = process.env.NEXT_PUBLIC_API_URL;
    console.log("Using API URL from env:", url);
    return url;
  }
  
  // In browser, check if we're on localhost (for local development only)
  if (typeof window !== "undefined") {
    const isLocalhost = window.location.hostname === "localhost" || 
                       window.location.hostname === "127.0.0.1" ||
                       window.location.hostname === "";
    if (isLocalhost) {
      const url = "http://localhost:8000";
      console.log("Using API URL (localhost):", url);
      return url;
    }
    // In production, NEXT_PUBLIC_API_URL should be set
    console.warn("NEXT_PUBLIC_API_URL is not set. Please configure it in Vercel environment variables.");
  }
  
  // Server-side default (shouldn't happen in auth client, but fallback)
  const url = "http://localhost:8000";
  console.log("Using API URL (fallback):", url);
  return url;
}

interface User {
  id: number;
  email: string;
}

interface Session {
  user: User;
  accessToken: string;
}

// Simple session storage
let currentSession: Session | null = null;

export const authClient = {
  async signUp(email: { email: string; password: string }) {
    const API_URL = getApiUrl();
    let response: Response;
    try {
      console.log("Attempting registration to:", `${API_URL}/api/auth/register`);
      
      response = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.email, password: email.password }),
        credentials: "omit",
      });

      console.log("Registration response status:", response.status);
      console.log("Registration response headers:", Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        // Try to get response text first to see what we're dealing with
        const responseText = await response.text();
        console.error("Registration error response text:", responseText);
        
        let error: any;
        try {
          error = responseText ? JSON.parse(responseText) : {};
        } catch (e) {
          error = { detail: responseText || `Registration failed with status ${response.status}` };
        }
        
        console.error("Registration error response:", error);
        throw new Error(error.detail || error.message || `Registration failed with status ${response.status}`);
      }
    } catch (err: any) {
      // Log the actual error for debugging
      console.error("Backend connection error (signUp):", err);
      console.error("Error type:", err.constructor.name);
      console.error("Error message:", err.message);
      console.error("Error name:", err.name);
      console.error("API URL attempted:", API_URL);
      
      // Handle network errors with better messaging
      if (err.message && (err.message.includes("Failed to fetch") || err.message.includes("NetworkError") || err.name === "TypeError")) {
        const errorMessage = 
          `Cannot connect to backend server at ${API_URL}.\n\n` +
          `Possible causes:\n` +
          `1. Backend server is not running\n` +
          `2. CORS configuration issue\n` +
          `3. Network connectivity problem\n\n` +
          `To fix:\n` +
          `- If running locally, start the backend: cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000\n` +
          `- Check that the backend is accessible at: ${API_URL}/api/health\n` +
          `- Verify CORS settings in backend allow requests from: ${typeof window !== "undefined" ? window.location.origin : "your frontend URL"}`;
        
        throw new Error(errorMessage);
      }
      throw err;
    }

    const data = await response.json();
    currentSession = {
      user: data.user,
      accessToken: data.accessToken,
    };
    
    // Store in localStorage
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_session", JSON.stringify(currentSession));
    }
    
    return currentSession;
  },

  async signIn(email: { email: string; password: string }) {
    const API_URL = getApiUrl();
    let response: Response;
    try {
      console.log("Attempting login to:", `${API_URL}/api/auth/login`);
      
      response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email.email, password: email.password }),
        // Add credentials for CORS
        credentials: "omit",
      });

      console.log("Login response status:", response.status);

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Login failed" }));
        console.error("Login error response:", error);
        throw new Error(error.detail || "Login failed");
      }
    } catch (err: any) {
      // Log the actual error for debugging
      console.error("Backend connection error (signIn):", err);
      console.error("Error type:", err.constructor.name);
      console.error("Error message:", err.message);
      console.error("Error name:", err.name);
      console.error("API URL attempted:", API_URL);
      
      // Handle network errors with better messaging
      if (err.message && (err.message.includes("Failed to fetch") || err.message.includes("NetworkError") || err.name === "TypeError")) {
        const errorMessage = 
          `Cannot connect to backend server at ${API_URL}.\n\n` +
          `Possible causes:\n` +
          `1. Backend server is not running\n` +
          `2. CORS configuration issue\n` +
          `3. Network connectivity problem\n\n` +
          `To fix:\n` +
          `- If running locally, start the backend: cd backend && python -m uvicorn app.main:app --reload --port 8000\n` +
          `- Check that the backend is accessible at: ${API_URL}/api/health\n` +
          `- Verify CORS settings in backend allow requests from: ${typeof window !== "undefined" ? window.location.origin : "your frontend URL"}`;
        
        throw new Error(errorMessage);
      }
      throw err;
    }

    const data = await response.json();
    currentSession = {
      user: data.user,
      accessToken: data.accessToken,
    };
    
    // Store in localStorage
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_session", JSON.stringify(currentSession));
    }
    
    return currentSession;
  },

  async signOut() {
    currentSession = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_session");
    }
  },

  async getSession(): Promise<Session | null> {
    // Try to get from memory first
    if (currentSession) {
      return currentSession;
    }
    
    // Try to get from localStorage
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("auth_session");
      if (stored) {
        try {
          currentSession = JSON.parse(stored);
          return currentSession;
        } catch (e) {
          localStorage.removeItem("auth_session");
        }
      }
    }
    
    return null;
  },
};

