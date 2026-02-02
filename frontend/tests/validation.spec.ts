import { validatePatientData } from '@/utils/validation'

describe('Validierung', () => {
    test('erkennt ungültige Alterswerte', () => {
        expect(validatePatientData({ alter: -1 })).toBeFalsy()
        expect(validatePatientData({ alter: 150 })).toBeFalsy()
        expect(validatePatientData({ alter: 45 })).toBeTruthy()
    })

    test('validiert Geschlechtsangabe', () => {
        expect(validatePatientData({ geschlecht: 'x' })).toBeFalsy()
        expect(validatePatientData({ geschlecht: 'w' })).toBeTruthy()
        expect(validatePatientData({ geschlecht: 'm' })).toBeTruthy()
    })
})