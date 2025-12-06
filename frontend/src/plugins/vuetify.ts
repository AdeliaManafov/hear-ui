// src/plugins/vuetify.ts
import 'vuetify/styles'
import {createVuetify} from 'vuetify'
import {aliases, mdi} from 'vuetify/iconsets/mdi'
import {lightTheme} from './theme'

export const vuetify = createVuetify({
    icons: {
        defaultSet: 'mdi',
        aliases,
        sets: {mdi},
    },
    theme: {
        defaultTheme: 'light',
        themes: {
            light: lightTheme,
        },
    },
})
