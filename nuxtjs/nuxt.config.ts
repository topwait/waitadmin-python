// https://nuxt.com/docs/api/configuration/nuxt-config
import { getEnvConfig } from './nuxt/env'

const envConfig: Record<string, any> = getEnvConfig()

export default defineNuxtConfig({
    devtools: { enabled: true },
    ssr: !!envConfig.ssr,
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
        baseURL: envConfig.baseUrl
    },

    runtimeConfig: {
        public: {
            ...envConfig
        }
    },

    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    api: 'modern-compiler'
                }
            }
        }
    },

    compatibilityDate: '2024-09-19'
})