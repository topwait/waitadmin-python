/**
 * 所有菜单类型
 */
interface AuthMenuWholeResponse {
    id: number;
    pid: number;
    name: string;
    children: AuthMenuWholeResponse[]
}

/**
 * 菜单列表类型
 */
interface AuthMenuListResponse {
    id: number;
    pid: number;
    type: string;
    name: string;
    icon: string;
    sort: number;
    perms: string;
    path: string;
    is_disable: number;
    create_time: string;
    update_time: string;
    children: AuthMenuListResponse[]
}

/**
 * 菜单详情类型
 */
interface AuthMenuDetailResponse {
    id: number;
    pid: number;
    type: string;
    name: string;
    icon: string;
    perms: string;
    params: string;
    component: string;
    path: string;
    sort: number;
    is_show: number;
    is_disable: number;
}
