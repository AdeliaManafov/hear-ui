/**
 * Unit tests for the NotFound (404) page component.
 */
import { describe, it, expect } from 'vitest'
import { mountWithRouter } from '../test/helpers'
import NotFound from './NotFound.vue'

describe('NotFound.vue', () => {
  it('renders 404 error code', async () => {
    const wrapper = await mountWithRouter(NotFound, { initialRoute: '/nonexistent' })
    expect(wrapper.text()).toContain('404')
  })

  it('shows localized "not found" message', async () => {
    const wrapper = await mountWithRouter(NotFound, { initialRoute: '/nonexistent' })
    expect(wrapper.text()).toContain('Seite nicht gefunden')
  })

  it('has a link back to home page', async () => {
    const wrapper = await mountWithRouter(NotFound, { initialRoute: '/nonexistent' })
    const link = wrapper.find('a')
    expect(link.exists()).toBe(true)
    expect(link.attributes('href')).toBe('/')
  })

  it('has a button with home text', async () => {
    const wrapper = await mountWithRouter(NotFound, { initialRoute: '/nonexistent' })
    const button = wrapper.find('button')
    expect(button.exists()).toBe(true)
    expect(button.text()).toContain('Zur Startseite')
  })
})
