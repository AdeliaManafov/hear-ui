import { describe, test, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import PatientForm from '@/components/PatientForm.vue'

describe('PatientForm', () => {
    test('validiert erforderliche Felder', async () => {
        const wrapper = mount(PatientForm)
        const submitButton = wrapper.find('[data-test="submit-button"]')
        await submitButton.trigger('click')
        expect(wrapper.find('[data-test="error-message"]')).toBeTruthy()
    })

    test('sendet Formulardaten korrekt', async () => {
        const wrapper = mount(PatientForm)
        // Formular ausfüllen (setValue expects string for input elements)
        await wrapper.find('[data-test="alter"]').setValue('45')
        await wrapper.find('[data-test="geschlecht"]').setValue('w')
        await wrapper.find('[data-test="submit-button"]').trigger('click')
        // wait for emission
        await nextTick()
        expect(wrapper.emitted().submit).toBeTruthy()
    })
})

// frontend/tests/components/PredictionResult.spec.ts
import { mount as mount2 } from '@vue/test-utils'
import PredictionResult from '@/components/PredictionResult.vue'

describe('PredictionResult', () => {
    test('zeigt Vorhersageergebnis korrekt an', () => {
        const prediction = {
            probability: 0.85,
            top_features: [
                { feature: 'Alter', importance: 0.3 }
            ]
        }
        const wrapper = mount2(PredictionResult, {
            props: { prediction }
        })
        expect(wrapper.text()).toContain('85%')
    })
})