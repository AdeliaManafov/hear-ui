import { createPinia, setActivePinia } from 'pinia'
import { usePatientStore } from '@/stores/patient'

describe('Patient Store', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
    })

    test('speichert Patientendaten', () => {
        const store = usePatientStore()
        const patientData = {
            alter: 45,
            geschlecht: 'w'
        }
        store.setPatientData(patientData)
        expect(store.currentPatient).toEqual(patientData)
    })

    test('löscht Patientendaten', () => {
        const store = usePatientStore()
        store.clearPatientData()
        expect(store.currentPatient).toBeNull()
    })
})
