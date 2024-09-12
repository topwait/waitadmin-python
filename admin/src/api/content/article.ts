import request from '@/utils/request'

const articleApi = {
    /**
     * 文章列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/content/article/lists',
            params
        })
    },

    /**
     * 文章详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/content/article/detail',
            params: { id }
        })
    },

    /**
     * 文章新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/content/article/add',
            params
        })
    },

    /**
     * 文章编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/content/article/edit',
            params
        })
    },

    /**
     * 文章删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/content/article/delete',
            params: { id }
        })
    }
}

export default articleApi
