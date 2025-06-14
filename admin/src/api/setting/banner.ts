import request from '@/utils/request'

const bannerApi = {
    /**
     * 轮播图位置
     */
    sites(): Promise<any> {
        return request.get({
            url: '/setting/banner/sites'
        })
    },

    /**
     * 轮播图列表
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
            url: '/setting/banner/lists',
            params
        })
    },

    /**
     * 轮播图详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/banner/detail',
            params: { id }
        })
    },

    /**
     * 轮播图新增
     *
     * @param {Object} params
     * @param {number} params.position
     * @param {string} params.title
     * @param {string} params.image
     * @param {string} params.target
     * @param {string} [params.url]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     */
    add(params: {
        position: number;
        title: string;
        image: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/setting/banner/add',
            params
        })
    },

    /**
     * 轮播图保存
     *
     * @param {Object} params
     * @param {number} params.position
     * @param {string} params.title
     * @param {string} params.image
     * @param {string} params.target
     * @param {string} [params.url]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     */
    edit(params: {
        id: number;
        position: number;
        title: string;
        image: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/setting/banner/edit',
            params
        })
    },

    /**
     * 轮播图删除
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/setting/banner/delete',
            params: { id }
        })
    }
}

export default bannerApi
