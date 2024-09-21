const rechargeApi = {
    /**
     * 套餐列表
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
     * @returns Promise<any>
     * @author zero
     */
    place(params: {
        money: number,
        package_id?: number
    }): Promise<any> {
        return $request.post({
            url: '/recharge/place',
            params
        })
    }
}

export default rechargeApi