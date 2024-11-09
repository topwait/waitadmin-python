const config = {
    // 网站标题
    title: 'Wa后台管理系统',
    // 版本编号
    version: '1.1.1',
    // 请求域名
    baseUrl: `${import.meta.env.VITE_APP_BASE_URL || ''}`,
    // 请求前缀
    urlPrefix: '/spi',
    // 请求超时
    timeout: 10 * 1000
}

export default config
