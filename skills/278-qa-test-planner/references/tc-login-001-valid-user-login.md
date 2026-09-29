## TC-LOGIN-001: Valid User Login

**Priority:** P0 (Critical)
**Type:** Functional
**Estimated Time:** 2 minutes

### Objective
Verify that users can successfully log in with valid credentials

### Pre-conditions
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

4. Click "Login" button
   **Expected:**
   - Loading indicator appears
   - User redirected to /dashboard
   - Welcome message displayed: "Welcome back, Test User"
   - Avatar/profile image displayed in header

### Post-conditions
- User session created
- Authentication token stored
- Analytics event logged

### Edge Cases to Consider
- TC-LOGIN-002: Invalid password
- TC-LOGIN-003: Non-existent email
- TC-LOGIN-004: SQL injection attempt
- TC-LOGIN-005: Very long password