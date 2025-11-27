/**
 * 所有部门类型
 */
interface AuthDeptWholeResponse {
    id: number;
    pid: number;
    name: string;
    is_disable: number;
    children: AuthDeptWholeResponse[]
}

/**
 * 部门列表类型
 */
interface AuthDeptListResponse {
    id: number;
    pid: number;
    name: string;
    mobile: string;
    duty: string;
    sort: number;
    is_disable: number;
    create_time: string;
    update_time: string;
    children: AuthDeptListResponse[]
}

/**
 * 部门详情类型
 */
interface AuthDeptDetailResponse {
    id: number;
    pid: number;
    name: string;
    duty: string;
    mobile: string;
    sort: number;
    is_disable: number;
}
