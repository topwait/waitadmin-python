// https://nuxt.com/docs/api/configuration/nuxt-config
import { loadEnv } from 'vite'

// 加载环境变量文件
const envData: Record<string, string> = loadEnv(process.env.NODE_ENV!, './')

export default defineNuxtConfig({
    // 源码的目录配置
    srcDir: 'src/',

    // 服务端渲染配置
    ssr: envData.VITE_SSR === 'true',

    // SPA加载模板配置
    spaLoadingTemplate: false,

    // 开发工具配置
    devtools: {
        enabled: envData.VITE_DEV === 'true'
    },

    // 应用基础配置
    app: {
        baseURL: envData.VITE_BASE_URL
    },

    // 开发服务器配置
    devServer: {
        port: parseInt(envData.VITE_PORT || '3000'),
        host: String(envData.VITE_HOST || 'localhost')
    },

    // 运行时环境配置
    runtimeConfig: {
        public: {
            ...envData
        }
    },

    // 全局CSS配置
    css: [
        '@/assets/styles/index.scss'
    ],

    // Nuxt模块配置
    modules: [
        'nuxt-icons',
        '@pinia/nuxt',
        '@nuxt/eslint',
        '@nuxtjs/tailwindcss',
        '@element-plus/nuxt'
    ],

    // Element Plus模块配置
    elementPlus: {
        defaultLocale: 'zh-cn'
    },

    // ESLint模块配置
    eslint: {
        checker: true
    },

    compatibilityDate: '2024-09-19'
})
