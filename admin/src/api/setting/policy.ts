import request from '@/utils/request'

const policyApi = {
    /**
     * 协议配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/policy/detail'
        })
    },

    /**
     * 协议配置保存
     *
     * @param {Object} params
     * @param {string} params.service
     * @param {string} params.private
     * @param {string} params.payment
     */
    save(params: {
        service: string;
        private: string;
        payment: string;
    }): Promise<any> {
        return request.post({
            url: '/setting/policy/save',
            params
        })
    }
}

export default policyApi
