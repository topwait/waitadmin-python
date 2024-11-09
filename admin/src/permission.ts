import { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import router, { layoutRouter, INDEX_ROUTE_NAME, firstValidRoute } from './router'
import { pageEnum } from '@/enums/page'
import useUserStore from './stores/modules/user'
import useTabsStore from './stores/modules/tabs'
import validateUtil from '@/utils/validate'
import config from './config'

// 免登录白名单
const whiteList: string[] = [
    pageEnum.LOGIN,
    pageEnum.ERROR_403
]

// 递归动态路由
const addRoutesRecursively = (routes: any, parentPath = '') => {
    try {
        routes.forEach((route: any) => {
            // 如果路由是外部链接则不添加
            if (validateUtil.isExternal(route.path)) {
                return
            }

            // 拼接父路由路径和当前路由路径
            const fullPath = parentPath + route.path

            // 创建路由对象确保路由的唯一性
            const routerEntry = {
                ...route,
                path: fullPath,
                name: route.name || fullPath.replace(/\//g, '_').replace('_', '')
            }

            // 添加注册路由
            if (!route.children) {
                router.addRoute(INDEX_ROUTE_NAME, routerEntry)
            } else {
                router.addRoute(routerEntry)
            }

            // 递归处理子路由
            if (route.children && route.children.length > 0) {
                addRoutesRecursively(route.children, fullPath + '/')
            }
        })
    } catch (e) {
        // eslint-disable-next-line no-console
        console.error('Error adding routes:', e)
    }
}

// 路由前置拦截
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
                addRoutesRecursively(routes)

                return next({ ...to, replace: true })
            } catch {
                return next({ path: pageEnum.LOGIN, query: { redirect: to.fullPath } })
            }
        }
    } else {
        return next({ path: pageEnum.LOGIN, query: { redirect: to.fullPath } })
    }
})
