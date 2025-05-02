Okay, let's outline the blueprint for transforming your gold master frontend (`apps/frontend`) into the `scoutdog.ai` homepage using the `mockup/` design, and then break it down into actionable, incremental prompts.

## High-Level Blueprint: Monorepo Transformation

1.  **Phase 1: Foundation (Completed)**
    *   Existing gold master monorepo setup (pnpm, Turbo, Next.js, FastAPI, Poetry, Docker, Taskfile, basic auth, API interaction, tests).

2.  **Phase 2: Frontend Preparation & Dependency Integration**
    *   **Goal:** Prepare `apps/frontend` to use the Shadcn UI system and styles from the mockup.
    *   Install necessary UI and utility dependencies.
    *   Copy Shadcn UI components, utils, hooks, and config from the mockup.
    *   Merge Tailwind CSS configurations.
    *   Merge global CSS styles.

3.  **Phase 3: Core Component & Layout Migration**
    *   **Goal:** Replace the basic layout and homepage structure of `apps/frontend` with the core components from the mockup, integrating existing authentication.
    *   Migrate static assets (logos, etc.).
    *   Copy and adapt the Navbar and Footer components.
    *   Integrate existing authentication (`AuthButtons`) into the new Navbar.
    *   Update the root layout (`layout.tsx`) to use the new Navbar and Footer.
    *   Copy the main content components for the homepage (Hero, Features, Contact, etc.).
    *   Rebuild the homepage (`page.tsx`) using the migrated components.

4.  **Phase 4: Additional Page Migration & Routing**
    *   **Goal:** Migrate specific pages (like `/projects`) from the mockup and ensure internal navigation uses Next.js routing.
    *   Create new page routes within `apps/frontend/src/app/`.
    *   Copy content and components for these pages.
    *   Replace `react-router-dom` links with `next/link`.

5.  **Phase 5: Cleanup & Verification**
    *   **Goal:** Remove obsolete code from the gold master frontend, clean up dependencies, and verify the final result.
    *   Remove unused original pages/components (e.g., `/dashboard`).
    *   Remove associated tests for deleted components.
    *   Remove unused dependencies (e.g., `react-router-dom`).
    *   Run linters, formatters, and type checkers.
    *   Perform final functional and visual checks.