// https://nuxt.com/docs/api/configuration/nuxt-config
import { loadEnv } from 'vite'

const envData = loadEnv(process.env.NODE_ENV!, './')

export default defineNuxtConfig({
    devtools: {
        enabled: true
    },

    ssr: !!envData.VITE_SSR,
    spaLoadingTemplate: false,

    css: ['@/assets/styles/index.scss'],

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

    runtimeConfig: {
        public: {
            ...envData
        }
    },

    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    api: 'modern-compiler'
                }
            }
        },
        plugins: [
            {
                name: 'vite-plugin-glob-transform',
                transform(code: string, id: string) {
                    if (id.includes('nuxt-icons')) {
                        return code.replace(/as:\s*['"]raw['"]/g, 'query: "?raw", import: "default"')
                    }
                    return code
                }
            }
        ]
    },

    compatibilityDate: '2024-09-19'
})