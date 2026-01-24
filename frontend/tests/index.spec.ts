import { createRouter, createWebHistory } from 'vue-router'
import { routes } from '@/router'

describe('Router', () => {
    const router = createRouter({
        history: createWebHistory(),
        routes
    })

    test('enthält erwartete Routen', () => {
        expect(routes).toContainEqual(
            expect.objectContaining({ path: '/', name: 'Home' })
        )
        expect(routes).toContainEqual(
            expect.objectContaining({ path: '/predict', name: 'Predict' })
        )
    })
})
