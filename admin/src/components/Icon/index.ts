// @ts-ignore
import localIconsName from 'virtual:svg-icons-names'
import * as ElementPlusIcons from '@element-plus/icons-vue'

export const EL_ICON_PREFIX: string = 'el-icon-'
export const SVG_ICON_PREFIX: string = 'svg-icon-'

const elIconsName: string[] = []

for (const [, component] of Object.entries(ElementPlusIcons)) {
    elIconsName.push(`${EL_ICON_PREFIX}${component.name}`)
}

export function getElementIconNames() {
    return elIconsName
}

export function getLocalIconNames() {
    return localIconsName
}
