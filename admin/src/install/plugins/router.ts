import type { App } from 'vue'
import router from '@/router'
import createInitGuard from '@/router/guard'

export default (app: App<Element>): void => {
    createInitGuard(router)
    app.use(router)
}
