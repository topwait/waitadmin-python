/**
 * 充值套餐类型
 */
interface RechargePackageResponse {
    // ID
    id: string;
    // 套餐名称
    name: string;
    // 充值金额
    money: number;
    // 赠送金额
    give_money: number;
}
