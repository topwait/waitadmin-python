const userApi = {
    /**
     * 个人中心
     *
     * @returns {Promise<UserCenterResponse>}
     * @author zero
     */
    center(): Promise<UserCenterResponse> {
        return $request.get<UserCenterResponse>({
            url: '/user/center'
        })
    },

    /**
     * 我的收藏
     *
     * @param {Object} params
     * @param {number} params.page - 当前页码
     * @returns {Promise<UserCollectResponse>}
     * @author zero
     */
    collect(params: { page?: number }): Promise<UserCollectResponse> {
        return $request.get<UserCollectResponse>({
            url: '/user/collect',
            params: {
                page: params.page
            }
        })
    },

    /**
     * 编辑资料
     *
     * @param {Object} params
     * @param {string} params.field - 要修改字段
     * @param {string} params.value - 要修改的值
     * @returns {Promise<any>}
     * @author zero
     */
    edit(params: { field: string, value: number|string }): Promise<any> {
        return $request.post({
            url: '/user/edit',
            params: {
                field: String(params.field),
                value: String(params.value)
            }
        })
    },

    /**
     * 找回密码
     *
     * @param {Object} params
     * @param {string} params.code - 验证码
     * @param {string} params.account - 账号
     * @param {string} params.password - 新的密码
     * @returns {Promise<any>}
     * @author zero
     */
    forgetPwd(params: { account: string, code: string, password: string }): Promise<any> {
        return $request.post({
            url: '/user/forget_pwd',
            params: {
                code: params.code,
                account: params.account,
                password: params.password
            }
        })
    },

    /**
     * 修改密码
     *
     * @param {Object} params
     * @param {string} params.new_pwd - 新的密码
     * @param {string} params.old_pwd - 旧的密码
     * @returns {Promise<any>}
     * @author zero
     */
    changePwd(params: { new_pwd: string, old_pwd: string }): Promise<any> {
        return $request.post({
            url: '/user/change_pwd',
            params: {
                new_pwd: params.new_pwd,
                old_pwd: params.old_pwd
            }
        })
    },

    /**
     * 绑定邮箱
     *
     * @param {Object} params
     * @param {string} params.scene - 场景值[change=修改,bind=绑定]
     * @param {string} params.email - 邮箱号
     * @param {string} params.code - 验证码
     * @returns {Promise<any>}
     * @author zero
     */
    bindEmail(params: { scene: string, email: string, code: string }): Promise<any> {
        return $request.post({
            url: '/user/bind_email',
            params: {
                scene: params.scene,
                email: params.email,
                code: params.code
            }
        })
    },

    /**
     * 绑定手机
     *
     * @param {Object} params
     * @param {string} params.scene - 场景值[change=修改,bind=绑定]
     * @param {string} params.mobile - 手机号
     * @param {string} params.code - 验证码
     * @returns {Promise<any>}
     * @author zero
     */
    bindMobile(params: { scene: string, mobile: string, code: string }): Promise<any> {
        return $request.post({
            url: '/user/bind_mobile',
            params: {
                scene: params.scene,
                mobile: params.mobile,
                code: params.code
            }
        })
    },

    /**
     * 绑定微信
     *
     * @param {Object} params
     * @param {string} params.state - 验证密钥
     * @param {string} params.code - 微信code
     * @returns {Promise<any>}
     * @author zero
     */
    bindWechat(params: { state: string, code: string }): Promise<any> {
        return $request.post({
            url: '/user/bind_wechat',
            params: {
                state: params.state,
                code: params.code
            }
        })
    }
}

export default userApi
