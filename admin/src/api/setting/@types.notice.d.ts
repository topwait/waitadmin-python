/**
 * 通知配置列表类型
 */
interface SettingNoticeListResponse {
    // ID
    id: number;
    // 场景
    scene: number;
    // 名称
    name: string;
    // 类型
    type: string;
    // 系统状态: [0=停用, 1=启用, 2=没有]
    sys_status: number;
    // 短信状态: [0=停用, 1=启用, 2=没有]
    ems_status: number;
    // 短信状态: [0=停用, 1=启用, 2=没有]
    sms_status: number;
}

/**
 * 通知配置详情类型
 */
interface SettingNoticeDetailResponse {
    // ID
    id: number;
    // 场景
    scene: number;
    // 名称
    name: string;
    // 类型
    type: string;
    // 客户端
    client: string;
    // 备注
    remarks: string;
    // 变量
    variable: Record<string, string>,
    // 系统模板
    sys_template: {
        // 状态: [0=停用, 1=启用, 2=没有]
        status: number;
        // 内容
        content: string;
        // 模板编码
        template_code: string;
    },
    // 短信模板
    ems_template: {
        // 状态: [0=停用, 1=启用, 2=没有]
        status: number;
        // 内容
        content: string;
        // 模板编码
        template_code?: string;
    },
    // 短信模板
    sms_template: {
        // 状态: [0=停用, 1=启用, 2=没有]
        status: number;
        // 内容
        content: string;
        // 模板编码
        template_code?: string;
    }
}
