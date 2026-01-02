// Custom auth client that works with our FastAPI backend
const API_URL = 
  process.env.NEXT_PUBLIC_API_URL || 
  (typeof window !== "undefined" && window.location.hostname !== "localhost" 
    ? "https://backend-nine-sigma-81.vercel.app" 
    : "http://localhost:8000");

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
      if (err.message && err.message.includes("Failed to fetch")) {
        throw new Error("Cannot connect to server. Make sure the backend is running on http://localhost:8000");
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
      if (err.message && err.message.includes("Failed to fetch")) {
        throw new Error("Cannot connect to server. Make sure the backend is running on http://localhost:8000");
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

