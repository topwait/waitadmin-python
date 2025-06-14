import request from '@/utils/request'

const rechargeApi = {
    /**
     * 充值记录列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.user]
     * @param {string} [params.order_sn]
     * @param {number} [params.pay_way]
     * @param {number} [params.pay_status]
     * @param {string} [params.start_time]
     * @param {string} [params.end_time]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        user?: string;
        order_sn?: string;
        pay_way?: number;
        pay_status?: number;
        start_time?: string;
        end_time?: string;
    }): Promise<any> {
        return request.get({
            url: '/finance/recharge/lists',
            params
        })
    }
}

export default rechargeApi
