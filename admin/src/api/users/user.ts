import request from '@/utils/request'

const userApi = {
    /**
     * 用户列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/users/user/lists',
            params
        })
    },

    /**
     * 用户详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/users/user/detail',
            params: { id }
        })
    },

    /**
     * 用户编辑
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
    adjustAccount(params: any): Promise<any> {
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
     */
    walletLogs(params: any): Promise<any> {
        return request.get({
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
     */
    sessions(params: any): Promise<any> {
        return request.get({
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
