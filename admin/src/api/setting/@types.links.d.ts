/**
 * 友链列表类型
 */
interface SettingLinksListResponse {
    // ID
    id: number;
    // 标题
    title: string;
    // 封面
    image: string;
    // 目标
    target: string;
    // 链接
    url: string;
    // 排序
    sort: number;
    // 是否禁用
    is_disable: boolean;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 友链详情类型
 */
interface SettingLinksDetailResponse {
    // ID
    id: number;
    // 标题
    title: string;
    // 封面
    image: string;
    // 目标
    target: string;
    // 链接
    url: string;
    // 排序
    sort: number;
    // 是否禁用
    is_disable: boolean;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}
