import request from '@/utils/request'

const paymentApi = {
    /**
     * 支付配置列表
     */
    lists(): Promise<any> {
        return request.get({
            url: '/setting/payment/lists'
        })
    },

    /**
     * 支付配置详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/payment/detail',
            params: { id }
        })
    },

    /**
     * 支付配置保存
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.channel
     * @param {string} params.shorter
     * @param {string} params.name
     * @param {string} params.icon
     * @param {number} params.sort
     * @param {number} params.status
     * @param {any} params.params
     */
    save(params: {
        id: number;
        channel: number;
        shorter: string;
        name: string;
        icon: string;
        sort: number;
        status: number;
        params: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/payment/save',
            params
        })
    }
}

export default paymentApi
