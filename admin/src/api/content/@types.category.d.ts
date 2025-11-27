/**
 * 所有文章分类类型
 */
interface ContentCategoryWholeResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 是否禁用: [0=否, 1=是]"
    is_disable: number;
}

/**
 * 文章分类列表类型
 */
interface ContentCategoryListResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 排序
    sort: number;
    // 是否禁用: [0=否, 1=是]"
    is_disable: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 文章分类详情类型
 */
interface ContentCategoryDetailResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 排序
    sort: number;
    // 是否禁用: [0=否, 1=是]"
    is_disable: number;
}
