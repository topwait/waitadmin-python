import { createApp } from 'vue'
import App from './App.vue'
import Install from './install'
import './permission'
import './assets/styles/index.scss'
import 'virtual:svg-icons-register'
import 'default-passive-events'

const app = createApp(App)

app.use(Install)
app.mount('#app')
