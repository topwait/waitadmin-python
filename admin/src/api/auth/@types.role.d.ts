/**
 * 所有角色类型
 */
interface AuthRoleWholeResponse {
    id: number;
    name: string;
    is_disable: number;
}

/**
 * 角色列表类型
 */
interface AuthRoleListResponse {
    id: number;
    name: string;
    describe: string;
    admin_sum: number;
    sort: number;
    is_disable: number;
    create_time: string;
    update_time: string;
}

/**
 * 角色详情类型
 */
interface AuthRoleDetailResponse {
    id: number;
    name: string;
    describe: string;
    sort: number;
    is_disable: number;
    menu_ids: number[]
}
