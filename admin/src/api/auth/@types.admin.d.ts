/**
 * 管理员列表类型
 */
interface AuthAdminListResponse {
    id: number;
    role: string;
    dept: string;
    avatar: string;
    nickname: string;
    username: string;
    mobile: string;
    email: string;
    is_disable: number;
    last_login_ip: string;
    last_login_time: string;
    create_time: string;
    update_time: string;
}

/**
 * 管理员自身类型
 */
interface AuthAdminOneselfResponse {
    user: {
        id: number;
        role_id: number;
        dept_id: number;
        post_id: number;
        avatar: string;
        nickname: string;
        username: string;
        mobile: string;
        email: string;
        role: string;
        is_disable: number;
    };
    perms: string[];
    menus: AuthAdminMenuResponse[];
}

/**
 * 管理员菜单类型
 */
interface AuthAdminMenuResponse {
    id: number;
    pid: number;
    type: string;
    name: string;
    icon: string;
    perms: string;
    params: string;
    component: string;
    path: string;
    is_show: number;
    is_disable: number;
    children: AuthAdminMenuResponse[];
}


/**
 * 管理员详情类型
 */
interface AuthAdminDetailResponse {
    id: number;
    role_id: number;
    dept_id: number;
    post_id: number;
    avatar: string;
    nickname: string;
    username: string;
    mobile: string;
    email: string;
    role: string;
    is_disable: number;
}
