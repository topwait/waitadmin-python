/**
 * 所有部门类型
 */
interface AuthDeptWholeResponse {
    // ID
    id: number;
    // 父ID
    pid: number;
    // 部门名称
    name: string;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
    // 子部门
    children: AuthDeptWholeResponse[]
}

/**
 * 部门列表类型
 */
interface AuthDeptListResponse {
    // ID
    id: number;
    // 父ID
    pid: number;
    // 部门名称
    name: string;
    // 部门电话
    mobile: string;
    // 负责人
    duty: string;
    // 排序编号
    sort: number;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
    // 子部门
    children: AuthDeptListResponse[]
}

/**
 * 部门详情类型
 */
interface AuthDeptDetailResponse {
    // ID
    id: number;
    // 父ID
    pid: number;
    // 部门名称
    name: string;
    // 负责人名
    duty: string;
    // 部门电话
    mobile: string;
    // 排序编号
    sort: number;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
}
