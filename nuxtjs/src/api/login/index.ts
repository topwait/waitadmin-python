const loginApi = {
    /**
     * 注册账号
     *
     * @param {Object} params
     * @param {number} params.scene - 注册场景[mobile=手机, email=邮箱]
     * @param {string} params.code - 验证码
     * @param {string} params.account - 账号
     * @param {string} params.password - 密码
     * @returns {Promise<LoginResultResponse>}
     * @author zero
     */
    register(params: {
        scene: string,
        code: string,
        account: string,
        password: string
    }): Promise<LoginResultResponse> {
        return $request.post<LoginResultResponse>({
            url: '/login/register',
            params
        })
    },

    /**
     * 登录系统
     *
     * @param {Object} params
     * @param {string} params.scene - 登录场景[mobile=手机, account=账号]
     * @param {string} params.code - 验证码
     * @param {string} params.mobile - 手机号[可选]
     * @param {string} params.account - 登录账号[可选]
     * @param {string} params.password - 登录密码[可选]
     * @returns {Promise<LoginResultResponse>}
     * @author zero
     */
    login(params: any): Promise<LoginResultResponse> {
        switch (params.scene) {
            case 'mobile':
                return $request.post<LoginResultResponse>({
                    url: '/login/mobile_login',
                    params: {
                        scene: params.scene,
                        mobile: params.mobile,
                        code: params.code
                    }
                })
            default:
                return $request.post<LoginResultResponse>({
                    url: '/login/account_login',
                    params: {
                        scene: params.scene,
                        account: params.account,
                        password: params.password
                    }
                })
        }
    },

    /**
     * 退出登录
     *
     * @returns {Promise<any>}
     * @author zero
     */
    logout(): Promise<any> {
        return $request.post({
            url: '/login/logout'
        })
    },

    /**
     * 公众号登录
     *
     * @param {Object} params
     * @param {string} params.state - 验证密钥
     * @param {string} params.code - 微信code
     * @returns {Promise<LoginResultResponse>}
     * @author zero
     */
    oaLogin(params: { state: string, code: string }): Promise<LoginResultResponse> {
        return $request.post<LoginResultResponse>({
            url: '/login/oa_login',
            params
        })
    },

    /**
     * 公众号登录二维码
     *
     * @param {string} event - 事件[login=登录,bind=绑定]
     * @returns {Promise<LoginQrcodeResponse>}
     * @author zero
     */
    oaLoginQr(event: string): Promise<LoginQrcodeResponse> {
        return $request.get<LoginQrcodeResponse>({
            url: '/login/qrcode',
            params: { event }
        })
    },

    /**
     * 公众号登录的检测
     *
     * @param {string} state - 验证密钥
     * @returns {Promise<LoginTicketResponse>}
     * @author zero
     */
    oaTicket(state: string): Promise<LoginTicketResponse> {
        return $request.get<LoginTicketResponse>({
            url: '/login/ticket',
            params: { state }
        })
    }
}

export default loginApi
