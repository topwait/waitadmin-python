import request from '@/utils/request'

const rechargePackApi = {
    /**
     * 充值套餐列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/market/recharge/lists',
            params
        })
    },

    /**
     * 充值套餐详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/market/recharge/detail',
            params: { id }
        })
    },

    /**
     * 充值套餐新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/market/recharge/add',
            params
        })
    },

    /**
     * 充值套餐编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/market/recharge/edit',
            params
        })
    },

    /**
     * 充值套餐删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/market/recharge/delete',
            params: { id }
        })
    },

    /**
     * 充值参数配置
     */
    config(params: any) {
        return request.post({
            url: '/market/recharge/config',
            params
        })
    }
}

export default rechargePackApi
