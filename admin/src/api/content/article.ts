import request from '@/utils/request'

const articleApi = {
    /**
     * 文章列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.title]
     * @param {number} [params.status]
     * @param {string} [params.start_time]
     * @param {string} [params.end_time]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        title?: string;
        status?: number;
        start_time?: string;
        end_time?: string;
    }): Promise<any> {
        return request.get({
            url: '/content/article/lists',
            params
        })
    },

    /**
     * 文章详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/content/article/detail',
            params: { id }
        })
    },

    /**
     * 文章新增
     *
     * @param {Object} params
     * @param {number} params.cid
     * @param {string} params.title
     * @param {string} [params.image]
     * @param {string} [params.intro]
     * @param {string} [params.content]
     * @param {number} [params.sort]
     * @param {number} [params.is_topping]
     * @param {number} [params.is_recommend]
     * @param {number} [params.is_show]
     */
    add(params: {
        cid: number;
        title: string;
        image?: string;
        intro?: string;
        content?: string;
        sort?: number;
        is_topping?: number;
        is_recommend?: number;
        is_show?: number;
    }): Promise<any> {
        return request.post({
            url: '/content/article/add',
            params
        })
    },

    /**
     * 文章编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.cid
     * @param {string} params.title
     * @param {string} [params.image]
     * @param {string} [params.intro]
     * @param {string} [params.content]
     * @param {number} [params.sort]
     * @param {number} [params.is_topping]
     * @param {number} [params.is_recommend]
     * @param {number} [params.is_show]
     */
    edit(params: {
        id: number;
        cid: number;
        title: string;
        image?: string;
        intro?: string;
        content?: string;
        sort?: number;
        is_topping?: number;
        is_recommend?: number;
        is_show?: number;
    }): Promise<any> {
        return request.post({
            url: '/content/article/edit',
            params
        })
    },

    /**
     * 文章删除
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/content/article/delete',
            params: { id }
        })
    }
}

export default articleApi
