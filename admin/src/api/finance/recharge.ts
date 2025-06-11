import request from '@/utils/request'

const rechargeApi = {
    /**
     * 充值记录列表
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
