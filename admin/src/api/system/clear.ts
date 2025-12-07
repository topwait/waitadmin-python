import request from '@/utils/request'

const clearApi = {
    /**
     * 清理缓存
     *
     * @param {Object} params
     * @param {boolean} params.system
     * @param {boolean} params.login
     * @returns {Promise<any>}
     * @author zero
     */
    clean(params: {
        system: boolean;
        login: boolean;
    }): Promise<any> {
        return request.post({
            url: '/system/clear/clean',
            params
        })
    }
}

export default clearApi
