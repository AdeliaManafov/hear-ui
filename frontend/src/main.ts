import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import {vuetify} from './plugins/vuetify'
import 'vuetify/styles'

const app = createApp(App)

app.use(router)
app.use(vuetify) // 👈 register Vuetify globally

app.mount('#app')
