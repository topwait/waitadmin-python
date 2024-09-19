import { defineStore } from 'pinia'
import { isObject } from '@vue/shared'
import { cacheEnum } from '~/enums/cache'
import cacheUtil from '~/utils/cache'
import themeUtil from '~/utils/theme'
import defaultSetting from '~/config/setting'

export const useConfStore = defineStore({
    id: 'conf',
    state: () => {
        const cacheSetting: object = cacheUtil.get(cacheEnum.SETTING_KEY)
        const state: any = {
            settingShow: false,
            ...defaultSetting
        }

        if (isObject(cacheSetting)) {
            Object.assign(state, cacheSetting)
        }
        return state
    },
    actions: {
        /**
         * 修改配置
         */
        setSetting(data: Record<string, any>): void {
            const { key, value } = data
            if (key in this) {
                this[key] = value
            }
            const settings: any = Object.assign({}, this.$state)
            delete settings.settingShow
            cacheUtil.set(cacheEnum.SETTING_KEY, settings)
        },
        /**
         * 修改主题
         */
        setTheme(color: string, dark: boolean): void {
            this.primaryTheme = color
            themeUtil.setTheme({
                primary: color,
                success: this.successTheme,
                warning: this.warningTheme,
                danger: this.dangerTheme,
                error: this.errorTheme,
                info: this.infoTheme
            }, dark)

            watchEffect((): void => {
                document.documentElement.className = dark ? ' dark' : ''
            })
        }
    }
})

export default useConfStore
