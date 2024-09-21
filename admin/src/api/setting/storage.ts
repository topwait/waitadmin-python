import request from '@/utils/request'

const storageApi = {
    /**
     * 存储配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/storage/detail'
        })
    },

    /**
     * 存储配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/storage/save',
            params
        })
    }
}

export default storageApi
