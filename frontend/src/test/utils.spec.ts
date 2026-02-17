/**
 * Unit tests for src/utils.ts — pure validation helpers.
 */
import { describe, it, expect } from 'vitest'
import { emailPattern, namePattern, passwordRules, confirmPasswordRules } from '@/utils'

// ── emailPattern ────────────────────────────────────────────────────
describe('emailPattern', () => {
  it('accepts a valid email', () => {
    expect(emailPattern.value.test('user@example.com')).toBe(true)
  })

  it('accepts email with sub-domain', () => {
    expect(emailPattern.value.test('u@sub.domain.org')).toBe(true)
  })

  it('rejects missing @', () => {
    expect(emailPattern.value.test('userexample.com')).toBe(false)
  })

  it('rejects missing TLD', () => {
    expect(emailPattern.value.test('user@')).toBe(false)
  })

  it('rejects empty string', () => {
    expect(emailPattern.value.test('')).toBe(false)
  })

  it('accepts plus addressing', () => {
    expect(emailPattern.value.test('user+tag@example.com')).toBe(true)
  })
})

// ── namePattern ─────────────────────────────────────────────────────
describe('namePattern', () => {
  it('accepts a simple name', () => {
    expect(namePattern.value.test('Anna')).toBe(true)
  })

  it('accepts names with spaces', () => {
    expect(namePattern.value.test('Anna Maria')).toBe(true)
  })

  it('accepts names with umlauts', () => {
    expect(namePattern.value.test('Müller')).toBe(true)
  })

  it('accepts names with accents', () => {
    expect(namePattern.value.test('José')).toBe(true)
  })

  it('rejects names with digits', () => {
    expect(namePattern.value.test('Anna123')).toBe(false)
  })

  it('rejects empty string', () => {
    expect(namePattern.value.test('')).toBe(false)
  })

  it('rejects names longer than 30 characters', () => {
    expect(namePattern.value.test('A'.repeat(31))).toBe(false)
  })

  it('accepts exactly 30 characters', () => {
    expect(namePattern.value.test('A'.repeat(30))).toBe(true)
  })
})

// ── passwordRules ───────────────────────────────────────────────────
describe('passwordRules', () => {
  it('returns required rule when isRequired=true', () => {
    const rules = passwordRules(true)
    expect(rules.required).toBe('Password is required')
  })

  it('does not include required when isRequired=false', () => {
    const rules = passwordRules(false)
    expect(rules.required).toBeUndefined()
  })

  it('requires minimum 8 characters', () => {
    const rules = passwordRules()
    expect(rules.minLength.value).toBe(8)
  })
})

// ── confirmPasswordRules ────────────────────────────────────────────
describe('confirmPasswordRules', () => {
  it('validates matching passwords', () => {
    const getValues = () => ({ password: 'secret123' })
    const rules = confirmPasswordRules(getValues)
    expect(rules.validate('secret123')).toBe(true)
  })

  it('rejects non-matching passwords', () => {
    const getValues = () => ({ password: 'secret123' })
    const rules = confirmPasswordRules(getValues)
    expect(rules.validate('wrong')).toBe('The passwords do not match')
  })

  it('works with new_password field', () => {
    const getValues = () => ({ new_password: 'newpass99' })
    const rules = confirmPasswordRules(getValues)
    expect(rules.validate('newpass99')).toBe(true)
  })

  it('returns required rule when isRequired=true', () => {
    const getValues = () => ({ password: '' })
    const rules = confirmPasswordRules(getValues, true)
    expect(rules.required).toBe('Password confirmation is required')
  })

  it('does not include required when isRequired=false', () => {
    const getValues = () => ({ password: '' })
    const rules = confirmPasswordRules(getValues, false)
    expect(rules.required).toBeUndefined()
  })
})
