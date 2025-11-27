/**
 * 充值套餐列表类型
 */
interface MarketRechargeListResponse {
    // ID
    id: number;
    // 金额
    money: number;
    // 赠送金额
    give_money: number;
    // 排序
    sort: number;
    // 是否显示: [0=否, 1=是]
    is_show: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 充值套餐详情类型
 */
interface MarketRechargeDetailResponse {
    // ID
    id: number;
    // 金额
    money: number;
    // 赠送金额
    give_money: number;
    // 排序
    sort: number;
    // 是否显示: [0=否, 1=是]
    is_show: number;
}
