/**
 * Unit tests for the HomePage component.
 */
import { describe, it, expect } from 'vitest'
import { mountWithRouter } from '../test/helpers'
import HomePage from './HomePage.vue'

describe('HomePage.vue', () => {
  it('renders the page title', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    expect(wrapper.text()).toContain('HEAR-UI')
  })

  it('renders three navigation cards', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    const cards = wrapper.findAll('.home-card')
    expect(cards.length).toBe(3)
  })

  it('has a card linking to SearchPatients', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    const html = wrapper.html()
    expect(html).toContain('/search-patients')
  })

  it('has a card linking to CreatePatient', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    const html = wrapper.html()
    expect(html).toContain('/create-patient')
  })

  it('has a card linking to PredictionsHome', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    const html = wrapper.html()
    expect(html).toContain('/prediction-home')
  })

  it('displays search patients card text', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    expect(wrapper.text()).toContain('Patienten suchen')
  })

  it('displays create patient card text', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    expect(wrapper.text()).toContain('Patient erstellen')
  })

  it('displays predictions card text', async () => {
    const wrapper = await mountWithRouter(HomePage, { initialRoute: '/home' })
    // The third card uses homepage.prediction_title key
    expect(wrapper.text()).toContain('Vorhersagen')
  })
})
