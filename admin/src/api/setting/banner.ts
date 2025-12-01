import request from '@/utils/request'

const bannerApi = {
    /**
     * 轮播图位置
     *
     * @returns {SettingBannerSitesResponse[]}
     * @author zero
     */
    sites(): Promise<SettingBannerSitesResponse[]> {
        return request.get<SettingBannerSitesResponse[]>({
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
     * @param {boolean} [params.is_disable]
     * @returns {SettingBannerListResponse[]}
     * @author zero
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        title?: string;
        is_disable?: boolean;
    }): Promise<SettingBannerListResponse[]> {
        return request.get<SettingBannerListResponse[]>({
            url: '/setting/banner/lists',
            params
        })
    },

    /**
     * 轮播图详情
     *
     * @param {number} id
     * @returns {SettingBannerDetailResponse}
     * @author zero
     */
    detail(id: number): Promise<SettingBannerDetailResponse> {
        return request.get<SettingBannerDetailResponse>({
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
     * @param {boolean} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
     */
    add(params: {
        position: number;
        title: string;
        image: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: boolean;
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
     * @param {boolean} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
     */
    edit(params: {
        id: number;
        position: number;
        title: string;
        image: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: boolean;
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
     * @returns {Promise<any>}
     * @author zero
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/setting/banner/delete',
            params: { id }
        })
    }
}

export default bannerApi
