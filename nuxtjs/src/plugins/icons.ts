import * as ElementPlusIcons from '@element-plus/icons-vue'

export const EL_ICON_PREFIX: string = 'el-icon-'
export const SVG_ICON_PREFIX: string = 'svg-icon-'

export default defineNuxtPlugin((nuxtApp): void => {
    for (const [iconName, component] of Object.entries(ElementPlusIcons)) {
        const componentName: string = `${EL_ICON_PREFIX}${iconName}`
        nuxtApp.vueApp.component(componentName, component)
    }
})
