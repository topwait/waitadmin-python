import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'url'
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import vueSetupExtend from 'vite-plugin-vue-setup-extend'

// https://vitejs.dev/config/
export default defineConfig({
    // 公共基础路径
    base: '/admin/',

    // 开发服务配置
    server: {
        host: '0.0.0.0',
        port: 5173
    },

    plugins: [
        // Vue官方插件
        vue(),

        // API自动导入
        AutoImport({
            imports: ['vue', 'vue-router'],
            resolvers: [ElementPlusResolver()],
            eslintrc: {
                enabled: true
            }
        }),

        // 按需引入组件
        Components({
            directoryAsNamespace: true,
            resolvers: [ElementPlusResolver()]
        }),

        // SVG图标插件
        createSvgIconsPlugin({
            iconDirs: [fileURLToPath(new URL('./src/assets/icons', import.meta.url))],
            symbolId: 'svg-icon-[dir]-[name]'
        }),

        //  Vue setup语法扩展
        vueSetupExtend()
    ],

    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    }
})
