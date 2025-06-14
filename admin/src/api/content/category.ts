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
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.name]
     * @param {number} [params.is_disable]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        name?: string;
        is_disable?: number;
    }): Promise<any> {
        return request.get({
            url: '/content/category/lists',
            params
        })
    },

    /**
     * 文章分类详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/content/category/detail',
            params: { id }
        })
    },

    /**
     * 文章分类新增
     *
     * @param {Object} params
     * @param {string} params.name
     * @param {number} [params.sort]
     * @param {number} params.is_disable
     */
    add(params: {
        name: string;
        sort?: number;
        is_disable: number;
    }): Promise<any> {
        return request.post({
            url: '/content/category/add',
            params
        })
    },

    /**
     * 文章分类编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {string} params.name
     * @param {number} [params.sort]
     * @param {number} params.is_disable
     */
    edit(params: {
        id: number;
        name: string;
        sort?: number;
        is_disable: number;
    }): Promise<any> {
        return request.post({
            url: '/content/category/edit',
            params
        })
    },

    /**
     * 文章分类删除
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/content/category/delete',
            params: { id }
        })
    }
}

export default articleCateApi
