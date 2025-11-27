import request from '@/utils/request'

const loginApi = {
    /**
     * 验证码
     */
    captcha(): Promise<LoginCaptchaResponse> {
        return request.get<LoginCaptchaResponse>({
            url: '/login/captcha'
        })
    },

    /**
     * 登录系统
     *
     * @param {Object} params
     * @param {string} params.username
     * @param {string} params.password
     * @param {string} [params.uuid]
     * @param {string} [params.code]
     */
    login(params: {
        username: string;
        password: string;
        uuid?: string;
        code?: string;
    }): Promise<LoginSuccessResponse> {
        return request.post<LoginSuccessResponse>({
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
