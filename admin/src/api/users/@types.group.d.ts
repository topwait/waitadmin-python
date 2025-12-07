/**
 * 全部用户分组类型
 */
interface UserGroupWholeResponse {
    // ID
    id: number;
    // 名称
    name: string;
}

/**
 * 用户分组列表类型
 */
interface UserGroupListResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 备注
    remarks: string;
    // 排序
    sort: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 用户分组详情类型
 */
interface UserGroupDetailResponse {
    // ID
    id: number;
    // 名称
    name: string;
    // 排序
    sort: number;
}
