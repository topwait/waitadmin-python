import type { RouteLocationNormalized } from 'vue-router'
import { popupEnum } from '~/enums/app'
import useAppStore from '~~/stores/app'
import useUserStore from '~~/stores/user'
import validateUtil from '~~/utils/validate'

export default defineNuxtRouteMiddleware(async (to: RouteLocationNormalized, from: RouteLocationNormalized) => {
    const appStore = useAppStore()
    const userStore = useUserStore()

    try {
        if (validateUtil.isEmptyObject(appStore.config)) {
            await appStore.getConfig()
        }

        if (validateUtil.isEmptyObject(userStore.users)) {
            if (userStore.isLogin) {
                await userStore.getUser()
            }
        }

        if (to.meta.auth && !userStore.isLogin) {
            if (from.meta.auth) {
                return navigateTo({
                    replace: true,
                    path: '/'
                })
            }
            appStore.setPopup(popupEnum.LOGIN)
            return abortNavigation()
        }
    } catch (error) {
        console.error(error)
        userStore.$reset()
    }
})