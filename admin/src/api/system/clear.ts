import request from '@/utils/request'

const clearApi = {
    /**
     * 清理缓存
     */
    clean(params: any): Promise<any> {
        return request.post({
            url: '/system/clear/clean',
            params
        })
    }
}

export default clearApi
