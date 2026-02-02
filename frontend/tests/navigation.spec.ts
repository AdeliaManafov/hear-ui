import { test, expect } from '@playwright/test';

test('navigation between main pages', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/HEAR/);

    await page.click('text=Patienten');
    await expect(page).toHaveURL(/.*patients/);

    await page.click('text=Vorhersage');
    await expect(page).toHaveURL(/.*predict/);
});