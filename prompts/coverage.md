# Missing Test Cases & Coverage Issues

This document lists missing or recommended test cases for the codebase, formatted as actionable GitHub issues. Each issue is specific to a function, module, or user flow, and is intended to guide developers toward comprehensive test coverage.

---

## :rotating_light: [Backend] FastAPI & Services

### 1. **Test: Health Check Endpoint**

**File:** `apps/backend/app/main.py`

- [x] **Should return 200 and correct message for `/` root endpoint.**

---

### 2. **Test: Greeting API**

**Files:** `apps/backend/app/api/v1/endpoints/greet.py`, `apps/backend/app/services/greeting.py`

- [x] **Should return a greeting message when DB returns a row.**
- [x] **Should return fallback message when DB returns no rows.**
- [x] **Should handle DB exceptions and return appropriate error/log.**
- [x] **Should require valid Auth0 JWT (unauthorized without or with invalid token).**

---

### 3. **Test: Upload API**

**Files:** `apps/backend/app/api/v1/endpoints/upload.py`, `apps/backend/app/services/storage.py`

- [x] **Should upload a valid file and return a public URL.**
- [x] **Should reject files with disallowed content types.**
- [x] **Should handle upload errors (e.g., storage unavailable, boto3 error).**
- [x] **Should require valid Auth0 JWT (unauthorized without or with invalid token).**
- [x] **Should handle missing/empty file in request.**
- [x] **Should reject files over a maximum size (if limit is set).**

---

### 4. **Test: Auth/JWT Validation**

**File:** `apps/backend/app/auth/jwt.py`

- [x] **Should validate a correct JWT and return payload.**
- [x] **Should reject expired JWT (ExpiredSignatureError).**
- [x] **Should reject JWT with invalid claims (JWTClaimsError).**
- [x] **Should reject JWT with bad signature or malformed token.**
- [x] **Should handle JWKS fetch failure gracefully.**

---

### 5. **Test: R2 Client Initialization**

**File:** `apps/backend/app/clients/r2.py`

- [x] **Should initialize R2 client with correct config.**
- [x] **Should raise HTTPException on bad/missing config.**
- [x] **Should return the same client instance (singleton pattern).**

---

### 6. **Test: AstraDB Connection**

**File:** `apps/backend/app/db/session.py`

- [x] **Should connect to AstraDB with valid config and log version.**
- [x] **Should raise FileNotFoundError if secure bundle is missing.**
- [x] **Should raise RuntimeError if connection fails.**
- [x] **Should close connection cleanly.**

---

## :sparkles: [Frontend] Next.js Dashboard & File Upload

### 7. **Test: Dashboard Page**

**File:** `apps/frontend/src/app/dashboard/page.tsx`

- [x] **Should fetch and display greeting from backend on load.**
- [x] **Should display error message if greeting fetch fails.**
- [x] **Should show loading indicator while fetching greeting.**
- [x] **Should render user info (name/email) when logged in.**

---

### 8. **Test: File Upload Section**

**File:** `apps/frontend/src/app/dashboard/page.tsx`

- [x] **Should allow user to select file and enable upload button.**
- [x] **Should POST file to backend and display returned URL.**
- [x] **Should display error if upload fails (e.g., network, backend error).**
- [x] **Should show uploading indicator while upload is in progress.**
- [x] **Should clear error and uploaded file state on new file selection.**
- [x] **Should reject upload if no file is selected.**
- [x] **Should handle backend validation errors (e.g., disallowed file type).**

---

## :triangular_flag_on_post: [General/Integration]

- [x] **Should require authentication for all protected endpoints and pages.**
- [ ] **Should handle and log unexpected errors gracefully (Sentry integration, if enabled).**
- [x] **Should pass all type/lint checks as part of CI.**

---

# :pushpin: How to Use

- Use this checklist to guide the creation of unit, integration, and end-to-end tests.
- Link each test case to the relevant file and function/component.
- Mark each as completed when implemented and passing.
