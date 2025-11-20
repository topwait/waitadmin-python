## 环境配置
**开发环境配置(一): 复制`.env.template.development` 为 `.env.development`**
```shell
# 当你运行 `pnpm run dev` 时使用这里的配置
NODE_ENV='development'
VITE_APP_BASE_URL='http://0.0.0.0:8100' # 配置服务端接口地址
```

**生产环境配置(一): 复制`.env.template.production` 为 `.env.production`**
```shell
# 当你运行 `pnpm build` 时使用这里的配置
NODE_ENV='production'
VITE_APP_BASE_URL='https://www.baid.com.com'
```

## 安装依赖
> 您可以使用 `npm`、`pnpm` 管理您的依赖包 建议使用 `pnpm`
```shell
# 安装依赖
pnpm install

# 开发运行
pnpm run dev

# 项目打包
pnpm build
```

##  生产依赖 (dependencies)
| 依赖名称                         | 作用                  |
|------------------------------|---------------------|
| `@element-plus/icons-vue`    | Element Plus 的图标库   | 
| `@vue/shared`                | Vue 共享工具函数          | 
| `@vueuse/core`               | Vue 组合式 API 工具集     | 
| `@wangeditor/editor`         | 富文本编辑器核心            |
| `@wangeditor/editor-for-vue` | 富文本编辑器的 Vue 封装      |
| `axios`                      | HTTP 请求库            | 
| `css-color-function`         | CSS 颜色处理函数          | 
| `default-passive-events`     | 解决触摸事件警告            |
| `echarts`                    | 图表库                 | 
| `element-plus`               | UI 组件库              |
| `lodash-es`                  | 实用工具库（如 `merge` 函数） | 
| `nprogress`                  | 进度条                 | 
| `pinia`                      | 状态管理                | 
| `vue`                        | 前端框架（项目核心）          | 
| `vue-clipboard3`             | 剪贴板功能               | 
| `vue-cropper`                | 图片裁剪                |
| `vue-echarts`                | Vue 的 ECharts 封装    | 
| `vue-router`                 | 路由管理                | 
| `vue3-video-play`            | 视频播放器               | 
| `vuedraggable`               | 拖拽排序                | 


## 开发依赖 (devDependencies)
| 依赖名称                               | 作用                        |
|------------------------------------|---------------------------|
| `@tailwindcss/postcss`             | Tailwind CSS 的 PostCSS 插件 |
| `@types/lodash-es`                 | lodash-es 的类型定义           |
| `@types/node`                      | Node.js 的类型定义             |
| `@types/nprogress`                 | nprogress 的类型定义           |
| `@typescript-eslint/eslint-plugin` | TypeScript 的 ESLint 插件    |
| `@typescript-eslint/parser`        | TypeScript 的 ESLint 解析器   |
| `@vitejs/plugin-vue`               | Vite 的 Vue 插件             |
| `consola`                          | 控制台日志工具                   |
| `eslint`                           | 代码检查工具                    |
| `eslint-plugin-vue`                | Vue 的 ESLint 插件           |
| `fs-extra`                         | 文件系统扩展                    |
| `jiti`                             | 运行时 TypeScript 解释器        |
| `postcss`                          | CSS 转换工具                  |
| `sass`                             | CSS 预处理器                  |
| `stylelint`                        | 样式检查工具                    |
| `stylelint-config-recess-order`    | Stylelint 配置（CSS 属性顺序）    |
| `stylelint-config-recommended-vue` | Vue 的 Stylelint 配置        |
| `stylelint-config-standard-scss`   | SCSS 的 Stylelint 配置       |
| `tailwindcss`                      | 原子化 CSS 框架                |
| `typescript`                       | TypeScript 编译器            |
| `unplugin-auto-import`             | 自动导入 API                  |
| `unplugin-vue-components`          | 组件自动导入                    |
| `vite`                             | 构建工具                      |
| `vite-plugin-svg-icons`            | SVG 图标插件                  |
| `vite-plugin-vue-setup-extend`     | Vue setup 语法扩展            |
| `vue-eslint-parser`                | Vue 的 ESLint 解析器          |
| `vue-tsc`                          | Vue TypeScript 检查器        |