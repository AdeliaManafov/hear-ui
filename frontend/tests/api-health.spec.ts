/**
 * E2E Tests: API Health & Basic Endpoints
 * 
 * Tests the backend API directly to ensure services are running.
 * These tests don't require authentication.
 */

import { test, expect } from '@playwright/test';

const API_URL = process.env.API_URL || 'http://localhost:8000';

test.describe('API Health Checks', () => {
  test('health check endpoint returns ok', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/v1/utils/health-check/`);
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.status).toBe('ok');
  });

  test('model info endpoint returns model status', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/v1/utils/model-info/`);
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data).toHaveProperty('loaded');
    expect(typeof data.loaded).toBe('boolean');
  });

  test('feature names endpoint returns feature mapping', async ({ request }) => {
    const response = await request.get(`${API_URL}/api/v1/utils/feature-names/`);
    
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    // Returns a dictionary of feature name mappings
    expect(typeof data).toBe('object');
    expect(Object.keys(data).length).toBeGreaterThan(0);
  });
});
