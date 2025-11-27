/**
 * 友链列表类型
 */
interface SettingLinksListResponse {
    id: number;
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
 * 友链详情类型
 */
interface SettingLinksDetailResponse {
    id: number;
    title: string;
    image: string;
    target: string;
    url: string;
    sort: number;
    is_disable: number;
    create_time: string;
    update_time: string;
}
