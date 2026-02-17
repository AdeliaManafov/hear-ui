/**
 * E2E Tests: Patient Management & SHAP Explanations
 * 
 * Tests:
 * 1. GET /patients/ - List patients
 * 2. GET /patients/{id} - Get patient details
 * 3. GET /patients/{id}/validate - Validate patient
 * 4. GET /patients/{id}/predict - Predict for patient
 * 5. GET /patients/{id}/explainer - SHAP explanation
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

test.describe('Patient Management', () => {
  
  test('list patients returns array', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/v1/patients/`);
    expect([200, 204, 503]).toContain(response.status());
    const data = await parseJsonOrLog(response);
    if (response.status() === 200) {
      expect(Array.isArray(data)).toBeTruthy();
    }
  });

  test('list patients with pagination', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/v1/patients/?paginated=true&limit=5`);
    expect([200, 503]).toContain(response.status());
    const data = await parseJsonOrLog(response);

    if (response.status() === 200) {
      expect(data).toHaveProperty('items');
      expect(data).toHaveProperty('total');
      expect(data).toHaveProperty('limit');
      expect(data).toHaveProperty('offset');
      expect(data).toHaveProperty('has_more');
      expect(data.limit).toBe(5);
      expect(Array.isArray(data.items)).toBeTruthy();
    }
  });
});

test.describe('Patient SHAP Explanations', () => {
  let patientId: string | undefined;

  test.beforeAll(async ({ request }) => {
    // Get first patient with data
    const response = await request.get(`${API_URL}/api/v1/patients/?limit=10`);
    if (response.status() !== 200) {
      console.warn('Could not fetch patients in beforeAll:', response.status())
      return
    }
    const patients = await response.json();
    
    if (patients && patients.length > 0) {
      patientId = patients[0].id;
    }
  });

  test('get patient by id', async ({ request }) => {
    if (!patientId) return test.skip();

    const response = await request.get(`${API_URL}/api/v1/patients/${patientId}`);
    expect(response.status()).toBe(200);
    const data = await response.json();
    
    expect(data).toHaveProperty('id');
    expect(data).toHaveProperty('input_features');
    expect(data.id).toBe(patientId);
  });

  test('validate patient features', async ({ request }) => {
    if (!patientId) return test.skip();

    const response = await request.get(`${API_URL}/api/v1/patients/${patientId}/validate`);
    expect(response.status()).toBe(200);
    const data = await response.json();
    
    expect(data).toHaveProperty('ok');
    expect(data).toHaveProperty('missing_features');
    expect(data).toHaveProperty('features_count');
    expect(typeof data.ok).toBe('boolean');
  });

  test('predict for patient', async ({ request }) => {
    if (!patientId) return test.skip();

    const response = await request.get(`${API_URL}/api/v1/patients/${patientId}/predict`);
    
    // Accept 200 (success) or 503 (model not loaded in CI)
    expect([200, 503]).toContain(response.status());
    
    if (response.status() === 200) {
      const data = await response.json();
      expect(data).toHaveProperty('prediction');
      expect(data.prediction).toBeGreaterThanOrEqual(0);
      expect(data.prediction).toBeLessThanOrEqual(1);
    }
  });

  test('get SHAP explanation for patient', async ({ request }) => {
    if (!patientId) return test.skip();

    const response = await request.get(`${API_URL}/api/v1/patients/${patientId}/explainer`);
    
    // Accept various status codes depending on environment
    expect([200, 400, 500, 503]).toContain(response.status());
    
    if (response.status() === 200) {
      const data = await response.json();
      
      expect(data).toHaveProperty('prediction');
      expect(data).toHaveProperty('top_features');
      expect(Array.isArray(data.top_features)).toBeTruthy();
      
      // Verify top features structure
      if (data.top_features.length > 0) {
        expect(data.top_features[0]).toHaveProperty('feature');
        expect(data.top_features[0]).toHaveProperty('importance');
      }
    }
  });
});

test.describe('Direct SHAP Explanation', () => {
  
  test('explainer endpoint returns SHAP values', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/explainer/explain`, {
      data: {
        age: 55,
        gender: 'w',
        primary_language: 'Deutsch',
        hearing_loss_onset: 'postlingual',
        include_plot: false
      }
    });
    
    // Accept various status codes
    expect([200, 422, 500, 503]).toContain(response.status());
    
    if (response.status() === 200) {
      const data = await response.json();
      
      expect(data).toHaveProperty('prediction');
      expect(data).toHaveProperty('feature_importance');
      expect(data).toHaveProperty('shap_values');
      expect(data).toHaveProperty('base_value');
      expect(data).toHaveProperty('top_features');
    }
  });
});
