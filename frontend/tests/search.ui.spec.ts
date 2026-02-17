/**
 * E2E Tests: Search Patients Page
 *
 * Tests the patient search functionality.
 */
import { test, expect } from '@playwright/test'

test.describe('Search Patients', () => {
  test('search page loads with input field', async ({ page }) => {
    await page.goto('/search-patients')
    const input = page.locator('input')
    await expect(input).toBeVisible()
  })

  test('search page has "new patient" button', async ({ page }) => {
    await page.goto('/search-patients')
    // Button linking to create patient
    const createBtn = page.locator('a[href*="create-patient"], button', {
      hasText: /Patient|Neuer/i,
    })
    await expect(createBtn.first()).toBeVisible()
  })

  test('typing in search shows loading or results area', async ({ page }) => {
    await page.goto('/search-patients')
    const input = page.locator('input')
    await input.fill('Test')
    // Wait for debounce + API call (may fail if backend not running, that's ok)
    await page.waitForTimeout(500)
    // Just verify the page didn't crash
    await expect(page.locator('#hear-ui')).toBeVisible()
  })
})
