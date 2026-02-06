import { defineConfig, devices } from '@playwright/test';
import 'dotenv/config'

/**
 * Playwright E2E Test Configuration
 *
 * Tests both API endpoints and UI interactions.
 * API tests can run independently without the frontend.
 */

export default defineConfig({
  testDir: './tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only - increased for stability */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: process.env.CI ? [['html'], ['github'], ['list']] : 'html',
  /* Global timeout - increased for CI stability */
  timeout: process.env.CI ? 90000 : 30000,
  /* Expect timeout */
  expect: {
    timeout: process.env.CI ? 15000 : 5000,
  },
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL for frontend */
    baseURL: process.env.FRONTEND_URL || 'http://localhost:5173',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* Screenshot on failure */
    screenshot: 'only-on-failure',
  },

  /* Configure projects for major browsers */
  projects: [
    // API-only tests (no browser needed, no frontend dependencies)
    {
      name: 'api',
      testMatch: /api-health\.(spec|test)\.ts$/,
      use: {
        baseURL: process.env.API_URL || 'http://localhost:8000',
      },
    },

    // Browser tests (when frontend is ready)
    {
      name: 'chromium',
      testMatch: /.*\.ui\.(spec|test)\.ts/,
      use: {
        ...devices['Desktop Chrome'],
      },
    },
  ],

  /* Run backend before tests if not in CI */
  // webServer: process.env.CI ? undefined : {
  //   command: 'cd ../backend && uvicorn app.main:app --reload',
  //   url: 'http://localhost:8000/api/v1/utils/health-check/',
  //   reuseExistingServer: true,
  // },
});
