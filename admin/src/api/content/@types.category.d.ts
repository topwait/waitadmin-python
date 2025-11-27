/**
 * 所有文章分类类型
 */
interface ContentCategoryWholeResponse {
    id: number;
    name: string;
    is_disable: number;
}

/**
 * 文章分类列表类型
 */
interface ContentCategoryListResponse {
    id: number;
    name: string;
    sort: number;
    is_disable: number;
    create_time: string;
    update_time: string;
}

/**
 * 文章分类详情类型
 */
interface ContentCategoryDetailResponse {
    id: number;
    name: string;
    sort: number;
    is_disable: number;
}
