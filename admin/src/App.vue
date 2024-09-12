<template>
    <el-config-provider :locale="elConfig.locale" :z-index="elConfig.zIndex">
        <router-view />
    </el-config-provider>
</template>

<script setup lang="ts">
import { useWindowSize, useThrottleFn } from '@vueuse/core'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import useAppStore from './stores/modules/app'
import useConfStore from './stores/modules/conf'

const appStore = useAppStore()
const confStore = useConfStore()

const elConfig = {
    zIndex: 3000,
    locale: zhCn
}

// 主题设置
confStore.setTheme(
    confStore.theme,
    confStore.primaryTheme,
    confStore.isDarkColor
)

// 适配宽度
const { width } = useWindowSize()
watch(
    width,
    useThrottleFn((value) => {
        const SM = 640
        const MD = 768
        if (value > SM) {
            appStore.setMobile(false)
            appStore.toCollapsed(false)
        } else {
            appStore.setMobile(true)
            appStore.toCollapsed(true)
        }
        if (value < MD) {
            appStore.toCollapsed(true)
        }
    }),
    {
        immediate: true
    }
)
</script>
