/**
 * 支付配置列表类型
 */
interface SettingPaymentListResponse {
    // ID
    id: number;
    // 渠道
    channel: number;
    // 缩写
    shorter: string;
    // 封面
    logo: string;
    // 图标
    icon: string;
    // 排序
    sort: number;
    // 状态
    status: boolean;
}

/**
 * 支付配置详情类型
 */
interface SettingPaymentDetailResponse {
    // ID
    id: number;
    // 渠道
    channel: number;
    // 缩写
    shorter: string;
    // 名称
    name: string;
    // 图标
    icon: string;
    // 排序
    sort: number;
    // 状态
    status: boolean;
    // 参数
    params: Record<string, string>
}
