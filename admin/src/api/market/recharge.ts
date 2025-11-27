import request from '@/utils/request'

const rechargePackApi = {
    /**
     * 充值套餐列表
     *
     * @returns {MarketRechargeListResponse[]}
     * @author zero
     */
    lists(): Promise<MarketRechargeListResponse[]> {
        return request.get<MarketRechargeListResponse[]>({
            url: '/market/recharge/lists'
        })
    },

    /**
     * 充值套餐详情
     *
     * @param {number} id
     * @returns {MarketRechargeDetailResponse}
     * @author zero
     */
    detail(id: number): Promise<MarketRechargeDetailResponse> {
        return request.get<MarketRechargeDetailResponse>({
            url: '/market/recharge/detail',
            params: { id }
        })
    },

    /**
     * 充值套餐新增
     *
     * @param {Object} params
     * @param {number} params.money
     * @param {number} params.give_money
     * @param {number} params.sort
     * @param {number} params.is_show
     * @returns {Promise<any>}
     * @author zero
     */
    add(params: {
        money: number;
        give_money: number;
        sort: number;
        is_show: number;
    }): Promise<any> {
        return request.post({
            url: '/market/recharge/add',
            params
        })
    },

    /**
     * 充值套餐编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.money
     * @param {number} params.give_money
     * @param {number} params.sort
     * @param {number} params.is_show
     * @returns {Promise<any>}
     * @author zero
     */
    edit(params: {
        id: number;
        money: number;
        give_money: number;
        sort: number;
        is_show: number;
    }): Promise<any> {
        return request.post({
            url: '/market/recharge/edit',
            params
        })
    },

    /**
     * 充值套餐删除
     *
     * @param {number} id
     * @returns {Promise<any>}
     * @author zero
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/market/recharge/delete',
            params: { id }
        })
    },

    /**
     * 充值配置更新
     *
     * @param {Object} params
     * @param {number} params.status
     * @param {number} params.min_recharge
     * @returns {Promise<any>}
     * @author zero
     */
    config(params: {
        status: number;
        min_recharge: number;
    }): Promise<any> {
        return request.post({
            url: '/market/recharge/config',
            params
        })
    }
}

export default rechargePackApi
