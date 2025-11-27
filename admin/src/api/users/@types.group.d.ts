/**
 * 全部用户分组类型
 */
interface UserGroupWholeResponse {
    id: number;
    name: string;
}

/**
 * 用户分组列表类型
 */
interface UserGroupListResponse {
    id: number;
    name: string;
    remarks: string;
    sort: number;
    create_time: string;
    update_time: string;
}

/**
 * 用户分组详情类型
 */
interface UserGroupDetailResponse {
    id: number;
    name: string;
    sort: number;
    is_disable: number;
}
