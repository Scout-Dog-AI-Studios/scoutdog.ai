# Frontend Development Rules & Guidelines (Next.js + Tailwind)

These rules ensure consistency and maintainability in the frontend application (`apps/frontend`).

## 1. Framework & Structure

- **Framework:** Utilize **Next.js 14+ App Router** for routing, rendering, and API routes (if frontend-specific).
- **Language:** Use **TypeScript** for all new code. Leverage strict mode and aim for strong type safety.
- **Directory Structure:**
  - Follow Next.js App Router conventions (`app/`, `layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`).
  - Place reusable components under `components/`. Consider sub-directories for organization (e.g., `components/ui/`, `components/auth/`).
  - Place utility functions under `lib/` or `utils/`.
  - Store static assets in the `public/` directory.

## 2. Styling

- **Primary Styling:** Use **Tailwind CSS (v4)** utility classes exclusively for styling.
- **Avoid Custom CSS:** Minimize or eliminate the use of global CSS files or CSS Modules unless absolutely necessary for complex scenarios not easily handled by Tailwind.
- **Configuration:** Configure Tailwind theme extensions (`colors`, `fontFamily`, etc.) in `tailwind.config.js`.
- **Component Logic:** Keep component logic focused on structure, state, and props. Styling should primarily be done via `className`.

## 3. Components

- **Reusability:** Design components to be reusable and composable.
- **Props:** Define component props clearly using TypeScript interfaces or types.
- **Client vs. Server:** Be mindful of React Server Components (RSC) vs. Client Components (`'use client'`). Use Client Components only when necessary (hooks, event listeners, browser APIs).

## 4. State Management

- **Local State:** Use React hooks (`useState`, `useReducer`) for component-level state.
- **Global State:** For simple global state, use React Context. If state becomes complex across many components, consider a lightweight library like Zustand. Avoid Redux unless the complexity truly warrants it.
- **Server State:** Use React Query (`@tanstack/react-query`) or SWR for managing server state (fetching, caching, synchronizing data from the backend API).

## 5. API Interaction

- **Fetching:** Use the native `fetch` API or a wrapper library configured within the server state management tool (React Query/SWR).
- **Backend URL:** Use environment variables (`NEXT_PUBLIC_API_URL`) to configure the backend API base URL.
- **Error Handling:** Implement proper loading and error states for API calls within components.

## 6. Authentication

- **Library:** Use the official Auth0 React SDK (`@auth0/auth0-react`).
- **Implementation:** Follow SDK patterns for login/logout flow, accessing user profile, getting access tokens, and protecting routes/components.

## 7. Environment Variables

- **Exposure:** Prefix variables needed in the browser with `NEXT_PUBLIC_`.
- **Files:** Use `.env.local` for local overrides (add to `.gitignore`). Use `.env.development` and `.env.production` for environment-specific defaults if needed.
- **Schema:** Document all required environment variables in `.env.example`.

## 8. Linting & Formatting

- **Tools:** Use ESLint and Prettier, configured at the monorepo root.
- **Enforcement:** Run linting and formatting checks before committing code (ideally via pre-commit hooks) and in CI.

## 9. Testing

- **Priority:** While rapid prototyping may limit extensive testing, aim for basic component tests (using Jest/React Testing Library) for critical UI elements and utility function unit tests.
- **Integration:** Consider end-to-end tests (using Playwright or Cypress) for critical user flows (like authentication) once features stabilize.
