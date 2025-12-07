import request from '@/utils/request'

const basicsApi = {
    /**
     * 后台配置详情
     *
     * @returns {SettingBacksResponse}
     * @author zero
     */
    detail(): Promise<SettingBacksResponse> {
        return request.get<SettingBacksResponse>({
            url: '/setting/backs/detail'
        })
    },

    /**
     * 后台配置保存
     *
     * @param {Object} params
     * @param {string} [params.name]
     * @param {string} [params.title]
     * @param {string} [params.cover]
     * @param {string} [params.favicon]
     * @param {string} [params.logo_black_big]
     * @param {string} [params.logo_black_small]
     * @param {string} [params.logo_white_big]
     * @param {string} [params.logo_white_small]
     * @param {string} [params.contacts]
     * @param {string} [params.mobile]
     * @returns {Promise<any>}
     * @author zero
     */
    save(params: {
        name?: string;
        title?: string;
        cover?: string;
        favicon?: string;
        logo_black_big?: string;
        logo_black_small?: string;
        logo_white_big?: string;
        logo_white_small?: string;
        contacts?: string;
        mobile?: string;
    }): Promise<any> {
        return request.post({
            url: '/setting/backs/save',
            params
        })
    }
}

export default basicsApi
