## User-Scoped Query Enforcement Skill

### Purpose
This skill guarantees zero possibility of cross-user data leakage by automatically applying user-scoped filtering to all data access queries.

### Problem This Solves
This skill encodes security as intelligence, not discipline, by systematically preventing unauthorized access to or modification of data belonging to other users. It solves the problem of developers accidentally exposing or allowing access to other users' data.

### Inputs
- The authenticated `user_id` obtained from the Secure JWT Guard Skill.
- Database queries or ORM operations requiring data filtering.
- Data models (e.g., SQLModel models) that include a `user_id` field for ownership.

### Outputs / Guarantees
- Guarantees that all data retrieval, update, and deletion operations are implicitly filtered by the authenticated `user_id`.
- Ensures that a user can only interact with their own data.
- Converts attempts to access or manipulate data owned by another user into a 404 Not Found response, preventing user enumeration and data leakage.

### Behavioral Contract
- **Pre-condition:** An authenticated `user_id` is available in the request context (e.g., from JWT validation).
- **Action:** Intercepts data access queries/operations and injects a `WHERE user_id = :authenticated_user_id` clause (or equivalent ORM filtering).
- **Post-condition:** Only data owned by the authenticated user is returned or affected. If the requested resource does not belong to the user, a 404 Not Found error is raised.

### Constraints
- Will not apply to global, non-user-specific data (e.g., public configuration, shared resources if explicitly allowed).
- Assumes data models include a `user_id` or similar ownership identifier.
- Will not bypass existing database-level access controls; it enhances them.

### Used By
- Backend Agent
- Auth-Security Agent

### Phase Compatibility
- Phase II
- Phase III
- Phase IV
- Phase V

### Failure Modes
- **No Ownership Field:** Fails explicitly if a data model intended for user-scoped access does not have a `user_id` field, prompting for spec clarification.
- **Unauthorized Access Attempt:** Returns 404 Not Found (to obscure existence of resource from unauthorized user) when a query attempts to access a resource not owned by the authenticated user.
- **Missing `user_id` Context:** Raises an internal server error if the authenticated `user_id` is not present in the request context when required.

### Success Signal
- Data operations (fetch, update, delete) complete successfully, affecting only the authenticated user's data.

### Invocation Rule
- Automatically applied as a query interceptor or ORM mixin for all backend data access layers involving user-owned data.
