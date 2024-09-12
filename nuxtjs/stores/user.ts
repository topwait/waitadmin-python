import type { Router } from 'vue-router'
import { defineStore } from 'pinia'
import { cacheEnum } from '~/enums/cache'
import cacheUtil from '@/utils/cache'
import loginApi from '~/api/login'
import userApi from '~/api/user'

interface UserSate {
    token: string | null,
    users: UserCenterResponse
}

const useUserStore = defineStore({
    id: 'userStore',
    state: (): UserSate => {
        return {
            token: cacheUtil.get(cacheEnum.TOKEN_KEY) || '',
            users: {} as UserCenterResponse,
        }
    },
    getters: {
        isLogin: (state: UserSate) => !!state.token
    },
    actions: {
        /**
         * 获取用户
         */
        async getUser(): Promise<UserCenterResponse> {
            this.users = await userApi.center()
            return this.users
        },
        /**
         * 登录系统
         */
        login(token: string): void {
            this.token = token
            cacheUtil.set(cacheEnum.TOKEN_KEY, token)
        },
        /**
         * 退出系统
         */
        async logout(): Promise<any> {
            const router: Router = useRouter()
            return new Promise((resolve, reject): void => {
                loginApi.logout().then((data: any): void => {
                    cacheUtil.remove(cacheEnum.TOKEN_KEY)
                    this.token = ''
                    this.users = {} as UserCenterResponse
                    router.push('/')
                    resolve(data)
                }).catch((error: any): void => {
                    reject(error)
                })
            })
        }
    }
})

export default useUserStore
