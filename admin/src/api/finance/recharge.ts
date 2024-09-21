import request from '@/utils/request'

const rechargeApi = {
    /**
     * 充值记录列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/finance/recharge/lists',
            params
        })
    }
}

export default rechargeApi
