import store from '@/stores'
import type { App } from 'vue'

export default (app: App<Element>): void => {
    app.use(store)
}
