/**
 * Unit tests for the API_BASE configuration.
 */
import { describe, it, expect } from 'vitest'

describe('API_BASE', () => {
  it('defaults to http://localhost:8000 when env var is not set', async () => {
    // The module reads import.meta.env.VITE_API_URL at import time.
    // In our test environment no VITE_API_URL is set, so it should default.
    const { API_BASE } = await import('@/lib/api')
    expect(API_BASE).toBe('http://localhost:8000')
  })
})
