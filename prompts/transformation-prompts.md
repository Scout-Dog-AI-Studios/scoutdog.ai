## Iterative Step Breakdown (Refined for Prompts)

Here's a more granular breakdown, sized for incremental LLM prompts:

**Phase 2: Frontend Preparation**

1.  **(P2.1)** Install UI/utility dependencies from `mockup/` into `apps/frontend`.
2.  **(P2.2)** Copy Shadcn UI components (`ui/`), utils (`lib/`), hooks (`hooks/`), and config (`components.json`) from `mockup/` to `apps/frontend`.
3.  **(P2.3)** Merge `tailwind.config.ts`: Combine base config from `apps/frontend` with Shadcn setup, custom colors, and animations from `mockup/`.
4.  **(P2.4)** Merge Global CSS: Combine `apps/frontend/src/app/globals.css` with necessary base styles/variables from `mockup/src/index.css` for Shadcn/Tailwind compatibility in Next.js.

**Phase 3: Core Component & Layout Migration**

5.  **(P3.1)** Migrate static assets (images) from `mockup/public/` to `apps/frontend/public/`.
6.  **(P3.2)** Copy structural components (`Navbar.tsx`, `Footer.tsx`) from `mockup/src/components/` to `apps/frontend/src/components/`.
7.  **(P3.3)** Update `apps/frontend/src/app/layout.tsx` to import and use the new Navbar and Footer, replacing the old placeholder header/footer.
8.  **(P3.4)** Integrate Authentication into Navbar: Modify the copied `Navbar.tsx` in `apps/frontend` to use the `useAuth0` hook and incorporate the login/logout logic (similar to the original `AuthButtons.tsx`). Mark Navbar as a client component.
9.  **(P3.5)** Copy homepage section components (`Hero.tsx`, `Features.tsx`, `Projects.tsx` (section component), `Contact.tsx`) from `mockup/src/components/` to `apps/frontend/src/components/`.
10. **(P3.6)** Rebuild `apps/frontend/src/app/page.tsx` to import and render the migrated homepage section components (Hero, Features, Projects section, Contact), mirroring the structure of `mockup/src/pages/Index.tsx`.

**Phase 4: Additional Page Migration & Routing**

11. **(P4.1)** Create `apps/frontend/src/app/projects/page.tsx`.
12. **(P4.2)** Copy the content and structure from `mockup/src/pages/Projects.tsx` into the new `apps/frontend/src/app/projects/page.tsx`, ensuring necessary component imports are adjusted (e.g., Navbar, Footer are handled by the layout).
13. **(P4.3)** Update Navigation Links: Search through all migrated components (Navbar, Footer, etc.) in `apps/frontend/src/components/` and replace internal navigation `<a>` tags or `react-router-dom` `<Link>` components with Next.js `<Link href="...">` components. Ensure `href` attributes point to the correct App Router paths (e.g., `/projects`).

**Phase 5: Cleanup & Verification**

14. **(P5.1)** Remove Obsolete Page/Components: Delete the `apps/frontend/src/app/dashboard/` directory and its contents. Delete the original `apps/frontend/src/components/AuthButtons.tsx` (as its logic is now in Navbar).
15. **(P5.2)** Remove Obsolete Tests: Delete test files related to the `/dashboard` page (e.g., `apps/frontend/src/app/dashboard/*.test.tsx`). Also delete tests related to the original `AuthButtons` if they exist. _Keep API interaction tests if applicable to new UI_.
16. **(P5.3)** Remove Unused Dependencies: Check `apps/frontend/package.json` for `react-router-dom` and remove it if present. Run `pnpm install --filter frontend` (or root `pnpm install`) to update the lockfile.
17. **(P5.4)** Run Quality Checks: Execute `task lint`, `task format`, `task typecheck` from the root directory and address any issues reported specifically for `apps/frontend`.
18. **(P5.5)** Final Verification (Instruction): Instruct the user to run `pnpm dev`, test navigation (Home, Projects), login/logout flow, check component rendering, and look for browser console errors.

---

## LLM Prompts for Transformation

Here are the prompts based on the refined steps. Each prompt assumes the previous one was successfully completed.

---

**Prompt P2.1: Install Mockup Dependencies**

```text
Objective: Add necessary UI and utility library dependencies from the `mockup` project to the `apps/frontend` project.

Context: The `mockup/` directory uses Shadcn UI and other libraries. We need to ensure `apps/frontend` has these installed to render the new components.

Instructions:
1.  Examine the `dependencies` and `devDependencies` in `mockup/package.json`.
2.  Identify libraries essential for the UI components and styling that are *not* already present or are different versions in `apps/frontend/package.json`. Key libraries likely include:
    *   `@radix-ui/*` (various components)
    *   `lucide-react`
    *   `class-variance-authority`
    *   `clsx`
    *   `tailwind-merge`
    *   `tailwindcss-animate`
    *   `embla-carousel-react` (if carousels are used)
    *   `react-hook-form` / `@hookform/resolvers/zod` / `zod` (if forms are used)
    *   `sonner` / `react-day-picker` / `recharts` / `vaul` etc. (based on specific Shadcn components used in the mockup)
3.  Navigate to the monorepo root directory in your terminal.
4.  Use `pnpm add` to install these identified libraries specifically into the `apps/frontend` workspace. Use the `-D` flag for development dependencies (like types). Example:
    `pnpm add lucide-react class-variance-authority clsx tailwind-merge tailwindcss-animate @radix-ui/react-slot --filter frontend`
    `pnpm add -D @types/node --filter frontend` (Example dev dep)
    *Ensure you add all necessary Radix packages used by the Shadcn components present in `mockup/src/components/ui`.*
5.  After adding all dependencies, run `pnpm install` from the root directory to ensure the lockfile is updated and dependencies are correctly linked.
```

---

**Prompt P2.2: Copy UI Components, Utils, Hooks & Shadcn Config**

```text
Objective: Transfer the core Shadcn UI setup files and related utilities from the `mockup` project to `apps/frontend`.

Context: Shadcn UI relies on generated UI components, utility functions, and potentially custom hooks. We need these files in `apps/frontend`.

Instructions:
1.  **Copy UI Components:** Recursively copy the entire `mockup/src/components/ui` directory to `apps/frontend/src/components/ui`. Overwrite if the directory already exists (it shouldn't based on the gold master).
2.  **Copy Utils:** Copy the `mockup/src/lib/utils.ts` file to `apps/frontend/src/lib/utils.ts`. Create the `lib` directory if it doesn't exist.
3.  **Copy Hooks:** Recursively copy the entire `mockup/src/hooks` directory (containing `use-toast.ts`, `use-mobile.tsx`) to `apps/frontend/src/hooks`. Create the `hooks` directory if it doesn't exist.
4.  **Copy Shadcn Config:** Copy the `mockup/components.json` file to the root of the `apps/frontend` directory.
5.  Verify that the following now exist:
    *   `apps/frontend/src/components/ui/` (with many `.tsx` files like `button.tsx`, `card.tsx`, etc.)
    *   `apps/frontend/src/lib/utils.ts`
    *   `apps/frontend/src/hooks/` (with `use-toast.ts`, `use-mobile.tsx`)
    *   `apps/frontend/components.json`
```

---

**Prompt P2.3: Merge Tailwind Configuration**

```text
Objective: Update the Tailwind CSS configuration in `apps/frontend` to support Shadcn UI and include custom styles from the mockup.

Context: Both projects use Tailwind, but the configurations need to be merged to include Shadcn's base styles, CSS variables, the `tailwindcss-animate` plugin, and the custom `scoutdog` colors/animations from the mockup.

Instructions:
1.  Open `apps/frontend/tailwind.config.ts`.
2.  Open `mockup/tailwind.config.ts`.
3.  Modify `apps/frontend/tailwind.config.ts` to incorporate the necessary elements from the mockup's config:
    *   **Content:** Ensure the `content` array includes paths relevant to Shadcn components (e.g., `./src/**/*.{ts,tsx}`). It should already cover `app/` and `components/`.
    *   **DarkMode:** Ensure `darkMode: ["class"]` is present.
    *   **Theme Extensions:**
        *   Merge the `extend.colors` section, adding the `scoutdog` colors and the Shadcn color definitions (border, input, ring, background, foreground, primary, secondary, destructive, muted, accent, popover, card, sidebar). Ensure hsl values are correctly defined using CSS variables as per Shadcn setup.
        *   Merge `extend.borderRadius`.
        *   Merge `extend.keyframes` (e.g., `accordion-down`, `accordion-up`, `fade-in`, `slide-up`).
        *   Merge `extend.animation`.
    *   **Plugins:** Add `require("tailwindcss-animate")` to the `plugins` array.
4.  Ensure the final `apps/frontend/tailwind.config.ts` correctly defines CSS variables for colors as expected by Shadcn UI (e.g., `border: 'hsl(var(--border))'`).
5.  Save the updated `apps/frontend/tailwind.config.ts`.

Reference `FRONTEND_RULES.md` for styling guidelines.
```

---

**Prompt P2.4: Merge Global CSS**

```text
Objective: Update the global CSS file in `apps/frontend` to include base styles required by Shadcn UI and Tailwind CSS variables.

Context: Shadcn UI relies on specific CSS variables and base styles being present. These need to be merged into the existing Next.js global stylesheet.

Instructions:
1.  Open `apps/frontend/src/app/globals.css`.
2.  Open `mockup/src/index.css`.
3.  Modify `apps/frontend/src/app/globals.css`:
    *   Ensure the `@tailwind base;`, `@tailwind components;`, `@tailwind utilities;` directives are present at the top.
    *   Copy the `@layer base { ... }` rules from `mockup/src/index.css` (both `:root` and `.dark`) which define the CSS variables for colors (background, foreground, card, popover, primary, etc.) and border-radius. Place these *after* the Tailwind directives.
    *   Copy the base body styles and any other essential base layer configurations from the mockup's CSS file into the `@layer base` section.
    *   Remove any conflicting base styles that might have been in the original `globals.css`. The result should prioritize Shadcn's variable setup.
4.  Ensure the CSS variables defined match those used in the updated `tailwind.config.ts`.
5.  Save the updated `apps/frontend/src/app/globals.css`.

Reference `FRONTEND_RULES.md`.
```

---

**Prompt P3.1: Migrate Static Assets**

```text
Objective: Copy required static image assets from the mockup to the `apps/frontend` public directory.

Context: The mockup uses a logo image (`lovable-uploads/0ad7e8a3-7d57-431d-b098-6a765f30f2e6.png`) referenced in its components (Navbar, Footer, Hero).

Instructions:
1.  Locate the logo image file within the `mockup/public/` directory (it appears to be in `mockup/public/lovable-uploads/`).
2.  Copy this image file (and its directory structure if desired, or place it directly) into the `apps/frontend/public/` directory. For example, copy `mockup/public/lovable-uploads/0ad7e8a3-7d57-431d-b098-6a765f30f2e6.png` to `apps/frontend/public/scoutdog-logo.png` (renaming for clarity is recommended).
3.  Verify the image file now exists in `apps/frontend/public/`. Remember the new path for updating component references later.
```

---

**Prompt P3.2: Copy Structural Components (Navbar, Footer)**

```text
Objective: Copy the Navbar and Footer React components from the mockup project to `apps/frontend`.

Context: These components define the main layout structure for the new design.

Instructions:
1.  Copy the file `mockup/src/components/Navbar.tsx` to `apps/frontend/src/components/Navbar.tsx`.
2.  Copy the file `mockup/src/components/Footer.tsx` to `apps/frontend/src/components/Footer.tsx`.
3.  Check the copied files for any immediate import errors (though functionality will be addressed later). Adjust relative paths within these files if necessary (e.g., if they import other components from `mockup/src/components`).
4.  Ensure the image path used in the copied Navbar/Footer components is updated to reflect the new location within `apps/frontend/public/` (e.g., change from `/lovable-uploads/...` to `/scoutdog-logo.png`).
```

---

**Prompt P3.3: Update Root Layout**

````text
Objective: Modify the root layout of `apps/frontend` to use the newly copied Navbar and Footer components.

Context: `apps/frontend/src/app/layout.tsx` currently defines the overall page structure, likely with placeholder header/footer elements.

Instructions:
1.  Open `apps/frontend/src/app/layout.tsx`.
2.  Import the `Navbar` and `Footer` components:
    ```typescript
    import Navbar from '@/components/Navbar';
    import Footer from '@/components/Footer';
    ```
3.  Locate the existing header/footer elements (potentially `header` and `footer` tags with placeholder text or the old `AuthButtons`).
4.  Replace the existing header element/content with `<Navbar />`.
5.  Replace the existing footer element/content with `<Footer />`.
6.  Ensure the main `{children}` prop is placed correctly between the Navbar and Footer.
7.  Remove the direct import and usage of the old `AuthButtons` component from `layout.tsx` if it was there (it will be integrated into Navbar next).
8.  Save the updated `apps/frontend/src/app/layout.tsx`.
````

---

**Prompt P3.4: Integrate Authentication into Navbar**

````text
Objective: Modify the newly copied `Navbar.tsx` component in `apps/frontend` to handle user authentication using the existing Auth0 setup.

Context: The original `apps/frontend` used `AuthButtons.tsx` which contained the `useAuth0` hook logic. This logic needs to be moved into or utilized by the new Navbar. The mockup Navbar has a placeholder Login button.

Instructions:
1.  Open `apps/frontend/src/components/Navbar.tsx`.
2.  Add the `'use client';` directive at the top of the file, as it will now use hooks.
3.  Import the necessary items from `@auth0/auth0-react`:
    ```typescript
    import { useAuth0 } from '@auth0/auth0-react';
    import { LogIn } from 'lucide-react'; // Keep LogIn icon if used
    ```
4.  Inside the `Navbar` component function, call the hook:
    ```typescript
    const { isAuthenticated, loginWithRedirect, logout, isLoading, user } = useAuth0();
    ```
5.  Locate the placeholder Login button (likely a `<Button>` component).
6.  Replace the placeholder button logic with conditional rendering based on `isAuthenticated`:
    *   If `isLoading`, show a loading indicator (e.g., `<div className="text-sm text-gray-500">Loading...</div>`).
    *   If `!isAuthenticated`, render the "Log In" button. Add an `onClick` handler: `onClick={() => loginWithRedirect()}`.
    *   If `isAuthenticated`, render a "Log Out" button. Add an `onClick` handler: `onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}`. You might want to display the user's name/email (`user?.name || user?.email`) here as well. Style the logout button appropriately (e.g., using red color or similar).
7.  Remove any unused state variables related to the mobile menu's open state if the Auth0 `isLoading` state can cover the initial render phase. Keep mobile menu toggle logic if needed.
8.  Ensure necessary icons like `LogIn` or potentially a user avatar icon are imported and used correctly.
9.  Save the updated `apps/frontend/src/components/Navbar.tsx`.

Reference `FRONTEND_RULES.md` regarding Auth0 usage.
````

---

**Prompt P3.5: Copy Homepage Section Components**

```text
Objective: Copy the React components that make up the sections of the mockup's homepage into `apps/frontend`.

Context: The mockup's `Index.tsx` page uses several distinct components (`Hero.tsx`, `Features.tsx`, `Projects.tsx` (the section component, not the page), `Contact.tsx`) to build its content.

Instructions:
1.  Copy the following files from `mockup/src/components/` to `apps/frontend/src/components/`:
    *   `Hero.tsx`
    *   `Features.tsx`
    *   `Projects.tsx` (Verify this is the component used on the index page, not the full page `mockup/src/pages/Projects.tsx`)
    *   `Contact.tsx`
2.  Review the copied components for imports. Ensure they correctly import UI elements from `@/components/ui` and utils from `@/lib/utils` within the `apps/frontend` structure. Update image paths if they reference assets now in `apps/frontend/public/` (like the Hero image).
```

---

**Prompt P3.6: Rebuild Homepage (`page.tsx`)**

````text
Objective: Update the main homepage file (`page.tsx`) in `apps/frontend` to use the newly migrated section components.

Context: `apps/frontend/src/app/page.tsx` currently contains the gold master's placeholder content. It needs to be replaced with the structure defined in the mockup's `Index.tsx`.

Instructions:
1.  Open `apps/frontend/src/app/page.tsx`.
2.  Delete the existing content within the main functional component.
3.  Import the necessary section components copied in the previous step:
    ```typescript
    import Hero from '@/components/Hero';
    import Features from '@/components/Features'; // Assuming Features component exists
    import Projects from '@/components/Projects'; // The section component
    import Contact from '@/components/Contact';
    // Import any other necessary components used directly on the mockup index page
    ```
4.  Replicate the component structure from `mockup/src/pages/Index.tsx`. It likely involves rendering the components sequentially:
    ```typescript
    export default function Home() {
      return (
        <div> {/* Or fragment <> */}
          <Hero />
          <Features /> {/* Add if present */}
          <Projects /> {/* Add if present */}
          <Contact />
          {/* Add any other sections */}
        </div>
      );
    }
    ```
5.  Ensure there are no remnants of the old dashboard or placeholder content.
6.  Save the updated `apps/frontend/src/app/page.tsx`.
````

---

**Prompt P4.1: Create Projects Page Route**

```text
Objective: Create the file structure for the `/projects` page in the Next.js App Router.

Context: The mockup has a dedicated projects page (`mockup/src/pages/Projects.tsx`). We need to create the corresponding route in `apps/frontend`.

Instructions:
1.  Create a new directory named `projects` inside `apps/frontend/src/app/`.
2.  Inside the newly created `apps/frontend/src/app/projects/` directory, create a file named `page.tsx`.
3.  Verify the file `apps/frontend/src/app/projects/page.tsx` exists.
```

---

**Prompt P4.2: Populate Projects Page Content**

```text
Objective: Copy the content and structure from the mockup's Projects page into the new `/projects` page in `apps/frontend`.

Context: We created the file structure in the previous step. Now we need to add the actual content.

Instructions:
1.  Open `mockup/src/pages/Projects.tsx`.
2.  Open the newly created `apps/frontend/src/app/projects/page.tsx`.
3.  Copy the JSX structure and component logic (including imports, state, data definitions like the `projects` array) from `mockup/src/pages/Projects.tsx` into `apps/frontend/src/app/projects/page.tsx`.
4.  **Crucially:** Remove the `Navbar` and `Footer` imports and rendering from the copied code, as these are now handled by the root `layout.tsx` in `apps/frontend`. Ensure only the page-specific content (like the heading, description, and project card grid) remains within the main function's return statement.
5.  Adjust imports for components (like `Button` from `@/components/ui`) to use the correct paths within `apps/frontend`.
6.  Save the updated `apps/frontend/src/app/projects/page.tsx`.
```

---

**Prompt P4.3: Update Navigation Links**

```text
Objective: Replace all internal navigation links in the migrated components with Next.js `<Link>` components.

Context: Components copied from the mockup (which used `react-router-dom` or simple `<a>` tags for navigation) need to be updated to use Next.js's router for client-side navigation.

Instructions:
1.  Search within the `apps/frontend/src/components/` directory (specifically in `Navbar.tsx`, `Footer.tsx`, and potentially others like `Hero.tsx` if they contain links) for:
    *   `<a>` tags with `href` attributes pointing to internal routes (like `/projects`, `/`, `#contact`, `#features`).
    *   `<Link>` components imported from `react-router-dom`.
2.  For each instance found:
    *   Import the `Link` component from `next/link`: `import Link from 'next/link';`.
    *   Replace the `<a>` tag or `react-router-dom` `<Link>` with the Next.js `<Link>`.
    *   Ensure the `href` attribute points to the correct App Router path (e.g., `/projects`).
    *   For hash links (`#contact`, `#features`), keep them as standard `<a>` tags, as Next.js `<Link>` doesn't handle hash scrolling by default without extra logic or if the target ID is on the *same* page. If these sections are on the homepage, ensure the links in the Navbar/Footer point to `/#contact` or `/#features`.
    *   Preserve any existing class names or styling attributes.
3.  Pay close attention to the Navbar links to ensure they point correctly to `/` and `/projects`.
4.  Save all modified files.

Reference `FRONTEND_RULES.md`.
```

---

**Prompt P5.1: Remove Obsolete Page/Components**

```text
Objective: Remove the original dashboard page and related components from the gold master frontend, as they are replaced by the new design.

Context: The `apps/frontend` project contained a `/dashboard` route and potentially specific `AuthButtons` component which are no longer needed.

Instructions:
1.  Delete the entire directory `apps/frontend/src/app/dashboard/`.
2.  Delete the file `apps/frontend/src/components/AuthButtons.tsx` (verify its logic was successfully merged into `Navbar.tsx` in step P3.4).
3.  Check `apps/frontend/src/app/layout.tsx` and `apps/frontend/src/app/page.tsx` again to ensure no references to the deleted dashboard or AuthButtons remain.
```

---

**Prompt P5.2: Remove Obsolete Tests**

```text
Objective: Remove tests associated with the deleted dashboard components.

Context: Test files for the `/dashboard` page are no longer relevant.

Instructions:
1.  Examine the `apps/frontend/` directory for test files related to the dashboard. These are likely located in `apps/frontend/src/app/dashboard/` (which was deleted) or potentially a general `__tests__` or `tests` directory if structured differently.
2.  Delete any files matching patterns like:
    *   `apps/frontend/src/app/dashboard/*.test.tsx`
    *   `apps/frontend/src/app/dashboard/**/*.test.tsx`
    *   Any tests specifically importing and testing the old `AuthButtons.tsx` component.
3.  Be cautious *not* to delete tests for reusable components (like UI elements) or core functionality (like providers) unless they are truly obsolete. API fetching tests might need adaptation rather than deletion.
```

---

**Prompt P5.3: Remove Unused Dependencies**

```text
Objective: Clean up `apps/frontend/package.json` by removing dependencies specific to the mockup's old setup (like `react-router-dom`) that are no longer needed.

Context: Migrating from the Vite/React Router mockup might leave unused dependencies.

Instructions:
1.  Open `apps/frontend/package.json`.
2.  Search for the `react-router-dom` dependency. If found, remove it from `dependencies`.
3.  Review other dependencies to see if any others were specific only to the mockup setup and not used by Next.js or the migrated components (this requires careful review).
4.  Navigate to the monorepo root directory.
5.  Run `pnpm install` to update the `pnpm-lock.yaml` file and remove the specified packages from `node_modules`.
```

---

**Prompt P5.4: Run Quality Checks**

```text
Objective: Ensure the transformed code adheres to linting, formatting, and type safety rules.

Context: Significant code changes have been made. Linters, formatters, and type checkers help catch errors and maintain consistency.

Instructions:
1.  Navigate to the monorepo root directory.
2.  Run the linting task: `task lint` (or `pnpm lint`). Address any errors reported, particularly in `apps/frontend`.
3.  Run the formatting task: `task format` (or `pnpm format`). This should automatically fix formatting issues.
4.  Run the type checking task: `task typecheck` (or `pnpm typecheck --filter frontend`). Address any TypeScript errors reported in `apps/frontend`.
5.  Repeat these steps until all checks pass without errors.

Reference `FRONTEND_RULES.md`, `BACKEND_RULES.md`, `INFRA_RULES.md`.
```

---

**Prompt P5.5: Final Verification (Instruction)**

```text
Objective: Perform a final manual check of the running application.

Context: Automated checks are complete. A manual walkthrough is needed to catch visual glitches, runtime errors, or unexpected behavior.

Instructions for User:
1.  Ensure any required backend services (like the FastAPI app) are running if testing API interactions. You can usually start everything with `pnpm dev` from the root.
2.  Navigate to the frontend application URL (typically `http://localhost:3000`).
3.  Verify the homepage (`/`) renders correctly with the new Hero, Features, Projects, and Contact sections. Check the layout, styling, and responsiveness.
4.  Test navigation: Click links in the Navbar and Footer to go to the Home (`/`) and Projects (`/projects`) pages. Verify client-side navigation works smoothly. Check hash links (`#contact`) if they exist.
5.  Test Authentication:
    *   Click the "Log In" button in the Navbar. Verify redirection to Auth0 and successful login.
    *   After login, verify the Navbar updates to show a "Log Out" button and potentially user information.
    *   Click the "Log Out" button. Verify successful logout and redirection back to the application.
6.  Check the browser's developer console for any JavaScript errors or warnings.
7.  Briefly check the `/projects` page rendering.

Report any issues found.
```
