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
    // Wait a bit for the definitions API call
    await page.waitForTimeout(1000)
    // There should be at least a form element or input fields
    const hasForm = await page.locator('form').count()
    const hasInputs = await page.locator('input, select, textarea').count()
    expect(hasForm + hasInputs).toBeGreaterThan(0)
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
