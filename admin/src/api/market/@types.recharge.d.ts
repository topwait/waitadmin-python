/**
 * 充值套餐列表类型
 */
interface MarketRechargeListResponse {
    id: number;
    money: number;
    give_money: number;
    sort: number;
    is_show: number;
    create_time: string;
    update_time: string;
}

/**
 * 充值套餐详情类型
 */
interface MarketRechargeDetailResponse {
    id: number;
    money: number;
    give_money: number;
    sort: number;
    is_show: number;
}
