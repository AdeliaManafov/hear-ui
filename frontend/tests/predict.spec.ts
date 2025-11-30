/**
 * E2E Tests: Prediction Workflow
 * 
 * Tests the complete prediction flow:
 * 1. POST /predict/ - Direct prediction
 * 2. POST /predict/?persist=true - Persisted prediction
 * 3. Validation of response structure
 */

import { test, expect } from '@playwright/test';

const API_URL = process.env.API_URL || 'http://localhost:8000';

test.describe('Prediction API', () => {
  
  test('direct prediction returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/predict/`, {
      data: {
        'Alter [J]': 55,
        'Geschlecht': 'w',
        'Primäre Sprache': 'Deutsch'
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    // Verify response structure
    expect(data).toHaveProperty('prediction');
    expect(data).toHaveProperty('explanation');
    
    // Prediction should be between 0 and 1
    expect(data.prediction).toBeGreaterThanOrEqual(0);
    expect(data.prediction).toBeLessThanOrEqual(1);
  });

  test('prediction with persist=true returns persistence info', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/predict/?persist=true`, {
      data: {
        'Alter [J]': 45,
        'Geschlecht': 'm',
        'Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...': '> 20 y'
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data).toHaveProperty('prediction');
    expect(data).toHaveProperty('persisted');
    
    if (data.persisted) {
      expect(data).toHaveProperty('prediction_id');
      expect(data.prediction_id).toBeTruthy();
    }
  });

  test('prediction with minimal data uses defaults', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/predict/`, {
      data: {
        'Alter [J]': 60
      }
    });
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    
    expect(data.prediction).toBeGreaterThanOrEqual(0);
    expect(data.prediction).toBeLessThanOrEqual(1);
  });

  test('prediction handles different age values', async ({ request }) => {
    const ages = [25, 45, 65, 85];
    
    for (const age of ages) {
      const response = await request.post(`${API_URL}/api/v1/predict/`, {
        data: { 'Alter [J]': age }
      });
      
      expect(response.ok()).toBeTruthy();
      const data = await response.json();
      expect(data.prediction).toBeGreaterThanOrEqual(0);
      expect(data.prediction).toBeLessThanOrEqual(1);
    }
  });
});
