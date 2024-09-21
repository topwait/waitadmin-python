import { defineStore } from 'pinia'
import { popupEnum } from '~/enums/app'
import appApi from '~/api/app'

interface AppSate {
    popupType: popupEnum,
    config: Record<string, any>
}

const useAppStore = defineStore({
    id: 'appStore',
    state: (): AppSate => ({
        popupType: popupEnum.NULL,
        config: {}
    }),
    getters: {
        getRechargeConfig: (state: AppSate) => state.config.recharge || {},
        getWebsiteConfig: (state: AppSate) => state.config.website || {},
        getLoginConfig: (state: AppSate) => state.config.login || {},
        getPcConfig: (state: AppSate) => state.config.pc || {}
    },
    actions: {
        /**
         * 获取全局配置
         */
        async getConfig(): Promise<any> {
            this.config = await appApi.config()
        },
        /**
         * 设置显示弹窗
         */
        setPopup(type: popupEnum): void {
            this.popupType = type
        }
    }
})

export default useAppStore
