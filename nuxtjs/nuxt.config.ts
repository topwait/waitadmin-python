// https://nuxt.com/docs/api/configuration/nuxt-config
import { loadEnv } from 'vite'

const envData: Record<string, string> = loadEnv(process.env.NODE_ENV!, './')

export default defineNuxtConfig({
    devtools: {
        enabled: true
    },

    ssr: !!envData.VITE_SSR,

    spaLoadingTemplate: false,

    css: [
        '@/assets/styles/index.scss'
    ],

    modules: [
        'nuxt-icons',
        '@pinia/nuxt',
        '@nuxt/eslint',
        '@nuxtjs/tailwindcss',
        '@element-plus/nuxt'
    ],

    elementPlus: {
        defaultLocale: 'zh-cn'
    },

    eslint: {
        checker: true
    },

    app: {
        baseURL: envData.VITE_BASE_URL
    },

    devServer: {
        port: parseInt(envData.VITE_PORT || '3000'),
        host: String(envData.VITE_HOST || 'localhost')
    },

    runtimeConfig: {
        public: {
            ...envData
        }
    },

    compatibilityDate: '2024-09-19'
})