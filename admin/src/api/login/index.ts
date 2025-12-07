import request from '@/utils/request'

const loginApi = {
    /**
     * 验证码
     *
     * @returns {LoginCaptchaResponse}
     * @author zero
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
     * @returns {LoginSuccessResponse}
     * @author zero
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
     *
     * @returns {any}
     * @author zero
     */
    logout(): Promise<any> {
        return request.post({
            url: '/login/logout'
        })
    }
}

export default loginApi
