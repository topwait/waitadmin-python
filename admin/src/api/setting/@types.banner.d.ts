/**
 * 轮播图位置类型
 */
interface SettingBannerSitesResponse {
    id: number;
    name: string;
}

/**
 * 轮播图列表类型
 */
interface SettingBannerListResponse {
    id: number;
    position: string;
    title: string;
    image: string;
    target: string;
    url: string;
    sort: number;
    is_disable: number;
    create_time: string;
    update_time: string;
}

/**
 * 轮播图详情类型
 */
interface SettingBannerDetailResponse {
    id: number;
    position: number;
    title: string;
    image: string;
    target: string;
    url: string;
    sort: number;
    is_disable: number;
    create_time: string;
    update_time: string;
}
