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
     * @returns {AuthAdminListResponse[]}
     * @author zero
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        username?: string;
        mobile?: string;
        role?: number;
    }): Promise<AuthAdminListResponse[]> {
        return request.get<AuthAdminListResponse[]>({
            url: '/auth/admin/lists',
            params
        })
    },

    /**
     * 管理员自身
     *
     * @returns {AuthAdminOneselfResponse}
     * @author zero
     */
    oneself(): Promise<AuthAdminOneselfResponse> {
        return request.get<AuthAdminOneselfResponse>({
            url: '/auth/admin/oneself'
        })
    },

    /**
     * 管理员详情
     *
     * @param {number} id
     * @returns {AuthAdminDetailResponse}
     * @author zero
     */
    detail(id: number): Promise<AuthAdminDetailResponse> {
        return request.get<AuthAdminDetailResponse>({
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
     * @param {boolean} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
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
        is_disable?: boolean;
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
     * @param {boolean} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
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
        is_disable?: boolean;
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
     * @returns {Promise<any>}
     * @author zero
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
     * @returns {Promise<any>}
     * @author zero
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/admin/delete',
            params: { id }
        })
    }
}

export default authAdminApi
