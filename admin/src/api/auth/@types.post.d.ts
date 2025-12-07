/**
 * 所有岗位类型
 */
interface AuthPostWholeResponse {
    // ID
    id: number;
    // 岗位编号
    code: string;
    // 岗位名称
    name: string;
}

/**
 * 岗位列表类型
 */
interface AuthPostListResponse {
    // ID
    id: number;
    // 岗位编号
    code: string;
    // 岗位名称
    name: string;
    // 岗位备注
    remarks: string;
    // 岗位排序
    sort: number;
    // 是否禁用
    is_disable: boolean;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 岗位详情类型
 */
interface AuthPostDetailResponse {
    // ID
    id: number;
    // 岗位编号
    code: string;
    // 岗位名称
    name: string;
    // 岗位备注
    remarks: string;
    // 岗位排序
    sort: number;
    // 是否禁用
    is_disable: boolean;
}
