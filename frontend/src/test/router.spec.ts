/**
 * Unit tests for the router configuration.
 */
import { describe, it, expect } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'

// The router module exports the router as default — we need the raw routes
// array, which is not exported. So we import the default router and inspect its
// options.
import router from '@/router/index'

describe('Router configuration', () => {
  it('exports a router instance', () => {
    expect(router).toBeDefined()
    expect(router.getRoutes).toBeDefined()
  })

  it('has the expected number of routes', () => {
    // Routes: redirect(/), home, create-patient, search-patients,
    // prediction/:id, prediction-home, patient-detail/:id,
    // patient-detail/:id/edit, catch-all 404
    const routes = router.getRoutes()
    expect(routes.length).toBeGreaterThanOrEqual(8)
  })

  it('redirects / to /home', async () => {
    const testRouter = createRouter({
      history: createMemoryHistory(),
      routes: router.options.routes,
    })
    await testRouter.push('/')
    await testRouter.isReady()
    expect(testRouter.currentRoute.value.path).toBe('/home')
  })

  it('resolves /home to Home name', () => {
    const resolved = router.resolve('/home')
    expect(resolved.name).toBe('Home')
  })

  it('resolves /create-patient to CreatePatient', () => {
    const resolved = router.resolve('/create-patient')
    expect(resolved.name).toBe('CreatePatient')
  })

  it('resolves /search-patients to SearchPatients', () => {
    const resolved = router.resolve('/search-patients')
    expect(resolved.name).toBe('SearchPatients')
  })

  it('resolves /prediction/:patient_id correctly', () => {
    const resolved = router.resolve('/prediction/abc-123')
    expect(resolved.name).toBe('Prediction')
    expect(resolved.params.patient_id).toBe('abc-123')
  })

  it('resolves /prediction-home to PredictionsHome', () => {
    const resolved = router.resolve('/prediction-home')
    expect(resolved.name).toBe('PredictionsHome')
  })

  it('resolves /patient-detail/:id correctly', () => {
    const resolved = router.resolve('/patient-detail/xyz-789')
    expect(resolved.name).toBe('PatientDetail')
    expect(resolved.params.id).toBe('xyz-789')
  })

  it('resolves /patient-detail/:id/edit to UpdatePatient', () => {
    const resolved = router.resolve('/patient-detail/xyz-789/edit')
    expect(resolved.name).toBe('UpdatePatient')
    expect(resolved.params.id).toBe('xyz-789')
  })

  it('catches unknown routes with NotFound', () => {
    const resolved = router.resolve('/does-not-exist')
    expect(resolved.name).toBe('NotFound')
  })
})
