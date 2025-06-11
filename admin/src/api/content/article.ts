import request from '@/utils/request'

const articleApi = {
    /**
     * 文章列表
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
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/content/article/delete',
            params: { id }
        })
    }
}

export default articleApi
