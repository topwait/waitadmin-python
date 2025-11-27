/**
 * 所有角色类型
 */
interface AuthRoleWholeResponse {
    // ID
    id: number;
    // 角色名称
    name: string;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
}

/**
 * 角色列表类型
 */
interface AuthRoleListResponse {
    // ID
    id: number;
    // 角色名称
    name: string;
    // 角色描述
    describe: string;
    // 管理员数
    admin_sum: number;
    // 角色排序
    sort: number;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 角色详情类型
 */
interface AuthRoleDetailResponse {
    // ID
    id: number;
    // 角色名称
    name: string;
    // 角色描述
    describe: string;
    // 角色排序
    sort: number;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
    // 菜单ID
    menu_ids: number[]
}
