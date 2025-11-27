/**
 * 支付配置列表类型
 */
interface SettingPaymentListResponse {
    id: number;
    channel: number;
    shorter: string;
    logo: string;
    icon: string;
    sort: number;
    status: number;
}

/**
 * 支付配置详情类型
 */
interface SettingPaymentDetailResponse {
    id: number;
    channel: number;
    shorter: string;
    name: string;
    icon: string;
    sort: number;
    status: number;
    params: Record<string, string>
}

