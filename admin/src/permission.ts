import { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import router, { layoutRouter, firstValidRoute } from './router'
import { pageEnum } from '@/enums/page'
import useUserStore from './stores/modules/user'
import useTabsStore from './stores/modules/tabs'
import validateUtil from '@/utils/validate'
import config from './config'

const whiteList: string[] = [
    pageEnum.LOGIN,
    pageEnum.ERROR_403
]

router.beforeEach(async (to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext): Promise<any> => {
    const userStore = useUserStore()
    const tabsStore = useTabsStore()

    document.title = String(to.meta.title ?? config.title)

    if (whiteList.includes(to.path)) {
        next()
    } else if (userStore.token) {
        const hasGetUserInfo: boolean = Object.keys(userStore.users || {}).length !== 0
        if (hasGetUserInfo) {
            if (to.path === pageEnum.LOGIN) {
                next({ path: pageEnum.INDEX })
            }
            next()
        } else {
            try {
                await userStore.getUserInfo()
                const routes = userStore.routes
                const routeName: string | undefined = firstValidRoute(routes)
                if (!routeName) {
                    userStore.resetState()
                    tabsStore.resetState()
                    return next(pageEnum.ERROR_403)
                }

                tabsStore.setCurrRouteName(routeName)
                layoutRouter.redirect = { name: routeName }

                router.addRoute(layoutRouter)
                routes.forEach((route: any): void => {
                    if (validateUtil.isExternal(route.path)) {
                        return
                    }
                    if (!route.children) {
                        const name: any = layoutRouter.name
                        router.addRoute(name, route)
                        return
                    }
                    router.addRoute(route)
                })

                return next({ ...to, replace: true })
            } catch (err) {
                return next({ path: pageEnum.LOGIN, query: { redirect: to.fullPath } })
            }
        }
    } else {
        return next({ path: pageEnum.LOGIN, query: { redirect: to.fullPath } })
    }
})
