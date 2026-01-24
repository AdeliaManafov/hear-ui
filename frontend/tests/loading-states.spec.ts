import { test, expect } from '@playwright/test';

test('shows loading state while fetching data', async ({ page }) => {
    // Delay API response for patients endpoint (match v1)
    await page.route('**/api/v1/patients*', async route => {
        await new Promise(r => setTimeout(r, 1500));
        await route.continue();
    });

    await page.goto('/patients');
    await expect(page.locator('[data-test="loading-spinner"]')).toBeVisible({ timeout: 5000 });
});
