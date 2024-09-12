import type { Router } from 'vue-router'
import useAppStore from '@/stores/modules/app'
import FaviconIco from '@/assets/images/favicon.ico'

export default function createInitGuard(router: Router): void {
    router.beforeEach(async (): Promise<void> => {
        const appStore = useAppStore()
        if (Object.keys(appStore.config).length === 0) {
            await appStore.getConfig()
            document.title = appStore.config.title
            let favicon: HTMLLinkElement = document.querySelector('link[rel="icon"]')!
            if (favicon) {
                favicon.href = FaviconIco
            }
            favicon = document.createElement('link')
            favicon.rel = 'icon'
            document.head.appendChild(favicon)
        }
    })
}
