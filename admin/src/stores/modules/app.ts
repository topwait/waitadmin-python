import { defineStore } from 'pinia'
import appApi from '@/api/app'

interface AppSate {
    config: Record<string, any>,
    isMobile: boolean,
    isRouteShow: boolean,
    isCollapsed: boolean,
    layoutHeight: number,
}

const useAppStore = defineStore({
    id: 'app',
    state: (): AppSate => ({
        config: {},
        isMobile: true,
        isRouteShow: true,
        isCollapsed: false,
        layoutHeight: 0
    }),
    getters: {

    },
    actions: {
        /**
         * 获取系统配置
         */
        getConfig() {
            return new Promise((resolve, reject): void => {
                appApi.config()
                    .then((data: any): void => {
                        this.config = data
                        resolve(data)
                    })
                    .catch((err: any): void => {
                        reject(err)
                    })
            })
        },
        /**
         * 设置手机模式
         */
        setMobile(value: boolean): void {
            this.isMobile = value
        },
        /**
         * 设置菜单伸缩
         */
        toCollapsed(toggle?: boolean): void {
            this.isCollapsed = toggle ?? !this.isCollapsed
        },
        /**
         * 刷新页面数据
         */
        refreshView(): void {
            this.isRouteShow = false
            nextTick((): void => {
                this.isRouteShow = true
            }).then((): void => { })
        }
    }
})

export default useAppStore
