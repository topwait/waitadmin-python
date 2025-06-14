import request from '@/utils/request'

const channelApi = {
    /**
     * 渠道配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/channel/detail'
        })
    },

    /**
     * 渠道配置保存
     *
     * @param {Object} params
     * @param {any} [params.wx]
     * @param {any} [params.oa]
     * @param {any} [params.op]
     */
    save(params: {
        wx?: any;
        oa?: any;
        op?: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/channel/save',
            params
        })
    }
}

export default channelApi
