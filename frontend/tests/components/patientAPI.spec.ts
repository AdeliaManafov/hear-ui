import { describe, test, expect, vi } from 'vitest'
import { patientApi } from '@/api/patient'
import axios from 'axios'

// Use Vitest mocking API instead of Jest
vi.mock('axios')

describe('patientApi', () => {
    test('sendet Vorhersageanfrage korrekt', async () => {
        const mockResponse = {
            data: { probability: 0.85 }
        }
        // Ensure axios.post is a mock function for Vitest
        ;(axios.post as unknown as any).mockResolvedValue(mockResponse)

        const patientData = {
            alter: 45,
            geschlecht: 'w'
        }
        const result = await patientApi.predict(patientData)
        expect(result.probability).toBe(0.85)
    })

    test('behandelt API-Fehler korrekt', async () => {
        ;(axios.post as unknown as any).mockRejectedValue(new Error('API Error'))
        await expect(patientApi.predict({})).rejects.toThrow('API Error')
    })
})
