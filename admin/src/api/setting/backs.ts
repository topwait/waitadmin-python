import request from '@/utils/request'

const basicsApi = {
    /**
     * 后台配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/backs/detail'
        })
    },

    /**
     * 后台配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/backs/save',
            params
        })
    }
}

export default basicsApi
