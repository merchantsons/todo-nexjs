// Custom auth client that works with our FastAPI backend
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
  
  // Server-side default (shouldn't happen in auth client, but fallback)
  return "http://localhost:8000";
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
      response = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.email, password: email.password }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Registration failed" }));
        throw new Error(error.detail || "Registration failed");
      }
    } catch (err: any) {
      if (err.message && (err.message.includes("Failed to fetch") || err.message.includes("NetworkError") || err.name === "TypeError")) {
        throw new Error(`Cannot connect to backend server at ${API_URL}. Please check if the backend is running and accessible.`);
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
      response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.email, password: email.password }),
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: "Login failed" }));
        throw new Error(error.detail || "Login failed");
      }
    } catch (err: any) {
      if (err.message && (err.message.includes("Failed to fetch") || err.message.includes("NetworkError") || err.name === "TypeError")) {
        throw new Error(`Cannot connect to backend server at ${API_URL}. Please check if the backend is running and accessible.`);
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

