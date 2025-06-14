import request from '@/utils/request'

const authAdminApi = {
    /**
     * 管理员列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.username]
     * @param {string} [params.mobile]
     * @param {string} [params.role]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        username?: string;
        mobile?: string;
        role?: number;
    }): Promise<any> {
        return request.get({
            url: '/auth/admin/lists',
            params
        })
    },

    /**
     * 管理员自身
     */
    oneself(): Promise<any> {
        return request.get({
            url: '/auth/admin/oneself'
        })
    },

    /**
     * 管理员详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/admin/detail',
            params: { id }
        })
    },

    /**
     * 管理员新增
     *
     * @param {Object} params
     * @param {number} params.role_id
     * @param {number} [params.dept_id]
     * @param {number} [params.post_id]
     * @param {string} params.nickname
     * @param {string} params.username
     * @param {string} params.password
     * @param {string} params.avatar
     * @param {string} [params.mobile]
     * @param {string} [params.email]
     * @param {number} [params.is_disable]
     */
    add(params: {
        role_id: number;
        dept_id?: number;
        post_id?: number;
        nickname: string;
        username: string;
        password: string;
        avatar: string;
        mobile?: string;
        email?: string;
        is_disable?: number;
    }): Promise<any> {
        params.dept_id = params.dept_id ? params.dept_id : 0
        params.post_id = params.post_id ? params.post_id : 0
        return request.post({
            url: '/auth/admin/add',
            params
        })
    },

    /**
     * 管理员编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.role_id
     * @param {number} [params.dept_id]
     * @param {number} [params.post_id]
     * @param {string} params.nickname
     * @param {string} params.username
     * @param {string} params.password
     * @param {string} params.avatar
     * @param {string} [params.mobile]
     * @param {string} [params.email]
     * @param {number} [params.is_disable]
     */
    edit(params: {
        id: number;
        role_id: number;
        dept_id?: number;
        post_id?: number;
        nickname: string;
        username: string;
        password: string;
        avatar: string;
        mobile?: string;
        email?: string;
        is_disable?: number;
    }): Promise<any> {
        params.dept_id = params.dept_id ? params.dept_id : 0
        params.post_id = params.post_id ? params.post_id : 0
        return request.post({
            url: '/auth/admin/edit',
            params
        })
    },

    /**
     * 管理员设置
     *
     * @param {Object} params
     * @param {string} params.avatar
     * @param {string} params.nickname
     * @param {string} [params.mobile]
     * @param {string} [params.email]
     * @param {string} [params.password]
     * @param {string} [params.password_old]
     */
    setInfo(params: {
        avatar: string;
        nickname: string;
        mobile?: string;
        email?: string;
        password?: string;
        password_old?: string;
    }): Promise<any> {
        return request.post({
            url: '/auth/admin/set_info',
            params
        })
    },

    /**
     * 管理员删除
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/admin/delete',
            params: { id }
        })
    }
}

export default authAdminApi
