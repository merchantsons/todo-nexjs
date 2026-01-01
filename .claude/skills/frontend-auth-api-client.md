## Frontend Auth-Aware API Client Skill

### Purpose
This skill centralizes and standardizes all frontend API access, automatically handling JWT attachment, authentication failures, and error normalization, leading to clean architecture and fewer bugs.

### Problem This Solves
This skill eliminates duplicated authentication logic across the frontend, prevents common errors related to token handling, and ensures consistent user experience during authentication failures. It solves the problem of scattered API call logic and inconsistent error handling.

### Inputs
- API endpoint URL.
- Request body/parameters.
- JWT stored in a secure client-side mechanism (e.g., HttpOnly cookie, localStorage).

### Outputs / Guarantees
- Guarantees that all outgoing API requests from the frontend automatically include the necessary JWT for authentication.
- Ensures consistent handling of 401 Unauthorized responses, typically by redirecting the user to the login page.
- Normalizes API error responses into a consistent format for easier UI consumption.
- Enforces a single, centralized entry point for all API interactions from the frontend.

### Behavioral Contract
- **Pre-condition:** User may or may not have a valid JWT available client-side.
- **Action:** Intercepts outgoing API requests, attaches JWT if available. Intercepts incoming API responses, specifically handling 401 errors.
- **Post-condition:** Successful API responses are passed to the caller. 401 errors trigger a logout/redirect flow. Other errors are normalized and passed.

### Constraints
- Will not handle business logic; solely focuses on API communication and authentication.
- Will not manage the JWT lifecycle (e.g., refresh tokens); assumes the token is provided or missing.
- Will not perform UI rendering; only triggers state changes (e.g., redirect).
- Will not invent API contracts; adheres strictly to backend specifications.

### Used By
- Frontend Agent

### Phase Compatibility
- Phase II
- Phase III
- Phase IV
- Phase V

### Failure Modes
- **Network Errors:** Gracefully handles network connectivity issues, returning a standardized network error object.
- **401 Unauthorized:** Automatically redirects to the `/login` page and clears any stored tokens.
- **API Contract Mismatch:** Logs a warning if API response deviates from expected spec but still attempts to process the response (fail-safe).
- **Invalid URL/Endpoint:** Returns a standardized error for inaccessible or malformed API endpoints.

### Success Signal
- Frontend components receive consistent, clean data from API calls, or a normalized error object, without needing to implement auth-specific logic.

### Invocation Rule
- All frontend components or services requiring backend data access must use this centralized API client skill (e.g., via a custom `useApi` hook or `apiService` module).
