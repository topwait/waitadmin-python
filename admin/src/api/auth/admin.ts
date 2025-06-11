import request from '@/utils/request'

const authAdminApi = {
    /**
     * 管理员列表
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
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/admin/detail',
            params: { id }
        })
    },

    /**
     * 管理员新增
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
     */
    edit(params: {
        id: number,
        role_id: number,
        dept_id?: number,
        post_id?: number,
        nickname: string,
        username: string,
        password: string,
        avatar: string,
        mobile?: string,
        email?: string,
        is_disable?: number
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
    */
    setInfo(params: {
        avatar: string,
        nickname: string,
        mobile?: string
        email?: string
        password?: string
        password_old?: string
    }): Promise<any> {
        return request.post({
            url: '/auth/admin/set_info',
            params
        })
    },

    /**
     * 管理员删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/admin/delete',
            params: { id }
        })
    }
}

export default authAdminApi
