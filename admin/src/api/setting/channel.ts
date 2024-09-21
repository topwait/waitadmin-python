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
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/channel/save',
            params
        })
    }
}

export default channelApi
