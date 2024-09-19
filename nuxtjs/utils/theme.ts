import colors from 'css-color-function'

const lightConfig: any = {
    'dark-2': 'shade(20%)',
    'light-3': 'tint(30%)',
    'light-5': 'tint(50%)',
    'light-7': 'tint(70%)',
    'light-8': 'tint(80%)',
    'light-9': 'tint(90%)'
}

const darkConfig: any = {
    'light-3': 'shade(20%)',
    'light-5': 'shade(30%)',
    'light-7': 'shade(50%)',
    'light-8': 'shade(60%)',
    'light-9': 'shade(70%)',
    'dark-2': 'tint(20%)'
}

const themeId: string = 'theme-vars'

const themeUtil = {
    /**
     * 生成变量
     * 可选值: [primary, success, warning, danger, error, info]
     *
     * @param {string} color   十六进制颜色
     * @param {string} type    颜色类型
     * @param {boolean} isDark 暗黑模式
     * @returns objects
     */
    generateVars(color: string, type: string = 'primary', isDark: boolean = false) {
        const colors: any = {
            [`--el-color-${type}`]: color
        }
        const config: Record<string, string> = isDark ? darkConfig : lightConfig
        for (const key in config) {
            colors[`--el-color-${type}-${key}`] = `color(${color} ${config[key]})`
        }
        return colors
    },

    /**
     * 生成主题
     *
     * @param {Record<string, string>} options
     * @param {boolean} isDark
     * @returns {string}
     */
    generateTheme(options: Record<string, string>, isDark: boolean = false): string {
        const varsMap: Record<string, string> = Object.keys(options).reduce((prev: any, key: string) => {
            return Object.assign(prev, this.generateVars(options[key], key, isDark))
        }, {})

        return Object.keys(varsMap).reduce((prev: string, key: string): string => {
            const color = colors.convert(varsMap[key])
            return `${prev}${key}:${color};`
        }, '')
    },

    /**
     * 设置主题
     *
     * @param {Record<string, string>} options
     * @param {isDark} isDark
     * @returns {void}
     */
    setTheme(options: Record<string, string>, isDark: boolean = false): void {
        const theme: string = this.generateTheme(options, isDark)
        const themeElem: string = `:root{${theme}}`
        let style: HTMLElement | null = document.getElementById(themeId)
        if (style) {
            style.innerHTML = themeElem
            return
        }
        style = document.createElement('style')
        style.setAttribute('type', 'text/css')
        style.setAttribute('id', themeId)
        style.innerHTML = themeElem
        document.head.append(style)
    }
}

export default themeUtil
