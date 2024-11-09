<template>
    <ElConfigProvider>
        <NuxtLoadingIndicator color="#0f70d8" :height="2" />
        <NuxtPage />
    </ElConfigProvider>
</template>

<script setup lang="ts">
import { ID_INJECTION_KEY, ElConfigProvider } from 'element-plus'
import useAppStore from './stores/app'
import useConfStore from './stores/conf'

const appStore = useAppStore()
const confStore = useConfStore()
const pcConfig = appStore.getPcConfig
const websiteConfig = appStore.getWebsiteConfig

confStore.setTheme(
    confStore.primaryTheme,
    confStore.isDarkColor
)

provide(ID_INJECTION_KEY, {
    prefix: 100,
    current: 0
})

useHead({
    title: pcConfig.title,
    link: [
        {
            rel: 'icon',
            href: pcConfig.favicon
        }
    ],
    meta: [
        {
            name: 'keywords',
            content: pcConfig.keywords
        },
        {
            name: 'description',
            content: pcConfig.description
        }
    ],
    script: websiteConfig.analyse ? [{src: websiteConfig.analyse}] : []
})
</script>
