import request from '@/utils/request'

const loginApi = {
    /**
     * 验证码
     */
    captcha(): Promise<any> {
        return request.get({
            url: '/login/captcha'
        })
    },

    /**
     * 登录系统
     */
    login(params: any): Promise<any> {
        return request.post({
            url: '/login/check',
            params
        })
    },

    /**
     * 退出系统
     */
    logout(): Promise<any> {
        return request.post({
            url: '/login/logout'
        })
    }
}

export default loginApi
