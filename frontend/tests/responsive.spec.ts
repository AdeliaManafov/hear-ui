import { test, expect } from '@playwright/test';

test.describe('responsive design', () => {
    test('mobile view', async ({ page }) => {
        await page.setViewportSize({ width: 375, height: 667 });
        await page.goto('/');
        await expect(page.locator('.mobile-menu')).toBeVisible();
    });
});