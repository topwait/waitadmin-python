import request from '@/utils/request'

const basicsApi = {
    /**
     * 网站配置详情
     *
     * @returns {Promise<SettingBasicsResponse>}
     * @author zero
     */
    detail(): Promise<SettingBasicsResponse> {
        return request.get<SettingBasicsResponse>({
            url: '/setting/basics/detail'
        })
    },

    /**
     * 网站配置保存
     *
     * @param {Object} params
     * @param {any} [params.website]
     * @param {any} [params.h5]
     * @param {any} [params.pc]
     * @returns {Promise<any>}
     * @author zero
     */
    save(params: {
        website?: any;
        h5?: any;
        pc?: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/basics/save',
            params
        })
    }
}

export default basicsApi
