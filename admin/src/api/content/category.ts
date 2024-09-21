import request from '@/utils/request'

const articleCateApi = {
    /**
     * 所有文章分类
     */
    whole(): Promise<any> {
        return request.get({
            url: '/content/category/whole'
        })
    },

    /**
     * 文章分类列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/content/category/lists',
            params
        })
    },

    /**
     * 文章分类详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/content/category/detail',
            params: { id }
        })
    },

    /**
     * 文章分类新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/content/category/add',
            params
        })
    },

    /**
     * 文章分类编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/content/category/edit',
            params
        })
    },

    /**
     * 文章分类删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/content/category/delete',
            params: { id }
        })
    }
}

export default articleCateApi
