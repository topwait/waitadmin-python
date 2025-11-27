import request from '@/utils/request'

const userApi = {
    /**
     * 用户列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.keyword]
     * @param {number} [params.is_disable]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        keyword?: string;
        is_disable?: number;
    }): Promise<UserListResponse[]> {
        return request.get<UserListResponse[]>({
            url: '/users/user/lists',
            params
        })
    },

    /**
     * 用户详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<UserDetailResponse> {
        return request.get<UserDetailResponse>({
            url: '/users/user/detail',
            params: { id }
        })
    },

    /**
     * 用户创建
     *
     * @param {Object} params
     * @param {string} params.account
     * @param {string} params.email
     * @param {string} params.mobile
     * @param {string} params.nickname
     * @param {string} params.password
     */
    create(params: {
        account: string;
        email: string;
        mobile: string;
        nickname: string;
        password: string;
    }): Promise<any> {
        return request.post({
            url: '/users/user/create',
            params
        })
    },

    /**
     * 用户编辑
     *
     * @param {number} user_id
     * @param {string} field
     * @param {string} value
     */
    edit(user_id: number, field: string, value: string): Promise<any> {
        return request.post({
            url: '/users/user/edit',
            params: {
                user_id,
                field,
                value: String(value)
            }
        })
    },

    /**
     * 拉黑名单
     *
     * @param {number} user_id
     */
    blacklist(user_id: number): Promise<any> {
        return request.post({
            url: '/users/user/blacklist',
            params: {
                user_id
            }
        })
    },

    /**
     * 修改分组
     *
     * @param {number} user_id
     * @param {number} group_id
     */
    changeGroup(user_id: number, group_id: number): Promise<any> {
        return request.post({
            url: '/users/user/change_group',
            params: {
                user_id,
                group_id
            }
        })
    },

    /**
     * 重置密码
     *
     * @param {number} user_id
     * @param {string} password
     */
    resetPassword(user_id: number, password: string): Promise<any> {
        return request.post({
            url: '/users/user/reset_password',
            params: {
                user_id,
                password
            }
        })
    },

    /**
     * 调整账户
     */
    adjustAccount(params: {
        user_id: number;
        action: string;
        amount: number;
        remark?: string;
    }): Promise<any> {
        return request.post({
            url: '/users/user/adjust_account',
            params: {
                user_id: params.user_id,
                action: params.action,
                amount: params.amount,
                remark: params.remark
            }
        })
    },

    /**
     * 账户日志
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {number} params.user_id
     */
    walletLogs(params: {
        page_no?: number;
        page_size?: number;
        user_id: string;
    }): Promise<UserWalletLogsResponse[]> {
        return request.get<UserWalletLogsResponse[]>({
            url: '/users/user/wallet_logs',
            params: {
                user_id: params.user_id,
                page_no: params.page_no,
                page_size: params.page_size
            }
        })
    },

    /**
     * 会话列表
     *
     * @param {Object} params
     * @param {number} params.user_id
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     */
    sessions(params: {
        user_id: number;
        page_no?: number;
        page_size?: number;
    }): Promise<UserSessionResponse[]> {
        return request.get<UserSessionResponse[]>({
            url: '/users/user/sessions',
            params: {
                user_id: params.user_id,
                page_no: params.page_no,
                page_size: params.page_size
            }
        })
    },

    /**
     * 强制下线
     *
     * @param {number} user_id
     * @param {string} uuid
     */
    kickOut(user_id: number, uuid: string): Promise<any> {
        return request.post({
            url: '/users/user/kick_out',
            params: {
                uuid,
                user_id
            }
        })
    }
}

export default userApi
