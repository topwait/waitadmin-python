import request from '@/utils/request'

const authPostApi = {
    /**
     * 所有岗位
     */
    whole(): Promise<any> {
        return request.get({
            url: '/auth/post/whole'
        })
    },

    /**
     * 岗位列表
     */
    lists(): Promise<any> {
        return request.get({
            url: '/auth/post/lists'
        })
    },

    /**
     * 岗位详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/post/detail',
            params: { id }
        })
    },

    /**
     * 岗位新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/auth/post/add',
            params
        })
    },

    /**
     * 岗位编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/auth/post/edit',
            params
        })
    },

    /**
     * 岗位删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/post/delete',
            params: { id }
        })
    }
}

export default authPostApi
