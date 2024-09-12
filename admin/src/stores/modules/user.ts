import { RouteRecordRaw } from 'vue-router'
import { defineStore } from 'pinia'
import { cacheEnum } from '@/enums/cache'
import { pageEnum } from '@/enums/page'
import router, { filterRoutes, resetRouter } from '@/router'
import useTabsStore from '@/stores/modules/tabs'
import cacheUtil from '@/utils/cache'
import authAdminApi from '@/api/auth/admin'
import loginApi from '@/api/login'

interface UserSate {
    token: string,
    perms: string[],
    users: Record<string, any>,
    routes: RouteRecordRaw[]
}

const useUserStore = defineStore({
    id: 'user',
    state: (): UserSate => ({
        // 令牌
        token: cacheUtil.get(cacheEnum.TOKEN_KEY) || '',
        // 用户
        users: {},
        // 权限
        perms: [],
        // 路由
        routes: []
    }),
    getters: {

    },
    actions: {
        /**
         * 重置状态
         */
        resetState(): void {
            this.token = ''
            this.users = {}
            this.perms = []
            resetRouter()
            cacheUtil.remove(cacheEnum.TOKEN_KEY)
        },
        /**
         * 登录系统
         */
        login(params: any): Promise<any> {
            return new Promise((resolve, reject): void => {
                loginApi.login({
                    username: params.username,
                    password: params.password,
                    uuid: params.uuid,
                    code: params.code
                }).then((data: any): void => {
                    cacheUtil.set(cacheEnum.TOKEN_KEY, data.token)
                    this.token = data.token
                    resolve(data)
                }).catch((error: any): void => {
                    reject(error)
                })
            })
        },
        /**
         * 退出系统
         */
        logout(): Promise<any> {
            return new Promise((resolve, reject): void => {
                loginApi.logout()
                    .then(async (data: any): Promise<void> => {
                        const tabsStore = useTabsStore()
                        this.resetState()
                        tabsStore.resetState()
                        await router.push(pageEnum.LOGIN)
                        resolve(data)
                    }).catch((error: any): void => {
                        reject(error)
                    })
            })
        },
        /**
         * 获取用户信息
         */
        getUserInfo(): Promise<any> {
            return new Promise((resolve, reject): void => {
                authAdminApi.oneself().then((data: any): void => {
                    this.users = data.user
                    this.perms = data.perms
                    this.routes = filterRoutes(data.menus)
                    resolve(data)
                }).catch((error: any): void => {
                    reject(error)
                })
            })
        }
    }
})

export default useUserStore
