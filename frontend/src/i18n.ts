import i18next from 'i18next'
import I18NextVue from 'i18next-vue'
import LanguageDetector from 'i18next-browser-languagedetector'
import {App} from "vue";

i18next
    // detect user language
    // learn more: https://github.com/i18next/i18next-browser-languageDetector
    .use(LanguageDetector)
    // init i18next
    // for all options read: https://www.i18next.com/overview/configuration-options
    .init({
        debug: false,
        fallbackLng: 'de',
        resources: {
            de: {
                translation: {
                    navbar_homepage: 'Startseite',
                    navbar_search_patients: 'Patient:innen suchen',
                    navbar_create_patient: 'Patient:in anlegen',
                    navbar_predictions: 'Vorhersage durchführen'
                }
            },
            en: {
                translation: {
                    navbar_homepage: 'Homepage',
                    navbar_search_patients: 'Search patients',
                    navbar_create_patient: 'Add new patient',
                    navbar_predictions: 'Predictions'
                }
            }
        }
    });

export default function installI18n(app: App) {
    app.use(I18NextVue, {i18next})
    return app
}