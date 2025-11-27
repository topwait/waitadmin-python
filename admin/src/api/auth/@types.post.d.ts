/**
 * 所有岗位类型
 */
interface AuthPostWholeResponse {
    id: number;
    code: string;
    name: string;
}

/**
 * 岗位列表类型
 */
interface AuthPostListResponse {
    id: number;
    code: string;
    name: string;
    remarks: string;
    sort: number;
    is_disable: number;
    create_time: string;
    update_time: string;
}

/**
 * 岗位详情类型
 */
interface AuthPostDetailResponse {
    id: number;
    code: string;
    name: string;
    remarks: string;
    sort: number;
    is_disable: number;
}
