import { test, expect } from '@playwright/test';

test('shows error message on API failure', async ({ page }) => {
    // Mock API to fail (match v1 endpoints)
    await page.route('**/api/v1/patients*', route => route.abort());

    await page.goto('/patients');
    // Prefer data-test selectors for stability
    await expect(page.locator('[data-test="error-message"]')).toBeVisible({ timeout: 5000 });
});
