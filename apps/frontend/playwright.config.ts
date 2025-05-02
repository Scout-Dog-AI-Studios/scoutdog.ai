import { defineConfig, devices } from "@playwright/test";
import path from "path";
import dotenv from "dotenv";

dotenv.config({ path: path.resolve(__dirname, ".", ".env.local") }); // Load .env.local for base URL

const PORT = process.env.PORT || 3000;
const baseURL = process.env.PLAYWRIGHT_BASE_URL || `http://localhost:${PORT}`;

/**
 * See https://playwright.dev/docs/test-configuration.
 */
export default defineConfig({
  testDir: "./e2e", // Directory where E2E tests will live
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html", // Generates an HTML report
  use: {
    baseURL: baseURL,
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],
  // webServer: {
  //   command: 'pnpm run dev',
  //   url: baseURL,
  //   reuseExistingServer: !process.env.CI,
  //   stdout: 'pipe',
  //   stderr: 'pipe',
  // },
});
