## Secure JWT Guard Skill

### Purpose
This skill permanently solves the problem of ensuring every backend endpoint enforces stateless JWT authentication correctly, preventing broken authentication vulnerabilities.

### Problem This Solves
This skill addresses the common hackathon failure of broken authentication by standardizing JWT validation, signature verification, expiry enforcement, and user identity matching, thereby guaranteeing secure access control.

### Inputs
- JWT (JSON Web Token) from the `Authorization` header.
- User ID from the request path or query parameters.
- JWT secret key (accessed securely, not hardcoded).

### Outputs / Guarantees
- Guarantees valid, unexpired, and properly signed JWTs are present for authenticated routes.
- Ensures the user ID embedded in the JWT matches the user ID referenced in the API request, enforcing user isolation.
- Provides a standardized 401 Unauthorized response for all authentication failures.
- Prevents access to protected resources with invalid or missing tokens.

### Behavioral Contract
- **Pre-condition:** A JWT is expected in the `Authorization: Bearer <token>` header for protected routes.
- **Action:** Extracts, decodes, and validates the JWT. Compares the user ID from the token with the user ID from the request.
- **Post-condition:** If valid, allows request to proceed. If invalid, raises a 401 error.

### Constraints
- Will not handle session-based authentication.
- Will not modify business logic beyond authentication enforcement.
- Will not store JWTs; strictly stateless validation.
- Will not generate JWTs.

### Used By
- Backend Agent
- Auth-Security Agent

### Phase Compatibility
- Phase II
- Phase III
- Phase IV
- Phase V

### Failure Modes
- **Invalid Signature:** Returns 401 Unauthorized with a clear message about signature invalidity.
- **Expired Token:** Returns 401 Unauthorized with a message indicating token expiry.
- **Malformed Token:** Returns 401 Unauthorized for tokens that do not conform to JWT structure.
- **User Mismatch:** Returns 401 Unauthorized (or 404 Not Found to prevent enumeration) if the token's user ID does not match the requested resource's user ID.
- **Missing Token:** Returns 401 Unauthorized if the `Authorization` header is missing or malformed.

### Success Signal
- Request successfully proceeds to the next handler with validated `user_id` context.

### Invocation Rule
- Automatically invoked as a dependency for any backend endpoint requiring authentication and authorization via JWT.
