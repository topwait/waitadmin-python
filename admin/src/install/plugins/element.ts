import type { App } from 'vue'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'

export default (app: App<Element>): void => {
    for (const [key, component] of Object.entries(ElementPlusIcons)) {
        app.component(key, component)
    }
}
