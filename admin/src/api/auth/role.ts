import request from '@/utils/request'

const authRoleApi = {
    /**
     * 所有角色
     */
    whole(): Promise<any> {
        return request.get({
            url: '/auth/role/whole'
        })
    },

    /**
     * 角色列表
     */
    lists(): Promise<any> {
        return request.get({
            url: '/auth/role/lists'
        })
    },

    /**
     * 角色详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/role/detail',
            params: { id }
        })
    },

    /**
     * 角色新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/auth/role/add',
            params
        })
    },

    /**
     * 角色编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/auth/role/edit',
            params
        })
    },

    /**
     * 角色删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/role/delete',
            params: { id: id }
        })
    }
}

export default authRoleApi
