import { test, expect } from '@playwright/test';

/**
 * Screenshot utility for generating prediction page screenshots
 * Run with: npx playwright test screenshot-prediction.spec.ts --headed
 */

test('capture prediction page screenshot', async ({ page }) => {
  // Navigate to homepage
  await page.goto('http://localhost:5173');
  
  // Wait for the page to load
  await page.waitForLoadState('networkidle');
  
  // Navigate to create patient if needed, or search for existing patient
  // For now, let's try to find an existing patient
  await page.click('a:has-text("Search Patients")');
  
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(1000);
  
  // Click on the first patient in the list (if any)
  const firstPatient = page.locator('.patient-card, .patient-item, a[href*="/patients/"]').first();
  
  if (await firstPatient.count() > 0) {
    await firstPatient.click();
    await page.waitForLoadState('networkidle');
    
    // Click on "Generate Prediction" or similar button
    const predictButton = page.locator('button:has-text("Prediction"), button:has-text("Generate Prediction"), a:has-text("Prediction")').first();
    
    if (await predictButton.count() > 0) {
      await predictButton.click();
      await page.waitForLoadState('networkidle');
      await page.waitForTimeout(2000); // Wait for chart to render
      
      // Take screenshot of the full page
      await page.screenshot({ 
        path: '/Users/adeliamanafov/hearUI_project/hear-ui/2026_XAI_Demo_Explaining_Clinical_Predictions_for_Tabular_Data-3/figures/imagesHearUI/3_1_Prediction_ResultsExplanation_NEW.png',
        fullPage: true 
      });
      
      console.log('Screenshot saved to 3_1_Prediction_ResultsExplanation_NEW.png');
    } else {
      console.log('Could not find prediction button');
    }
  } else {
    console.log('No patients found. Please create a patient first.');
  }
});
