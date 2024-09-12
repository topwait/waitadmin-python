import request from '@/utils/request'

const authAdminApi = {
    /**
     * 管理员列表
     */
    lists(params: any): Promise<any> {
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
    add(params: any): Promise<any> {
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
    edit(params: any): Promise<any> {
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
    setInfo(params: any): Promise<any> {
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
