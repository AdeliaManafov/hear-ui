/**
 * Shared test helpers for mounting Vue components with router, Vuetify, i18n.
 */
import { mount, type ComponentMountingOptions } from '@vue/test-utils'
import { createRouter, createMemoryHistory, type RouteRecordRaw } from 'vue-router'
import { type Component } from 'vue'

/**
 * Minimal route stubs – enough for router-link / router-view to work.
 */
const stubRoutes: RouteRecordRaw[] = [
  { path: '/', redirect: '/home' },
  { path: '/home', name: 'Home', component: { template: '<div>Home</div>' } },
  { path: '/create-patient', name: 'CreatePatient', component: { template: '<div>Create</div>' } },
  { path: '/search-patients', name: 'SearchPatients', component: { template: '<div>Search</div>' } },
  { path: '/prediction/:patient_id', name: 'Prediction', component: { template: '<div>Prediction</div>' } },
  { path: '/prediction-home', name: 'PredictionsHome', component: { template: '<div>PredictionsHome</div>' } },
  { path: '/patient-detail/:id', name: 'PatientDetail', component: { template: '<div>PatientDetail</div>' } },
  { path: '/patient-detail/:id/edit', name: 'UpdatePatient', component: { template: '<div>Update</div>' } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: { template: '<div>404</div>' } },
]

/**
 * Mount a component with an in-memory router already pushed to `initialRoute`.
 */
export async function mountWithRouter(
  component: Component,
  options: ComponentMountingOptions<any> & { initialRoute?: string } = {},
) {
  const { initialRoute = '/', ...mountOptions } = options
  const router = createRouter({
    history: createMemoryHistory(),
    routes: stubRoutes,
  })

  router.push(initialRoute)
  await router.isReady()

  return mount(component, {
    ...mountOptions,
    global: {
      ...(mountOptions.global ?? {}),
      plugins: [...(mountOptions.global?.plugins ?? []), router],
    },
  })
}
