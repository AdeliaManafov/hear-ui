/**
 * Unit tests for the AppLayout component.
 */
import { describe, it, expect } from 'vitest'
import { mountWithRouter } from '../test/helpers'
import AppLayout from './AppLayout.vue'

describe('AppLayout.vue', () => {
  it('renders the app shell', async () => {
    const wrapper = await mountWithRouter(AppLayout, { initialRoute: '/home' })
    expect(wrapper.find('#hear-ui').exists()).toBe(true)
  })

  it('renders a navigation drawer', async () => {
    const wrapper = await mountWithRouter(AppLayout, { initialRoute: '/home' })
    expect(wrapper.find('.v-navigation-drawer').exists()).toBe(true)
  })

  it('renders an app bar', async () => {
    const wrapper = await mountWithRouter(AppLayout, { initialRoute: '/home' })
    expect(wrapper.find('.v-app-bar').exists()).toBe(true)
  })

  it('has navigation items in the drawer', async () => {
    const wrapper = await mountWithRouter(AppLayout, { initialRoute: '/home' })
    const navItems = wrapper.findAll('.nav-item')
    // Home, Search, Create, Predictions = 4 items
    expect(navItems.length).toBe(4)
  })

  it('has a language switch button', async () => {
    const wrapper = await mountWithRouter(AppLayout, { initialRoute: '/home' })
    const langBtn = wrapper.find('.language-button')
    expect(langBtn.exists()).toBe(true)
  })

  it('renders a router-view area for content', async () => {
    const wrapper = await mountWithRouter(AppLayout, { initialRoute: '/home' })
    expect(wrapper.find('.v-main').exists()).toBe(true)
  })
})
