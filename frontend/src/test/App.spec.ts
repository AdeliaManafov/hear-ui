import { describe, it, expect } from 'vitest'
import { mountWithRouter } from './helpers'
import App from '../App.vue'

describe('App.vue', () => {
  it('mounts without error', async () => {
    const wrapper = await mountWithRouter(App, { initialRoute: '/home' })
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the AppLayout component', async () => {
    const wrapper = await mountWithRouter(App, { initialRoute: '/home' })
    // AppLayout contains a v-app with id "hear-ui"
    expect(wrapper.find('#hear-ui').exists()).toBe(true)
  })
})
