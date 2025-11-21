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
    debug: true,
    fallbackLng: 'de',
    resources: {
      en: {
        translation: {
          homepage: 'Homepage',
          search_patients: 'Search patients',
          create_patient: 'Add new patient',
          predictions: 'Predictions'
        }
      },
      de: {
        translation: {
          homepage: 'Startseite',
          search_patients: 'Patient:innen suchen',
          create_patient: 'Patient:in anlegen',
          predictions: 'Vorhersage durchführen'
        }
      }
    }
  });

export default function installI18n(app: App) {
  app.use(I18NextVue, { i18next })
  return app
}