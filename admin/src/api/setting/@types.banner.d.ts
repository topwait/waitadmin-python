/**
 * 轮播图位置类型
 */
interface SettingBannerSitesResponse {
    // ID
    id: number;
    // 名称
    name: string;
}

/**
 * 轮播图列表类型
 */
interface SettingBannerListResponse {
    // ID
    id: number;
    // 位置
    position: string;
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
 * 轮播图详情类型
 */
interface SettingBannerDetailResponse {
    // ID
    id: number;
    // 位置
    position: number;
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
