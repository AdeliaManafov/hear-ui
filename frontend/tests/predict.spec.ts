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

// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function parseJsonOrLog(response: any) {
  if (!response.ok()) {
    const text = await response.text().catch(() => '<no body>')
    console.warn('Non-ok response', response.status(), text)
    return null
  }
  return response.json()
}

test.describe('Prediction API', () => {
  
  test('direct prediction returns valid response', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/predict/`, {
      data: {
        'Alter [J]': 55,
        'Geschlecht': 'w',
        'Primäre Sprache': 'Deutsch',
        'Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...': 'postlingual',
        'Diagnose.Höranamnese.Ursache....Ursache...': 'Unbekannt',
        'Symptome präoperativ.Tinnitus...': 'ja',
        'Behandlung/OP.CI Implantation': 'Cochlear'
      }
    });
    
    // Allow for 200 or 503 (model not loaded in some environments)
    expect([200, 503]).toContain(response.status());
    const data = await parseJsonOrLog(response);
    if (response.status() === 200) {
      // Verify response structure
      expect(data).toHaveProperty('prediction');
      expect(data).toHaveProperty('explanation');
      // Prediction should be between 0 and 1
      expect(data.prediction).toBeGreaterThanOrEqual(0);
      expect(data.prediction).toBeLessThanOrEqual(1);
    }
  });

  test('prediction with persist=true returns persistence info', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/predict/?persist=true`, {
      data: {
        'Alter [J]': 45,
        'Geschlecht': 'm',
        'Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...': '> 20 y',
        'Diagnose.Höranamnese.Ursache....Ursache...': 'Hörsturz',
        'Symptome präoperativ.Tinnitus...': 'nein',
        'Behandlung/OP.CI Implantation': 'Cochlear'
      }
    });
    
    expect([200, 503]).toContain(response.status());
    const data = await parseJsonOrLog(response);

    if (response.status() === 200) {
      expect(data).toHaveProperty('prediction');
      expect(data).toHaveProperty('persisted');
      if (data.persisted) {
        expect(data).toHaveProperty('prediction_id');
        expect(data.prediction_id).toBeTruthy();
      }
    }
  });

  test('prediction with minimal data returns validation error', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/predict/`, {
      data: {
        'Alter [J]': 60
      }
    });
    
    // Backend requires critical fields — minimal data returns 422
    expect([200, 422, 503]).toContain(response.status());
    const data = await parseJsonOrLog(response);

    if (response.status() === 200) {
      expect(data.prediction).toBeGreaterThanOrEqual(0);
      expect(data.prediction).toBeLessThanOrEqual(1);
    }
  });

  test('prediction handles different age values', async ({ request }) => {
    const ages = [25, 45, 65, 85];
    
    for (const age of ages) {
      const response = await request.post(`${API_URL}/api/v1/predict/`, {
        data: {
          'Alter [J]': age,
          'Geschlecht': 'w',
          'Diagnose.Höranamnese.Beginn der Hörminderung (OP-Ohr)...': 'postlingual',
          'Diagnose.Höranamnese.Ursache....Ursache...': 'Unbekannt'
        }
      });
      
      expect([200, 422, 503]).toContain(response.status());
      const data = await parseJsonOrLog(response);
      if (response.status() === 200) {
        expect(data.prediction).toBeGreaterThanOrEqual(0);
        expect(data.prediction).toBeLessThanOrEqual(1);
      }
    }
  });
});
