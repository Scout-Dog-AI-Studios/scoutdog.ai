import { test, expect } from "@playwright/test";

test("homepage has expected title", async ({ page }) => {
  // Navigate to the base URL defined in playwright.config.ts
  await page.goto("/");

  // Expect the page title to contain "Stack Test App" (adjust if your title is different)
  await expect(page).toHaveTitle(/Stack Test App/);

  // Example: Expect the main heading to be visible
  await expect(page.locator("h1").first()).toBeVisible();
});
