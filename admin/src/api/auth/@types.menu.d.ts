/**
 * 所有菜单类型
 */
interface AuthMenuWholeResponse {
    // ID
    id: number;
    // 父ID
    pid: number;
    // 菜单名称
    name: string;
    // 子菜单
    children: AuthMenuWholeResponse[]
}

/**
 * 菜单列表类型
 */
interface AuthMenuListResponse {
    // ID
    id: number;
    // 父ID
    pid: number;
    // 权限类型: [M=目录, C=菜单, A=按钮]
    type: string;
    // 菜单名称
    name: string;
    // 菜单图标
    icon: string;
    // 菜单排序
    sort: number;
    // 路由权限
    perms: string;
    // 路径地址
    path: string;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
    // 子菜单
    children: AuthMenuListResponse[]
}

/**
 * 菜单详情类型
 */
interface AuthMenuDetailResponse {
    // ID
    id: number;
    // 父ID
    pid: number;
    // 权限类型: [M=目录, C=菜单, A=按钮]
    type: string;
    // 菜单名称
    name: string;
    // 菜单图标
    icon: string;
    // 菜单权限
    perms: string;
    // 路由参数
    params: string;
    // 组件路径
    component: string;
    // 页面路径
    path: string;
    // 菜单排序
    sort: number;
    // 是否显示: [0=否, 1=是]
    is_show: number;
    // 是否禁用: [0=否, 1=是]
    is_disable: number;
}
