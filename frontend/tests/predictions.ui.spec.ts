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
    // Wait for any async content to load
    await page.waitForTimeout(1000)
    // The page should have some text content
    const body = await page.textContent('body')
    expect(body!.length).toBeGreaterThan(50)
  })
})
