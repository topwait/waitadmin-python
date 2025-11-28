import { defineStore } from 'pinia'
import { popupEnum } from '@/enums/app'
import appApi from '@/api/app'

interface AppSate {
    popupType: popupEnum,
    config: AppConfigResponse
}

const useAppStore = defineStore('appStore', {
    state: (): AppSate => ({
        popupType: popupEnum.NULL,
        config: {} as AppConfigResponse
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
        async getConfig(): Promise<AppConfigResponse> {
            this.config = await appApi.config()
            return this.config
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
