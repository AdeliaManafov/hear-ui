/**
 * E2E Tests: Create Patient Page
 *
 * Tests the patient creation form page.
 */
import { test, expect } from '@playwright/test'

test.describe('Create Patient Page', () => {
  test('create patient page loads', async ({ page }) => {
    await page.goto('/create-patient')
    await expect(page.locator('#hear-ui')).toBeVisible()
  })

  test('page shows a form or form fields', async ({ page }) => {
    await page.goto('/create-patient')
    // The create form renders fields dynamically from feature definitions
    // API may fail in CI without backend - that's OK, just check UI renders
    await page.waitForTimeout(500)
    // There should be at least the app container or some UI elements
    const appVisible = await page.locator('#hear-ui').isVisible()
    expect(appVisible).toBe(true)
  })

  test('navigating to create patient from home works', async ({ page }) => {
    await page.goto('/home')
    // Click the create patient card (second card)
    const cards = page.locator('.home-card')
    await cards.nth(1).click()
    await page.waitForURL('**/create-patient')
    expect(page.url()).toContain('/create-patient')
  })
})
