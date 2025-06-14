import request from '@/utils/request'

const clearApi = {
    /**
     * 清理缓存
     *
     * @param {Object} params
     * @param {boolean | number} params.system
     * @param {boolean | number} params.login
     */
    clean(params: {
        system: boolean | number;
        login: boolean | number;
    }): Promise<any> {
        return request.post({
            url: '/system/clear/clean',
            params
        })
    }
}

export default clearApi
