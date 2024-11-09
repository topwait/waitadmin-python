import { RouteRecordRaw, RouterView, createRouter, createWebHistory, RouteRecordName, Router } from 'vue-router'
import useUserStore from '@/stores/modules/user'
import validateUtil from '@/utils/validate'
import Layout from '@/layout/index.vue'

// 读取视图模块
const modules: Record<string, any> = import.meta.glob('/src/views/**/*.vue')

// 定义布局路由
export const INDEX_ROUTE_NAME = Symbol()
export const layoutRouter: RouteRecordRaw = {
    path: '/',
    component: Layout,
    name: INDEX_ROUTE_NAME
}

/**
 * 获取视图模块
 *
 * @returns {string[]}
 * @author zero
 */
export function getModulesKey(): string[] {
    return Object.keys(modules).map((item: string) => item
        .replace('/src/views/', '')
        .replace('.vue', ''))
}

/**
 * 过滤路由参数
 *
 * @param {any[]} routes
 * @param {boolean} firstRoute
 * @author zero
 */
export function filterRoutes(routes: any[], firstRoute: boolean = true): RouteRecordRaw[] {
    return routes.map((route) => {
        // @ts-ignore
        const routeRecord: RouteRecordRaw = {
            path: validateUtil.isExternal(route.path) ? route.path : firstRoute ? `/${route.path}` : route.path,
            name: Symbol(route.path),
            meta: {
                type: route.type,
                icon: route.icon,
                title: route.name,
                perms: route.perms,
                query: route.params,
                hidden: !route.is_show
            }
        }

        switch (route.type) {
            case 'M':
                routeRecord.component = firstRoute ? markRaw(Layout) : markRaw(RouterView)
                if (!route.children) {
                    routeRecord.component = RouterView
                }
                break
            case 'C':
                routeRecord.component = dynamicViews(route.component)
                break
        }

        if (route.children !== null && route.children && route.children.length) {
            routeRecord.children = filterRoutes(route.children, false)
        }

        return routeRecord
    })
}

/**
 * 动态加载视图
 *
 * @param {string} component
 * @returns RouterView
 * @author zero
 */
export function dynamicViews(component: string) {
    const key: string | undefined = Object.keys(modules).find((key: string) => {
        return key.includes(`${component}.vue`)
    })

    if (key) {
        return modules[key]
    }

    // eslint-disable-next-line no-console
    console.error(`找不到组件${component},请确保组件路径正确`)
    return RouterView
}

/**
 * 首个有效路由
 *
 * @param {RouteRecordRaw[]} routes
 * @returns {string | undefined}
 * @author zero
 */
export function firstValidRoute(routes: RouteRecordRaw[]): string | undefined {
    for (const route of routes) {
        if (route.meta?.type === 'C' && !route.meta?.hidden && !validateUtil.isExternal(route.path)) {
            return route.name as string
        }
        if (route.children) {
            const name: string | undefined = firstValidRoute(route.children)
            if (name) {
                return name
            }
        }
    }
}

/**
 * 重置路由数据
 *
 * @returns {void}
 * @author zero
 */
export function resetRouter(): void {
    router.removeRoute(INDEX_ROUTE_NAME)
    const { routes } = useUserStore()
    routes.forEach((route: RouteRecordRaw): void => {
        const name: RouteRecordName | undefined = route.name
        if (name && router.hasRoute(name)) {
            router.removeRoute(name)
        }
    })
}

/**
 * 创建默认路由
 *
 * @returns {Router}
 * @author zero
 */
const router: Router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/:pathMatch(.*)*',
            component: () => import('@/views/error/404.vue')
        },
        {
            path: '/403',
            component: () => import('@/views/error/403.vue')
        },
        {
            path: '/login',
            component: () => import('@/views/login.vue')
        },
        {
            path: '/auth/account',
            component: Layout,
            children: [
                {
                    path: 'setting',
                    component: () => import('@/views/auth/admin/setting.vue'),
                    name: Symbol(),
                    meta: {
                        title: '个人设置'
                    }
                }
            ]
        }
    ]
})

export default router
