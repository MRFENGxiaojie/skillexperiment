## Examples

<details>
<summary><strong>Example: Login Flow Test Case</strong></summary>

```markdown
## TC-LOGIN-001: Valid User Login

**Priority:** P0 (Critical)
**Type:** Functional

### Objective
Verify that users can successfully log in with valid credentials.

### Preconditions
- User account exists (test@example.com / Test123!)
- User is not already logged in
- Browser cookies cleared

### Test Steps
1. Navigate to https://app.example.com/login
   **Expected:** Login page displays with email and password fields
2. Enter email: test@example.com
   **Expected:** Email field accepts input
3. Enter password: Test123!
   **Expected:** Password field shows masked characters
4. Click "Login"
   **Expected:** Redirected to /dashboard with "Welcome back, Test User" shown

### Post-conditions
- User session created
- Authentication token stored
```
</details>

See also [tc-login-001-valid-user-login.md](tc-login-001-valid-user-login.md) and [tc-ui-045-mobile-navigation-menu.md](tc-ui-045-mobile-navigation-menu.md) for full example test cases.