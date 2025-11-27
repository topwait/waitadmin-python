/**
 * 通知配置列表类型
 */
interface SettingNoticeListResponse {
    id: number;
    scene: number;
    name: string;
    type: string;
    sys_status: number;
    ems_status: number;
    sms_status: number;
}

/**
 * 通知配置详情类型
 */
interface SettingNoticeDetailResponse {
    id: number;
    scene: number;
    name: string;
    type: string;
    client: string;
    remarks: string;
    variable: Record<string, string>,
    sys_template: {
        status: string;
        content: string;
        template_code: string;
    },
    ems_template: {
        status: string;
        content: string;
        template_code?: string;
    },
    sms_template: {
        status: string;
        content: string;
        template_code?: string;
    }
}
