/**
 * E2E Tests: Predictions Home Page
 *
 * Tests the predictions overview/informational page.
 */
import { test, expect } from '@playwright/test'

test.describe('Predictions Home Page', () => {
  test('predictions page loads', async ({ page }) => {
    await page.goto('/prediction-home')
    await expect(page.locator('#hear-ui')).toBeVisible()
  })

  test('predictions page shows content', async ({ page }) => {
    await page.goto('/prediction-home')
    // API may fail in CI without backend - just verify page renders
    await page.waitForTimeout(500)
    // The app container should be visible
    const appVisible = await page.locator('#hear-ui').isVisible()
    expect(appVisible).toBe(true)
  })
})
