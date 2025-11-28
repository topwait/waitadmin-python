const rechargeApi = {
    /**
     * 套餐列表
     *
     * @returns {RechargePackageResponse[]}
     * @author zero
     */
    package(): Promise<RechargePackageResponse[]> {
        return $request.get<RechargePackageResponse[]>({
            url: '/recharge/package'
        })
    },

    /**
     * 充值下单
     *
     * @param params
     * @param {number} params.money - 充值金额
     * @param {number} [params.package_id] - 套餐ID
     * @returns {Promise<any>}
     * @author zero
     */
    place(params: {
        money: number;
        package_id?: number;
    }): Promise<any> {
        return $request.post({
            url: '/recharge/place',
            params
        })
    }
}

export default rechargeApi
