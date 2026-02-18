/**
 * Unit tests for the i18n module.
 */
import { describe, it, expect } from 'vitest'
import i18next from 'i18next'

describe('i18n', () => {
  it('is initialized', () => {
    expect(i18next.isInitialized).toBe(true)
  })

  it('defaults to German', () => {
    expect(i18next.language).toBe('de')
  })

  it('translates a known German key', () => {
    const result = i18next.t('homepage.title')
    expect(result).toBe('HEAR-UI')
  })

  it('can switch to English', async () => {
    await i18next.changeLanguage('en')
    expect(i18next.language).toBe('en')

    const result = i18next.t('homepage.title')
    expect(result).toBe('HEAR-UI')

    // Switch back to de for other tests
    await i18next.changeLanguage('de')
  })

  it('falls back to German for missing English keys', async () => {
    await i18next.changeLanguage('en')
    // 'search.text' is only in de — should fallback
    const result = i18next.t('search.text')
    expect(result).toBe('Patienten suchen...')

    await i18next.changeLanguage('de')
  })
})
