import request from '@/utils/request'

const authDeptApi = {
    /**
     * 所有部门
     */
    whole(): Promise<any> {
        return request.get({
            url: '/auth/dept/whole'
        })
    },

    /**
     * 部门列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/auth/dept/lists',
            params
        })
    },

    /**
     * 部门详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/dept/detail',
            params: { id }
        })
    },

    /**
     * 部门新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/auth/dept/add',
            params
        })
    },

    /**
     * 部门编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/auth/dept/edit',
            params
        })
    },

    /**
     * 部门删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/dept/delete',
            params: { id }
        })
    }
}

export default authDeptApi
