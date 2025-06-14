import request from '@/utils/request'

const linksApi = {
    /**
     * 友链列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.title]
     * @param {number} [params.is_disable]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        title?: string;
        is_disable?: number;
    }): Promise<any> {
        return request.get({
            url: '/setting/links/lists',
            params
        })
    },

    /**
     * 友链详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/links/detail',
            params: { id }
        })
    },

    /**
     * 友链新增
     *
     * @param {Object} params
     * @param {string} params.title
     * @param {string} [params.image]
     * @param {string} [params.target]
     * @param {string} [params.url]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     */
    add(params: {
        title: string;
        image?: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/setting/links/add',
            params
        })
    },

    /**
     * 友链编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {string} params.title
     * @param {string} [params.image]
     * @param {string} [params.target]
     * @param {string} [params.url]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     */
    edit(params: {
        id: number;
        title: string;
        image?: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/setting/links/edit',
            params
        })
    },

    /**
     * 友链删除
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/setting/links/delete',
            params: {
                id
            }
        })
    }
}

export default linksApi
